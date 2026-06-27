#!/usr/bin/env bash
set -e

echo "🚀 Starting Render deployment..."

# Change to Django project directory
cd fagierrandsbackup

# Start gunicorn
exec gunicorn fagierrandsbackup.wsgi:application --bind 0.0.0.0:$PORT
