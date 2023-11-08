# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Installeer afhankelijkheden en tools indien nodig
# RUN apt-get update && apt-get install -y <jouw-pakketten> && rm -rf /var/lib/apt/lists/*

FROM python:3.9-slim

# Kopieer de Python requirements file
COPY requirements.txt /requirements.txt

# Installeer Python dependencies
RUN pip install --no-cache-dir -r /requirements.txt

# Kopieer root filesystem
COPY rootfs /

# Kopieer het Python script
COPY run.py /run.py

# Stel het commando in om je script te starten
CMD ["python3", "/run.py"]