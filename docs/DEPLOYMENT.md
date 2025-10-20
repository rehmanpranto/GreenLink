# GreenLink Deployment Guide

## 🚀 Production Deployment Overview

This guide covers deploying GreenLink to production environments, including cloud platforms, server configurations, and best practices for scalability and security.

## 🏗️ Deployment Architecture Options

### Option 1: Traditional VPS/Server Deployment
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Nginx       │    │    Gunicorn     │    │   PostgreSQL    │
│                 │    │                 │    │                 │
│ - Reverse Proxy │◄──►│ - Django App    │◄──►│ - Database      │
│ - Static Files  │    │ - Multiple      │    │ - Redis Cache   │
│ - SSL/TLS       │    │   Workers       │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Option 2: Containerized Deployment (Docker)
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Load Balancer  │    │ Docker Compose  │    │   Cloud Storage │
│                 │    │                 │    │                 │
│ - Nginx/Traefik │◄──►│ - Django        │◄──►│ - Media Files   │
│ - SSL Termination│    │ - PostgreSQL    │    │ - Backups       │
│                 │    │ - Redis         │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Option 3: Cloud Platform Deployment (Heroku/DigitalOcean App Platform)
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CDN/Cloud     │    │  Platform as    │    │   Managed       │
│                 │    │   a Service     │    │   Database      │
│ - Static Files  │◄──►│ - Auto Scaling  │◄──►│ - PostgreSQL    │
│ - Media Files   │    │ - Load Balancer │    │ - Automated     │
│ - SSL/TLS       │    │ - Health Checks │    │   Backups       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Pre-Deployment Setup

### Environment Configuration

1. **Create Production Settings**
   ```python
   # green_university_campus/settings/production.py
   from .base import *
   import os
   from decouple import config
   
   # Security Settings
   DEBUG = False
   SECRET_KEY = config('SECRET_KEY')
   ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
   
   # Database Configuration
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': config('DB_NAME'),
           'USER': config('DB_USER'),
           'PASSWORD': config('DB_PASSWORD'),
           'HOST': config('DB_HOST', default='localhost'),
           'PORT': config('DB_PORT', default='5432'),
           'OPTIONS': {
               'sslmode': 'require',
           },
       }
   }
   
   # Static Files
   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
   
   # Media Files (Cloud Storage)
   DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
   AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
   AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
   AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
   AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
   
   # Security Headers
   SECURE_SSL_REDIRECT = True
   SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
   SECURE_HSTS_SECONDS = 31536000
   SECURE_HSTS_INCLUDE_SUBDOMAINS = True
   SECURE_HSTS_PRELOAD = True
   SECURE_CONTENT_TYPE_NOSNIFF = True
   SECURE_BROWSER_XSS_FILTER = True
   X_FRAME_OPTIONS = 'DENY'
   
   # Session Security
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   SESSION_COOKIE_HTTPONLY = True
   CSRF_COOKIE_HTTPONLY = True
   
   # Cache Configuration
   CACHES = {
       'default': {
           'BACKEND': 'django_redis.cache.RedisCache',
           'LOCATION': config('REDIS_URL'),
           'OPTIONS': {
               'CLIENT_CLASS': 'django_redis.client.DefaultClient',
           }
       }
   }
   
   # Logging
   LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'formatters': {
           'verbose': {
               'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
               'style': '{',
           },
       },
       'handlers': {
           'file': {
               'level': 'INFO',
               'class': 'logging.handlers.RotatingFileHandler',
               'filename': '/var/log/greenlink/django.log',
               'maxBytes': 15728640,  # 15MB
               'backupCount': 10,
               'formatter': 'verbose',
           },
           'console': {
               'level': 'INFO',
               'class': 'logging.StreamHandler',
               'formatter': 'verbose',
           },
       },
       'root': {
           'handlers': ['console', 'file'],
           'level': 'INFO',
       },
   }
   ```

2. **Update Requirements for Production**
   ```txt
   # requirements/production.txt
   -r base.txt
   
   # Production Server
   gunicorn==21.2.0
   
   # Database
   psycopg2-binary==2.9.7
   
   # Cache
   django-redis==5.3.0
   redis==4.6.0
   
   # Storage
   django-storages==1.14.2
   boto3==1.28.57
   
   # Monitoring
   sentry-sdk==1.32.0
   
   # Security
   django-environ==0.11.2
   ```

3. **Environment Variables Template (.env.production)**
   ```env
   # Django Settings
   SECRET_KEY=your-super-secret-production-key-here
   DEBUG=False
   ALLOWED_HOSTS=greenlink.green.edu.bd,www.greenlink.green.edu.bd
   
   # Database
   DB_NAME=greenlink_production
   DB_USER=greenlink_user
   DB_PASSWORD=super_secure_db_password
   DB_HOST=localhost
   DB_PORT=5432
   
   # Cache
   REDIS_URL=redis://localhost:6379/1
   
   # AWS S3 (for media files)
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_STORAGE_BUCKET_NAME=greenlink-media
   AWS_S3_REGION_NAME=us-east-1
   
   # Email (for password resets)
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=noreply@green.edu.bd
   EMAIL_HOST_PASSWORD=email_app_password
   
   # Monitoring
   SENTRY_DSN=https://your-sentry-dsn-here
   ```

