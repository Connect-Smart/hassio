#!/bin/bash

CONFIG_PATH=/data/options.json

HA_TOKEN=$(jq --raw-output ".token" $CONFIG_PATH)
ENTITY_ID=$(jq --raw-output ".entity" $CONFIG_PATH)
API_KEY=$(jq --raw-output ".apikey" $CONFIG_PATH)

#ENTITY_ID="sensor.$ENTITY"  # Vervang dit door het gewenste entiteits-ID
REMOTE_API_URL="https://www.voxip.nl/api/"
INTERVAL=5  # Tijd in seconden tussen elk API-verzoek
NEW_VALUE="20"

# Instellingen
HA_HOST="http://localhost:8123"  # Vervang dit door het adres van jouw Home Assistant

curl -X POST -H "Authorization: Bearer $HA_TOKEN" \
     -H "Content-Type: application/json" \
     -d "{
       \"state\": \"29\",
       \"attributes\": {
         \"friendly_name\": \"test123\"
       }
     }" \
     "$HA_HOST/api/states/$ENTITY_ID"

perform_api_request() {
    # Bijvoorbeeld, een API-aanroep om de waarde van een entiteit op te halen
    REMOTE_DATA=$(curl "$REMOTE_API_URL")

    # API-aanroep om de entiteit bij te werken
    curl -X POST -H "Authorization: Bearer $HA_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"state\": \"$REMOTE_DATA\"}" \
        "$HA_HOST/api/states/$ENTITY_ID"

    echo "Entiteit $ENTITY_ID bijgewerkt naar $REMOTE_DATA"
}

# Start de lus
while true; do
    # Voer de API-aanroep uit
    perform_api_request

    # Wacht het opgegeven interval voordat de lus opnieuw wordt uitgevoerd
    sleep $INTERVAL
done