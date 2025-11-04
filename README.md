A Location-Based Services Web Application
Developed by Simona Petrauskaite (Student ID: C19343861)

** Screenshots available in documentation **

⸻

 Project Overview

This project demonstrates the development of a location-based services (LBS) web application using Django, Leaflet.js, and PostGIS.
It allows users to interactively explore and visualize spatial city data, perform proximity searches, and view information about different urban areas.

The application integrates:
	•	A PostgreSQL/PostGIS spatial database
	•	A Django REST API for spatial queries
	•	A responsive web interface with Leaflet maps
	•	Spatial functionality such as nearest cities and radius-based search

⸻

 Key Features

 Spatial Database Management
	•	PostgreSQL with PostGIS for storing and querying geographic data
	•	Spatial indexing and geometry support (points, polygons, etc.)

 REST API (Middle Tier)
	•	Developed with Django and Django REST Framework
	•	Endpoints for spatial queries:
	•	/query/api/nearest/ → Find nearest cities
	•	/query/api/radius/ → Find cities within a radius

 Interactive Map Interface
	•	Built with Leaflet.js and OpenStreetMap tiles
	•	Real-time map interactions:
	•	Click to search nearby cities
	•	View distances, city info, and popup details
	•	Proximity Search UI with “Nearest” and “Within Radius” modes

 Responsive Frontend
	•	Built using Bootstrap 5
	•	Works across desktop, tablet, and mobile devices

 Optional Next Step Cloud-Ready Architecture
	•	Can be containerized with Docker
	•	Configurable .env file for environment settings

⸻

 Tech Stack

Frontend
HTML, CSS (Bootstrap 5), JavaScript, Leaflet.js

Backend
Django 4.2, Django REST Framework, Django Leaflet
Technology

Database
PostgreSQL + PostGIS

Spatial Tools
GDAL, ogr2ogr

Version Control
Git + GitHub

Deployment (Local)
Python virtual environment

⸻

 Setup Instructions

1. Clone the Repository
git clone https://github.com/simona379/week1_webmapping_setup.git
cd week1_webmapping_setup

2. Set Up Virtual Environment
python3 -m venv webmapping_env
source webmapping_env/bin/activate

3. Install Dependencies
pip install -U pip
pip install -r requirements.txt

4. Configure Database

- Make sure PostgreSQL and PostGIS are installed:
brew install postgresql postgis

- Create a database:
psql -U postgres
CREATE DATABASE webmapping_db;
\c webmapping_db
CREATE EXTENSION postgis;

- Update settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'webmapping_db',
        'USER': 'postgres',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

5. Run Migrations and Start the Server

python manage.py makemigrations
python manage.py migrate
python manage.py runserver
Visit @ http://127.0.0.1:8000/

⸻

 Directory Structure

week1_webmapping_setup/
├── cities/                 # Core app (base models, data)
├── cities_api/             # REST API for city data
├── cities_query/           # Map + proximity search interface
├── spatial_data_app/       # PostGIS spatial model integration
├── static/                 # JS, CSS, Leaflet assets
├── templates/              # HTML templates (base, map, etc.)
├── webmapping_project/     # Django project config
├── webmapping_env/         # Virtual environment
├── requirements.txt
└── manage.py

⸻

 Spatial Queries Implemented
	1.	Nearest City Search — find 10 closest cities from a given coordinate.
	2.	Within Radius Search — list all cities within a user-defined radius (km).
	3.	Bounding Box Query (future work) — limit results within a visible map extent.

⸻

 Security Practices
	•	CSRF protection on all AJAX POST requests
	•	Secure environment variables using .env
	•	Django middleware for XSS and CSRF protection enabled

⸻

 Future Improvements
	•	Add user authentication for saved searches
	•	Deploy to cloud (Render / Railway / Docker)
	•	Add city comparison visualizations
	•	Integrate location autocomplete with Mapbox or Nominatim
