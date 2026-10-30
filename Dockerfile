FROM python:3.12-slim-trixie

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# The converter is only as faithful as the faces it can see and the Impress that reads the deck: this
# distribution carries LibreOffice 25.2, and the fonts below are what the worship decks are set in
# (spec 166). trixie, not bookworm, for the version: bookworm's 7.4 re-wraps the tables it converts.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq5 \
        libreoffice-impress \
        fonts-liberation \
        fonts-liberation-sans-narrow \
        fonts-crosextra-carlito \
        fonts-crosextra-caladea \
        fonts-noto-core \
        util-linux \
    && rm -rf /var/lib/apt/lists/*

COPY docker/slides-fonts.conf /etc/fonts/conf.d/99-gkps-slides.conf
RUN fc-cache -f

# requirements-dev.txt starts with `-r requirements.txt`; the image is a local
# development environment, so the dev extras (test tooling) are installed too.
COPY requirements.txt requirements-dev.txt ./

RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

# A monospaced fallback is a silent re-wrap of every slide, so the build refuses one.
RUN python -m multimedia.slide_fonts

RUN chmod +x docker/entrypoint.sh

EXPOSE 8000
EXPOSE 63174

ENTRYPOINT ["/bin/sh", "docker/entrypoint.sh"]
CMD ["gunicorn", "multimedia.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
