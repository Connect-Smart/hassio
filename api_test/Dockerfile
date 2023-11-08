# Gebruik de officiële Home Assistant add-on basisimage als basis
FROM homeassistant/amd64-base:3.13

# Kopieer de benodigde bestanden naar de container
COPY main.py /app/main.py
COPY config.json /data/config.json
COPY logo.png /data/logo.png
COPY web /data/web

# Installeer eventuele extra afhankelijkheden
RUN pip install aiohttp

# Definieer de opstartopdracht
CMD [ "python", "/app/main.py" ]
