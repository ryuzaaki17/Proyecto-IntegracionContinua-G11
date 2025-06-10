#!/bin/sh

echo "⏳ Esperando a que PostgreSQL esté disponible en flask_db:5432..."

while ! nc -z flask_db 5432; do
  sleep 1
done

echo "✅ PostgreSQL está listo. Iniciando Flask..."

exec flask run --host=0.0.0.0 --port=4000