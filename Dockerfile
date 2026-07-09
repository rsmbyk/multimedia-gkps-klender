FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# psycopg2 source builds are flaky on slim images; use the binary wheel instead.
RUN pip install --no-cache-dir psycopg2-binary==2.9.9 \
    && grep -v '^psycopg2==' requirements.txt > /tmp/requirements.txt \
    && pip install --no-cache-dir -r /tmp/requirements.txt

COPY . .

RUN chmod +x docker/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "docker/entrypoint.sh"]
CMD ["gunicorn", "multimedia.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
