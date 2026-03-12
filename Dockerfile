FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app
ENV PORT=8000

COPY requirements.txt .
RUN apt-get update && apt-get install -y postgresql-client && apt-get clean
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Scripts para Railway (com DATABASE_URL) vs Docker local
COPY scripts/wait-for-postgres.sh /wait-for-postgres.sh
COPY scripts/start.sh /start.sh
RUN chmod +x /wait-for-postgres.sh /start.sh

# Railway: usa start.sh com DATABASE_URL
# Local: usa wait-for-postgres.sh (docker-compose)
CMD ["/bin/sh", "-c", "if [ -n \"$DATABASE_URL\" ]; then /start.sh; else /wait-for-postgres.sh; fi"]
