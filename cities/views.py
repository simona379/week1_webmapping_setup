from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse
from .models import City
from django.db import models
from .serializers import CitySerializer, CityListSerializer
from django.core.exceptions import ValidationError
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance


@method_decorator(cache_page(60 * 5), name='get')  # Cache for 5 minutes
class CityListCreateView(generics.ListCreateAPIView):
    queryset = City.objects.all()
   
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CityListSerializer
        return CitySerializer
    
    def perform_create(self, serializer):
        try:
            # Validate coordinates
            lat = float(serializer.validated_data['latitude'])
            lng = float(serializer.validated_data['longitude'])
           
            if not (-90 <= lat <= 90):
                raise ValidationError("Latitude must be between -90 and 90")
            if not (-180 <= lng <= 180):
                raise ValidationError("Longitude must be between -180 and 180")
           
            serializer.save()
        except (ValueError, ValidationError) as e:
            raise ValidationError(f"Invalid data: {str(e)}")



class CityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer



@api_view(['GET'])
def cities_geojson(request):
    """Return cities data in GeoJSON format for Leaflet"""
    features = []
    for city in City.objects.all():
        # guard in case location is missing
        lat = float(city.latitude) if city.latitude is not None else None
        lon = float(city.longitude) if city.longitude is not None else None

        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat],  # GeoJSON: [lon, lat]
            },
            "properties": {
                "id": city.id,
                "name": city.name,
                "country": city.country,
                "population": city.population,
                "description": getattr(city, "description", "") or "",
                "founded_year": city.founded_year,
                "area_km2": float(getattr(city, "area_km2", 0)) if getattr(city, "area_km2", None) else None,
                "timezone": city.timezone or "",
                # 👇 add these so your UI can read them directly
                "latitude": lat,
                "longitude": lon,
            }
        })

    return JsonResponse({"type": "FeatureCollection", "features": features})

def map_view(request):
    """Render the main map page"""
    return render(request, 'cities/map.html')

@api_view(['GET'])
def city_search(request):
    """Search cities by name or country"""
    query = request.GET.get('q', '')
    if query:
        cities = City.objects.filter(
            models.Q(name__icontains=query) |
            models.Q(country__icontains=query)
        )
    else:
        cities = City.objects.all()
   
    serializer = CityListSerializer(cities, many=True)
    return Response(serializer.data)


try:
    from cities_query.models import SpatialCity 
except Exception:
    SpatialCity = None


# Add this optimized version
@api_view(['POST'])
def find_nearest_cities_optimized(request):
    """Optimized version with better performance"""
    try:
        data = request.data
        lat = float(data.get('lat'))
        lng = float(data.get('lng'))
        limit = int(data.get('limit', 10))  # Allow custom limit
       
        search_point = Point(lng, lat, srid=4326)
       
        # Optimized query with limited fields
        nearest_cities = SpatialCity.objects.annotate(
            distance=Distance('location', search_point)
        ).only(
            'id', 'name', 'country', 'population', 'latitude', 'longitude', 'description'
        ).order_by('distance')[:limit]
       
        # Faster serialization
        results = [
            {
                'rank': i + 1,
                'id': city.id,
                'name': city.name,
                'country': city.country,
                'population': city.population,
                'coordinates': {'lat': city.latitude, 'lng': city.longitude},
                'distance_km': round(city.distance.km, 2),
                'description': city.description
            }
            for i, city in enumerate(nearest_cities)
        ]
       
        return Response({
            'search_point': {'lat': lat, 'lng': lng},
            'total_found': len(results),
            'nearest_cities': results
        })
       
    except Exception as e:
        return Response({'error': str(e)}, status=500)

