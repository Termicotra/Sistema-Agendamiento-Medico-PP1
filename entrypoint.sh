#!/bin/bash
# Fail on error
set -e

# Run migrations
echo "Running Django migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn main.wsgi:application --bind 0.0.0.0:8000
