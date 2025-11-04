from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from cities_query.models import SpatialCity
import time

class Command(BaseCommand):
    help = 'Test proximity search performance'
   
    def handle(self, *args, **options):
        test_points = [
            (53.3498, -6.2603),  # Dublin
            (51.5074, -0.1278),  # London
            (40.7128, -74.0060), # New York
            (35.6762, 139.6503), # Tokyo
            (-33.8688, 151.2093) # Sydney
        ]
       
        times = []
       
        for lat, lng in test_points:
            search_point = Point(lng, lat, srid=4326)
           
            start_time = time.time()
           
            nearest_cities = list(SpatialCity.objects.annotate(
                distance=Distance('location', search_point)
            ).order_by('distance')[:10])
           
            end_time = time.time()
            query_time = (end_time - start_time) * 1000
            times.append(query_time)
           
            self.stdout.write(
                f"Search at ({lat}, {lng}): {query_time:.2f}ms, found {len(nearest_cities)} cities"
            )
       
        avg_time = sum(times) / len(times)
        self.stdout.write(
            self.style.SUCCESS(f"Average query time: {avg_time:.2f}ms")
        )