## 🐧 Linux Server Deployment (Ubuntu 22.04)

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y postgresql postgresql-contrib
sudo apt install -y nginx
sudo apt install -y redis-server
sudo apt install -y git
sudo apt install -y supervisor
```

### 2. Database Setup

```bash
# Create PostgreSQL database and user
sudo -u postgres psql

CREATE DATABASE greenlink_production;
CREATE USER greenlink_user WITH PASSWORD 'super_secure_db_password';
ALTER ROLE greenlink_user SET client_encoding TO 'utf8';
ALTER ROLE greenlink_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE greenlink_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE greenlink_production TO greenlink_user;
\q
```

### 3. Application Deployment

```bash
# Create application user
sudo adduser --system --group --home /opt/greenlink greenlink

# Clone repository
sudo -u greenlink git clone https://github.com/rehmanpranto/GreenLink.git /opt/greenlink/app
cd /opt/greenlink/app

# Create virtual environment
sudo -u greenlink python3 -m venv /opt/greenlink/venv

# Install dependencies
sudo -u greenlink /opt/greenlink/venv/bin/pip install -r requirements/production.txt

# Copy environment file
sudo -u greenlink cp .env.production /opt/greenlink/.env

# Collect static files
sudo -u greenlink /opt/greenlink/venv/bin/python manage.py collectstatic --noinput --settings=green_university_campus.settings.production

# Run migrations
sudo -u greenlink /opt/greenlink/venv/bin/python manage.py migrate --settings=green_university_campus.settings.production

# Create superuser
sudo -u greenlink /opt/greenlink/venv/bin/python manage.py createsuperuser --settings=green_university_campus.settings.production
```

### 4. Gunicorn Configuration

```bash
# Create Gunicorn configuration
sudo tee /opt/greenlink/gunicorn.conf.py > /dev/null <<EOF
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
reload = False
daemon = False
user = "greenlink"
group = "greenlink"
pidfile = "/opt/greenlink/gunicorn.pid"
accesslog = "/var/log/greenlink/gunicorn-access.log"
errorlog = "/var/log/greenlink/gunicorn-error.log"
loglevel = "info"
EOF

# Create log directory
sudo mkdir -p /var/log/greenlink
sudo chown greenlink:greenlink /var/log/greenlink
```

### 5. Supervisor Configuration

```bash
# Create supervisor configuration
sudo tee /etc/supervisor/conf.d/greenlink.conf > /dev/null <<EOF
[program:greenlink]
command=/opt/greenlink/venv/bin/gunicorn --config /opt/greenlink/gunicorn.conf.py green_university_campus.wsgi:application
directory=/opt/greenlink/app
user=greenlink
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/greenlink/supervisor.log
environment=DJANGO_SETTINGS_MODULE="green_university_campus.settings.production"
EOF

