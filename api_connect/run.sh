#!/bin/bash

CONFIG_PATH=/data/options.json

HA_TOKEN=$(jq --raw-output ".token" $CONFIG_PATH)
ENTITY_ID=$(jq --raw-output ".entity" $CONFIG_PATH)

# Instellingen
HA_HOST="http://localhost:8123"  # Vervang dit door het adres van jouw Home Assistant

# De waarde die je wilt instellen
NEW_VALUE="42"

# API-aanroep om de entiteit bij te werken
curl -X POST -H "Authorization: Bearer $HA_TOKEN" \
     -H "Content-Type: application/json" \
     -d "{\"state\": \"$NEW_VALUE\"}" \
     "$HA_HOST/api/states/$ENTITY_ID"

echo "Entiteit $ENTITY_ID bijgewerkt naar $NEW_VALUE"