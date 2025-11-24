#!/bin/bash

# Script de inicio para Railway
set -e  # Detener si hay errores

echo "========================================"
echo "Iniciando aplicación Django en Railway"
echo "========================================"

# Verificar que DATABASE_URL existe
if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL no está configurada"
    exit 1
fi

echo "✓ DATABASE_URL detectada"

# Ejecutar migraciones
echo "Ejecutando migraciones..."
python manage.py migrate --noinput

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Crear superusuario si no existe (opcional)
# python manage.py createsuperuser --noinput --username admin --email admin@example.com || true

echo "✓ Preparación completada"
echo "Iniciando servidor Gunicorn..."

# Iniciar Gunicorn
exec gunicorn main.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
