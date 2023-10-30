#!/bin/bash

CONFIG_PATH=/data/options.json

HA_TOKEN=$(jq --raw-output ".token" $CONFIG_PATH)
ENTITY_ID=$(jq --raw-output ".entity" $CONFIG_PATH)

# Instellingen
HA_HOST="http://localhost:8123"  # Vervang dit door het adres van jouw Home Assistant

EXISTING_ENTITY=$(curl -s -X GET -H "Authorization: Bearer $HA_TOKEN" \
     -H "Content-Type: application/json" \
     "$HA_HOST/api/states/$ENTITY_ID")

# Als de entiteit al bestaat, werk deze dan bij
if [[ ! -z "$EXISTING_ENTITY" ]]; then
    # De waarde die je wilt instellen
    NEW_VALUE="42"

    # API-aanroep om de entiteit bij te werken
    curl -X POST -H "Authorization: Bearer $HA_TOKEN" \
         -H "Content-Type: application/json" \
         -d "{\"state\": \"$NEW_VALUE\"}" \
         "$HA_HOST/api/states/$ENTITY_ID"

    echo "Entiteit $ENTITY_ID bijgewerkt naar $NEW_VALUE"
else
    # De configuratie voor de nieuwe entiteit
    ENTITY_CONFIG='{
      "platform": "template",
      "sensors": {
        "example_sensor": {
          "value_template": "{{ states.sensor.some_other_sensor.state }}"
        }
      }
    }'

    # API-aanroep om de configuratie toe te voegen
    curl -X POST -H "Authorization: Bearer $HA_TOKEN" \
         -H "Content-Type: application/json" \
         -d "$ENTITY_CONFIG" \
         "$HA_HOST/api/config/config_entries/entry_id/options"

    echo "Nieuwe entiteit toegevoegd aan Home Assistant configuratie"
fi