# Update supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start greenlink
```

### 6. Nginx Configuration

```bash
# Create Nginx configuration
sudo tee /etc/nginx/sites-available/greenlink > /dev/null <<'EOF'
upstream greenlink_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name greenlink.green.edu.bd www.greenlink.green.edu.bd;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name greenlink.green.edu.bd www.greenlink.green.edu.bd;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/greenlink.green.edu.bd/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/greenlink.green.edu.bd/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # Security Headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # File Upload Limit
    client_max_body_size 10M;
    
    # Static Files
    location /static/ {
        alias /opt/greenlink/app/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Media Files (if not using S3)
    location /media/ {
        alias /opt/greenlink/app/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
    
    # Main Application
    location / {
        proxy_pass http://greenlink_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
    
    # Health Check
    location /health/ {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/greenlink /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 7. SSL Certificate Setup (Let's Encrypt)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d greenlink.green.edu.bd -d www.greenlink.green.edu.bd

# Test automatic renewal
sudo certbot renew --dry-run
```

## 🐳 Docker Deployment

### 1. Dockerfile

```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=green_university_campus.settings.production

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create application user
RUN addgroup --system django \
    && adduser --system --ingroup django django

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements/production.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Change ownership
RUN chown -R django:django /app

# Switch to non-root user
USER django

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Start server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "green_university_campus.wsgi:application"]
```

### 2. Docker Compose

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      POSTGRES_DB: greenlink_production
      POSTGRES_USER: greenlink_user
      POSTGRES_PASSWORD: super_secure_db_password
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U greenlink_user -d greenlink_production"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  web:
    build: .
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    environment:
      - DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
      - DB_NAME=greenlink_production
      - DB_USER=greenlink_user
      - DB_PASSWORD=super_secure_db_password
      - DB_HOST=db
      - DB_PORT=5432
      - REDIS_URL=redis://redis:6379/1
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: unless-stopped

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### 3. Production Docker Commands

```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d --build

# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Update application
git pull
docker-compose -f docker-compose.prod.yml up -d --build
```

## ☁️ Cloud Platform Deployment

### Heroku Deployment

1. **Prepare for Heroku**
   ```python
   # Procfile
   release: python manage.py migrate
   web: gunicorn green_university_campus.wsgi:application --log-file -
   ```

   ```python
   # runtime.txt
   python-3.11.6
   ```

2. **Heroku Configuration**
   ```bash
   # Install Heroku CLI and login
   heroku login
   
   # Create application
   heroku create greenlink-app
   
   # Add PostgreSQL
   heroku addons:create heroku-postgresql:mini
   
   # Add Redis
   heroku addons:create heroku-redis:mini
   
   # Set environment variables
   heroku config:set SECRET_KEY="your-secret-key"
   heroku config:set DEBUG=False
   heroku config:set DJANGO_SETTINGS_MODULE=green_university_campus.settings.production
   
   # Deploy
   git push heroku main
   
   # Run commands
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

### DigitalOcean App Platform

```yaml
# .do/app.yaml
name: greenlink
services:
- name: web
  source_dir: /
  github:
    repo: rehmanpranto/GreenLink
    branch: main
    deploy_on_push: true
  run_command: gunicorn --worker-tmp-dir /dev/shm green_university_campus.wsgi:application
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: DEBUG
    value: "False"
  - key: DJANGO_SETTINGS_MODULE
    value: green_university_campus.settings.production
  - key: SECRET_KEY
    value: your-secret-key
    type: SECRET
  - key: DATABASE_URL
    type: SECRET
    scope: RUN_AND_BUILD_TIME
databases:
- name: greenlink-db
  engine: PG
  num_nodes: 1
  size: db-s-dev-database
  version: "14"
```

## 📊 Monitoring and Maintenance

### 1. Health Checks

```python
# health/views.py
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import redis

def health_check(request):
    """Health check endpoint for load balancers."""
    checks = {
        'database': False,
        'cache': False,
        'status': 'unhealthy'
    }
    
    try:
        # Database check
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        checks['database'] = True
    except Exception:
        pass
    
    try:
        # Cache check
        cache.set('health_check', 'ok', timeout=10)
        checks['cache'] = cache.get('health_check') == 'ok'
    except Exception:
        pass
    
    if checks['database'] and checks['cache']:
        checks['status'] = 'healthy'
        return JsonResponse(checks, status=200)
    else:
        return JsonResponse(checks, status=503)
```

### 2. Monitoring with Sentry

```python
# settings/production.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

sentry_sdk.init(
    dsn=config('SENTRY_DSN'),
    integrations=[
        DjangoIntegration(
            transaction_style='url',
            middleware_spans=True,
            signals_spans=True,
            cache_spans=True,
        ),
        RedisIntegration(),
    ],
    traces_sample_rate=0.1,
    send_default_pii=True,
    environment='production',
)
```

### 3. Backup Scripts

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups/greenlink"
S3_BUCKET="greenlink-backups"

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup
pg_dump -h localhost -U greenlink_user -d greenlink_production \
    | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Media files backup (if not using S3)
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz /opt/greenlink/app/media/

# Upload to S3
aws s3 sync $BACKUP_DIR s3://$S3_BUCKET/

# Clean old local backups (keep 7 days)
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

### 4. Log Rotation

```bash
# /etc/logrotate.d/greenlink
/var/log/greenlink/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 greenlink greenlink
    postrotate
        supervisorctl restart greenlink
    endscript
}
```

## 🔒 Security Checklist

- [ ] HTTPS enabled with valid SSL certificate
- [ ] Security headers properly configured
- [ ] Database credentials secured
- [ ] Secret key rotated and secured
- [ ] Debug mode disabled
- [ ] Admin panel secured (custom URL)
- [ ] File upload restrictions in place
- [ ] Rate limiting configured
- [ ] Regular security updates applied
- [ ] Backup strategy implemented
- [ ] Monitoring and alerting configured

## 📈 Performance Optimization

### Database Optimization
```sql
-- Add missing indexes
CREATE INDEX CONCURRENTLY idx_post_created_at ON social_post(created_at DESC);
CREATE INDEX CONCURRENTLY idx_message_conversation ON chat_message(sender_id, receiver_id, timestamp);

-- Update statistics
ANALYZE;
```

### Caching Strategy
```python
# Cache frequently accessed data
from django.core.cache import cache

def get_user_stats(user_id):
    cache_key = f'user_stats_{user_id}'
    stats = cache.get(cache_key)
    if not stats:
        stats = calculate_stats(user_id)
        cache.set(cache_key, stats, timeout=3600)  # 1 hour
    return stats
```

---

This deployment guide provides comprehensive instructions for deploying GreenLink to production environments with proper security, monitoring, and maintenance procedures.
