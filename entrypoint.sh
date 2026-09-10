#!/bin/bash
set -e

echo "⏳ Esperando a que la base de datos esté lista..."
until python -c "import psycopg2; psycopg2.connect('$DATABASE_URL')" 2>/dev/null; do
  sleep 2
done
echo "✅ Base de datos conectada."

echo "📦 Ejecutando migrate..."
python manage.py migrate --noinput

echo "📦 Poblando cuarteles..."
python manage.py poblar_cuartel

echo "📦 Creando cuentas..."
python manage.py crear_cuentas

echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "🚀 Iniciando servidor..."
exec gunicorn central_gestion.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3
