#!/bin/bash

CONFIG_PATH=/data/options.json

HA_TOKEN=$(jq --raw-output ".token" $CONFIG_PATH)
ENTITY_ID=$(jq --raw-output ".entity" $CONFIG_PATH)
API_KEY=$(jq --raw-output ".apikey" $CONFIG_PATH)

ENTITY_ID="sensor.energie_prijzen_CS"  # Vervang dit door het gewenste entiteits-ID
REMOTE_API_URL="https://www.voxip.nl/api/"
INTERVAL=5  # Tijd in seconden tussen elk API-verzoek
NEW_VALUE="0"
WEB_PORT="8099"                  # Luisterpoort voor de webserver

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

mkdir www
mkdir -p /etc/nginx/conf.d
chmod 777 www
chmod 777 /etc/nginx
chmod 777 /etc/nginx/conf.d

# Maak een eenvoudige HTML-pagina met de entiteitswaarde
cat <<EOF > /www/index.html
<!DOCTYPE html>
<html>
<body>
<h2 id="entityName">Loading...</h2>
<h2 id="entityValue">Loading...</h2>
<script>
  const entityNameElement = document.getElementById("entityName");
  const entityValueElement = document.getElementById("entityValue");

  // WebSocket-verbinding met Home Assistant
  const socket = new WebSocket("ws://localhost:8123/api/websocket");

  // Luister naar updates van de entiteit
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.event_type === "state_changed" && data.data.entity_id === "sensor.energie_prijzen_CS") {
      const newState = data.data.new_state;
      entityNameElement.textContent = newState.attributes.friendly_name;
      entityValueElement.textContent = newState.state;
    }
  };
</script>
</body>
</html>
EOF

apk add nginx

# Configureer de webserver
#echo "daemon off;" >> /etc/nginx/nginx.conf
echo "error_log /dev/stdout info;" >> /etc/nginx/nginx.conf

#cat /etc/nginx/nginx.conf

# Maak een Nginx-configuratiebestand voor de webpagina
cat <<EOF > /etc/nginx/http.d/default.conf
server {
    listen       $WEB_PORT;
    server_name  localhost;

    location / {
        root   /www;
        index  index.html;
    }
    error_page 404 /index.html;
    location = /index.html {
            root /www;
            internal;
    }

}
EOF

# Start Nginx
nginx



# Start de lus
while true; do
    # Wacht het opgegeven interval voordat de lus opnieuw wordt uitgevoerd
    sleep $INTERVAL

    # Voer de API-aanroep uit
    perform_api_request

done