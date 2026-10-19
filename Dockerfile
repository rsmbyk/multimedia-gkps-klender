FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq5 \
        libreoffice-impress \
        fonts-liberation \
        util-linux \
    && rm -rf /var/lib/apt/lists/*

# requirements-dev.txt starts with `-r requirements.txt`; the image is a local
# development environment, so the dev extras (test tooling) are installed too.
COPY requirements.txt requirements-dev.txt ./

RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

RUN chmod +x docker/entrypoint.sh

EXPOSE 8000
EXPOSE 63174

ENTRYPOINT ["/bin/sh", "docker/entrypoint.sh"]
CMD ["gunicorn", "multimedia.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
