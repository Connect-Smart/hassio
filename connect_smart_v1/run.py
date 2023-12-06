import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Gebruik het interne token verkregen door de supervisor
HASS_TOKEN = os.getenv("SUPERVISOR_TOKEN")
HASS_API = "http://supervisor/core/api"
TEST_SENSOR_ENTITY_ID = "sensor.test_sensor"
WEBSITE_USERNAME = os.getenv("username")
WEBSITE_PASSWORD = os.getenv("password")

headers = {
    "Authorization": f"Bearer {HASS_TOKEN}",
    "Content-Type": "application/json",
}

def get_external_data():
    website_url = "https://voxip.nl/api/"
    response = requests.get(website_url)
    
    if response.ok:
        # Hier kun je de logica aanpassen om de benodigde gegevens uit de website te halen
        login_data = {"username": username, "password": password}
        external_data = requests.post(url, json=login_data)
        return external_data
    else:
        return None

def update_test_sensor(value):
    url = f"{HASS_API}/states/{TEST_SENSOR_ENTITY_ID}"
    data = {"state": value}
    
    response = requests.post(url, headers=headers, json=data)
    
    return response.ok

@app.route('/toggle-switch', methods=['POST'])
def toggle_switch():
    entity_id = "switch.jouw_switch_entity_id"
    url = f"{HASS_API}/services/switch/toggle"
    data = {"entity_id": entity_id}
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.ok:
        return "Switch toggled!", 200
    else:
        return "Failed to toggle switch.", 500

@app.route('/admin', methods=['GET'])
def get_test_sensor():
    # Haal gegevens van de externe website
    external_data = get_external_data()
    
    if external_data is not None:
        # Update de test sensor met de externe gegevens
        if update_test_sensor(external_data['desired_value']):
            return jsonify({"message": "Test sensor updated successfully"}), 200
        else:
            return "Failed to update test sensor.", 500
    else:
        return "Failed to retrieve external data.", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
