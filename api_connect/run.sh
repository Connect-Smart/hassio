#!/bin/bash

# Inclusie van Bashio-configuratie
source /config/bashio/config.json

# Haal de toegangstoken op uit Bashio
TOKEN=$(bashio::config 'homeassistant.api_token')

# URL voor de Home Assistant RESTful API
API_URL="http://homeassistant.local:8123/api"

# Schakel een specifieke schakelaar in (verander deze naar de gewenste entity_id)
ENTITY_ID="switch.my_switch"

# Aanroepen van de Home Assistant API om de schakelaar in te schakelen
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
     -d '{"entity_id": "'$ENTITY_ID'"}' \
     $API_URL/services/switch/turn_on
