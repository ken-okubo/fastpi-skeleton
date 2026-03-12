#!/bin/bash
# Script de inicializacao para Railway / producao
# Suporta multiplos processos via PROCESS_TYPE

set -e

echo "Starting application..."
echo "Environment: ${RAILWAY_ENVIRONMENT:-local}"
echo "Process Type: ${PROCESS_TYPE:-web}"

# Detecta se estamos no Railway
if [ -n "$DATABASE_URL" ]; then
    echo "Railway detected (DATABASE_URL present)"

    # Roda migrations (apenas no processo web)
    if [ "$PROCESS_TYPE" = "web" ] || [ -z "$PROCESS_TYPE" ]; then
        echo "Running database migrations..."
        alembic upgrade head
    fi
fi

# Inicia o processo apropriado
case "${PROCESS_TYPE:-web}" in
    web)
        echo "Starting web server on port ${PORT:-8000}..."
        exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
        ;;
    worker)
        echo "Starting worker..."
        exec python worker.py
        ;;
    *)
        echo "Unknown PROCESS_TYPE: $PROCESS_TYPE"
        echo "Valid options: web, worker"
        exit 1
        ;;
esac
