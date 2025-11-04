# Deployment Guide

## Prerequisites
- Ubuntu 20.04+ server
- Domain name pointing to your server
- SSH access to server

## Installation Steps

### 1. Server Setup
```bash
sudo apt update
sudo apt install nginx postgresql postgresql-contrib postgis
sudo systemctl enable nginx postgresql
2. Database Setup
sudo -u postgres createuser --interactive webmapping
sudo -u postgres createdb webmapping_production
sudo -u postgres psql -d webmapping_production -c "CREATE EXTENSION postgis;"
3. Application Deployment
git clone [your-repository-url]
cd webmapping_project
pip install -r requirements.txt
python manage.py migrate --settings=webmapping_project.settings_production
python manage.py collectstatic --settings=webmapping_project.settings_production
4. Nginx Configuration
Create /etc/nginx/sites-available/webmapping:
server {
    listen 80;
    server_name your-domain.com;
    
    location /static/ {
        alias /var/www/webmapping/static/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
5. Process Management
# Install gunicorn
pip install gunicorn

# Create systemd service
sudo nano /etc/systemd/system/webmapping.service
[Unit]
Description=WebMapping Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/webmapping_project
ExecStart=/path/to/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 webmapping_project.wsgi:application

[Install]
WantedBy=multi-user.target
sudo systemctl enable webmapping
sudo systemctl start webmapping
```
