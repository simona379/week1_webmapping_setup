// Proximity Map (cities_query/map.html)
let map;
// Initialize proximity search when map loads
document.addEventListener('DOMContentLoaded', function() {
// proximity_map.js
  if (!document.getElementById('toggle-proximity')) return;

  // if map.js already made window.map, use it; otherwise wait briefly
  const start = () => window.proximitySearch = new ProximitySearch(window.Map);
  if (window.Map) start();
  else setTimeout(() => { if (window.Map) start(); }, 500);
});

//Week 5 - proximity Search
class ProximitySearch {
    constructor(map) {
        this.map = map;
        this.searchMarker = null;
        this.nearestCitiesLayer = L.layerGroup().addTo(this.map);
        this.radiusCircle = null;
        this.isProximityMode = false;
        
        this.initializeProximityFeatures();
    }
    
    initializeProximityFeatures() {
        // Add proximity search toggle button
        this.addProximityControls();
        
        // Add click handler for proximity search
        this.map.on('click', (e) => {
            if (this.isProximityMode) {
                this.performProximitySearch(e.latlng.lat, e.latlng.lng);
            }
        });
    }
    
    addProximityControls() {
        // Add toggle button to existing controls
        const proximityToggle = document.createElement('button');
        proximityToggle.id = 'proximity-toggle';
        proximityToggle.className = 'btn btn-outline-primary';
        proximityToggle.innerHTML = '📍 Proximity Search';
        proximityToggle.onclick = () => this.toggleProximityMode();
        
        // Add to existing control panel
        const controlPanel = document.querySelector('.map-controls') || document.body;
        controlPanel.appendChild(proximityToggle);
        
        // Add radius input
        const radiusInput = document.createElement('input');
        radiusInput.id = 'radius-input';
        radiusInput.type = 'number';
        radiusInput.value = '100';
        radiusInput.placeholder = 'Radius (km)';
        radiusInput.className = 'form-control d-none';
        radiusInput.style.width = '120px';
        radiusInput.style.display = 'inline-block';
        radiusInput.style.marginLeft = '10px';
        
        controlPanel.appendChild(radiusInput);
    }
    
    toggleProximityMode() {
        this.isProximityMode = !this.isProximityMode;
        const toggleBtn = document.getElementById('proximity-toggle');
        const radiusInput = document.getElementById('radius-input');
        
        if (this.isProximityMode) {
            toggleBtn.innerHTML = '❌ Exit Proximity';
            toggleBtn.className = 'btn btn-danger';
            radiusInput.classList.remove('d-none');
            this.map.getContainer().style.cursor = 'crosshair';
            showAlert('Click anywhere on the map to find nearest cities', 'info');
        } else {
            toggleBtn.innerHTML = '📍 Proximity Search';
            toggleBtn.className = 'btn btn-outline-primary';
            radiusInput.classList.add('d-none');
            this.map.getContainer().style.cursor = '';
            this.clearProximityResults();
        }
    }
    
    async performProximitySearch(lat, lng) {
        // Clear previous results
        this.clearProximityResults();
        
        // Add search marker
        this.searchMarker = L.marker([lat, lng], {
            icon: L.icon({
                iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
                shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                iconSize: [25, 41],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34]
            })
        }).addTo(this.map);
        
        this.searchMarker.bindPopup(`
            <strong>Search Point</strong><br>
            Lat: ${lat.toFixed(6)}<br>
            Lng: ${lng.toFixed(6)}
        `).openPopup();
        
        // Show loading
        showLoading(true);
        
        try {
            const response = await fetch('/cities/api/nearest/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({ lat, lng })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            this.displayNearestCities(data.nearest_cities);
            this.updateResultsPanel(data);
            
        } catch (error) {
            console.error('Error finding nearest cities:', error);
            showAlert('Error performing proximity search. Please try again.', 'danger');
        } finally {
            showLoading(false);
        }
    }
    
    displayNearestCities(cities) {
        cities.forEach((city, index) => {
            const marker = L.marker([city.coordinates.lat, city.coordinates.lng], {
                icon: this.getNumberedIcon(city.rank)
            });
            
            const popupContent = `
                <div class="city-popup proximity-result">
                    <h6>#${city.rank} ${city.name}</h6>
                    <p><strong>Country:</strong> ${city.country}</p>
                    <p><strong>Population:</strong> ${city.population.toLocaleString()}</p>
                    <p><strong>Distance:</strong> ${city.distance_km} km (${city.distance_miles} mi)</p>
                    ${city.founded_year ? `<p><strong>Founded:</strong> ${city.founded_year}</p>` : ''}
                    ${city.description ? `<p><em>${city.description}</em></p>` : ''}
                    <button class="btn btn-sm btn-primary" onclick="proximitySearch.zoomToCity(${city.coordinates.lat}, ${city.coordinates.lng})">
                        Zoom Here
                    </button>
                </div>
            `;
            
            marker.bindPopup(popupContent);
            this.nearestCitiesLayer.addLayer(marker);
        });
        
        // Fit map to show search point and results
        if (cities.length > 0) {
            const group = new L.featureGroup([
                this.searchMarker,
                ...this.nearestCitiesLayer.getLayers()
            ]);
            this.map.fitBounds(group.getBounds().pad(0.1));
        }
    }
    
    getNumberedIcon(number) {
        return L.divIcon({
            className: 'numbered-marker',
            html: `<div class="marker-number">${number}</div>`,
            iconSize: [30, 30],
            iconAnchor: [15, 15]
        });
    }
    
    updateResultsPanel(data) {
        // Create or update results panel
        let resultsPanel = document.getElementById('proximity-results');
        if (!resultsPanel) {
            resultsPanel = document.createElement('div');
            resultsPanel.id = 'proximity-results';
            resultsPanel.className = 'proximity-results-panel';
            document.body.appendChild(resultsPanel);
        }
        
        resultsPanel.innerHTML = `
            <div class="card">
                <div class="card-header">
                    <h5>Nearest Cities Results</h5>
                    <button type="button" class="btn-close" onclick="proximitySearch.clearProximityResults()"></button>
                </div>
                <div class="card-body">
                    <p><strong>Search Point:</strong> ${data.search_point.lat.toFixed(4)}, ${data.search_point.lng.toFixed(4)}</p>
                    <p><strong>Cities Found:</strong> ${data.total_found}</p>
                    <div class="results-list">
                        ${data.nearest_cities.map(city => `
                            <div class="result-item" onclick="proximitySearch.zoomToCity(${city.coordinates.lat}, ${city.coordinates.lng})">
                                <strong>#${city.rank} ${city.name}, ${city.country}</strong><br>
                                <small>${city.distance_km} km away • Population: ${city.population.toLocaleString()}</small>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
        
        resultsPanel.style.display = 'block';
    }
    
    zoomToCity(lat, lng) {
        this.map.setView([lat, lng], 12);
    }
    
    clearProximityResults() {
        if (this.searchMarker) {
            this.map.removeLayer(this.searchMarker);
            this.searchMarker = null;
        }
        
        this.nearestCitiesLayer.clearLayers();
        
        if (this.radiusCircle) {
            this.map.removeLayer(this.radiusCircle);
            this.radiusCircle = null;
        }
        
        const resultsPanel = document.getElementById('proximity-results');
        if (resultsPanel) {
            resultsPanel.style.display = 'none';
        }
    }
}

