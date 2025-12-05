#!/bin/bash
set -e

echo "Starting Django container..."

# Esperar a que la base de datos esté disponible
echo "Waiting for database..."
until python manage.py showmigrations >/dev/null 2>&1; do
    sleep 1
done

echo "Running Django migrations..."
python manage.py makemigrations --merge || true
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Arrancar Gunicorn en el puerto que da Railway
echo "Starting Gunicorn..."
exec gunicorn main.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --log-level info
