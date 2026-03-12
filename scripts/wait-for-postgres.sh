#!/bin/sh
# Script para Docker local - aguarda PostgreSQL e roda migrations
set -e

cd /app

host="db"
echo "Waiting for PostgreSQL at $host..."

until PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$host" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' >/dev/null 2>&1; do
  echo "PostgreSQL not ready at $host, waiting..."
  sleep 2
done

echo "PostgreSQL is up at $host!"
echo "Running migrations..."
alembic upgrade head

echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
