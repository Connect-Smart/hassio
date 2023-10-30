#!/bin/bash

CONFIG_PATH=/data/options.json

HA_TOKEN=$(jq --raw-output ".token" $CONFIG_PATH)
ENTITY=$(jq --raw-output ".entity" $CONFIG_PATH)
API_KEY=$(jq --raw-output ".apikey" $CONFIG_PATH)

ENTITY_ID="sensor.$ENTITY"  # Vervang dit door het gewenste entiteits-ID
REMOTE_API_URL="https://www.voxip.nl/api/"
INTERVAL=5  # Tijd in seconden tussen elk API-verzoek

# Instellingen
HA_HOST="http://localhost:8123"  # Vervang dit door het adres van jouw Home Assistant

EXISTING_ENTITY=$(curl -s -X GET -H "Authorization: Bearer $HA_TOKEN" \
     -H "Content-Type: application/json" \
     "$HA_HOST/api/states/$ENTITY_ID")

# Als de entiteit al bestaat, werk deze dan bij
if [[ ! -z "$EXISTING_ENTITY" ]]; then
    # De waarde die je wilt instellen
    NEW_VALUE="40"

    # API-aanroep om de entiteit bij te werken
    curl -s -X POST -H "Authorization: Bearer $HA_TOKEN" \
         -H "Content-Type: application/json" \
         -d "{\"state\": \"$NEW_VALUE\"}" \
         "$HA_HOST/api/states/$ENTITY_ID"

    echo "Entiteit $ENTITY_ID bijgewerkt naar $NEW_VALUE"
else
    # De configuratie voor de nieuwe entiteit
    ENTITY_CONFIG='{
      "platform": "template",
      "sensors": {
        "test": {
          "value_template": "{{ states.sensor.some_other_sensor.state }}"
        }
      }
    }'

    # API-aanroep om de configuratie toe te voegen
    RESPONSE=$(curl -s -X POST -H "Authorization: Bearer $HA_TOKEN" \
         -H "Content-Type: application/json" \
         -d "$ENTITY_CONFIG" \
         -w "%{http_code}" \
         -o /dev/null \
         "$HA_HOST/api/config/config_entries/entry_id/options")

    if [[ "$RESPONSE" == "403" ]]; then
        echo "403 Forbidden. Stopping the addon."
        core stop
    else
        echo "Nieuwe entiteit toegevoegd aan Home Assistant configuratie"
    fi
fi

perform_api_request() {
    # Plaats hier je API-aanroep
    # Bijvoorbeeld, een API-aanroep om de waarde van een entiteit op te halen
     REMOTE_DATA=$(curl -s "$REMOTE_API_URL")

    RESPONSE=$(curl -X POST -H "Authorization: Bearer $HA_TOKEN" \
         -H "Content-Type: application/json" \
         -d "{\"state\": \"$REMOTE_DATA\"}" \
         -w "%{http_code}" \
         -o /dev/null \
         "$HA_HOST/api/states/$ENTITY_ID")

    if [[ "$RESPONSE" == "403" ]]; then
        echo "403 Forbidden. Stopping the addon."
        core stop
    else
        echo "Entiteit $ENTITY_ID bijgewerkt naar $REMOTE_DATA"
    fi
}

# Start de lus
while true; do
    # Voer de API-aanroep uit
    perform_api_request

    # Wacht het opgegeven interval voordat de lus opnieuw wordt uitgevoerd
    sleep $INTERVAL
done