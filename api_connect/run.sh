#!/bin/bash

CONFIG_PATH=/data/options.json

HA_TOKEN=$(jq --raw-output ".token" $CONFIG_PATH)
ENTITY_ID=$(jq --raw-output ".entity" $CONFIG_PATH)
API_KEY=$(jq --raw-output ".apikey" $CONFIG_PATH)

ENTITY_ID="sensor.energie_prijzen_CS"  # Vervang dit door het gewenste entiteits-ID
REMOTE_API_URL="https://www.voxip.nl/api/"
INTERVAL=5  # Tijd in seconden tussen elk API-verzoek
NEW_VALUE="0"
PAGE_CONTENT="<!DOCTYPE html><html><head><title>Entity Viewer</title></head><body><h1>Entity Viewer</h1><p>Entity: $ENTITY_ID</p><iframe src=\"$HA_HOST/lovelace/0\" width=\"800\" height=\"600\"></iframe></body></html>"
# Start een eenvoudige webserver om de pagina weer te geven
mkdir www
chmod 777 www
echo -e "$PAGE_CONTENT" > /www/index.html

# Instellingen
HA_HOST="http://localhost:8123"  # Vervang dit door het adres van jouw Home Assistant

curl -s -X POST -H "Authorization: Bearer $HA_TOKEN" \
     -H "Content-Type: application/json" \
     -d "{
       \"state\": \"29\",
       \"attributes\": {
         \"friendly_name\": \"energie_prijzen\"
       }
     }" \
     "$HA_HOST/api/states/$ENTITY_ID"

perform_api_request() {
    # Bijvoorbeeld, een API-aanroep om de waarde van een entiteit op te halen
    REMOTE_DATA=$(curl "$REMOTE_API_URL")

    # API-aanroep om de entiteit bij te werken
    curl -s -X POST -H "Authorization: Bearer $HA_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"state\": \"$REMOTE_DATA\"}" \
        "$HA_HOST/api/states/$ENTITY_ID"

    echo "Entiteit $ENTITY_ID bijgewerkt naar $REMOTE_DATA"
}

python3 -m http.server --directory /www 8099


# Start de lus
while true; do
    # Wacht het opgegeven interval voordat de lus opnieuw wordt uitgevoerd
    sleep $INTERVAL

    # Voer de API-aanroep uit
    perform_api_request
done