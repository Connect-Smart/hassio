#!/bin/bash
set -e

# Vervang 'your_entity_id' door de gewenste entiteit-id en 'your_value' door de gewenste waarde.
ENTITY_ID="your_entity_id"
NEW_VALUE="your_value"

# Activeer de virtuele omgeving van Home Assistant.
source /config/homeassistant/.venv/bin/activate

# Roep de Home Assistant-service aan om een nieuwe waarde in te stellen voor de entiteit.
echo "Stel de waarde $NEW_VALUE in voor entiteit $ENTITY_ID"
hass-cli service call homeassistant/update_entity -d '{
  "entity_id": "'$ENTITY_ID'",
  "state": "'$NEW_VALUE'"
}'