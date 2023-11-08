# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM
FROM python:3.9-slim

# Copy root filesystem
COPY rootfs /



COPY run.py /run.py

CMD ["python3", "/run.py"]
