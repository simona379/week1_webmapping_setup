import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
# GDAL and PROJ libraries for GeoDjango
#GDAL_LIBRARY_PATH = '/opt/homebrew/opt/gdal/lib/libgdal.dylib'
#GEOS_LIBRARY_PATH = '/opt/homebrew/opt/geos/lib/libgeos_c.dylib'
#PROJ_LIBRARY_PATH = '/opt/homebrew/opt/proj/lib/libproj.dylib'

# GeoDjango: shared libs
GDAL_LIBRARY_PATH = "/usr/local/opt/gdal/lib/libgdal.dylib"
GEOS_LIBRARY_PATH = "/usr/local/opt/geos/lib/libgeos_c.dylib"

# GDAL/PROJ data directories (env vars — Django doesn't have settings for these)
os.environ.setdefault("GDAL_DATA", "/usr/local/opt/gdal/share/gdal")
os.environ.setdefault("PROJ_LIB", "/usr/local/opt/proj/share/proj")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your-secret-key-here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # GeoDjango
    'django.contrib.gis',
    
    # Third party
    'rest_framework',
    'rest_framework_gis',
    'django_filters',
    'corsheaders',
    'drf_spectacular',
    
    # Local apps
    'maps', # From Week 1
    'spatial_data_app', # From Week 2
    'cities_api',  # New API app for week 3
    'cities', # app from Week 4
    'cities_query', #Week 5
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webmapping_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'webmapping_project.wsgi.application'

# Database configuration for PostGIS
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'webmapping_db',
        'USER': 'webmapping',
        'PASSWORD': 'awm123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Open for development
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True # Only for development
CORS_ALLOW_CREDENTIALS = True 

# API Documentation
SPECTACULAR_SETTINGS = {
    'TITLE': 'Cities API',
    'DESCRIPTION': 'RESTful API for city data with spatial capabilities',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

