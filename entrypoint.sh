#!/bin/bash
set -e

echo "📦 Esperando base de datos..."
for i in $(seq 1 30); do
  if python -c "import psycopg2, os; psycopg2.connect(os.environ.get('DATABASE_URL', 'sqlite:///tmp/test.db'))" 2>/dev/null; then
    break
  fi
  echo "  Intento $i/30..."
  sleep 3
done

echo "📦 Migrate..."
python manage.py migrate --noinput

echo "📦 Poblar cuartel..."
python manage.py poblar_cuartel || true

echo "📦 Crear cuentas..."
python manage.py crear_cuentas || true

echo "📦 Collectstatic..."
python manage.py collectstatic --noinput

echo "🚀 Iniciando servidor en puerto ${PORT:-8000}..."
exec gunicorn central_gestion.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3
