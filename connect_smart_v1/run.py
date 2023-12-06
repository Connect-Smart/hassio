import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Gebruik het interne token verkregen door de supervisor
HASS_TOKEN = os.getenv("SUPERVISOR_TOKEN")
HASS_API = "http://supervisor/core/api"

# Instellingen voor de inloggegevens van de website
API_USERNAME = os.getenv("username")
API_PASSWORD = os.getenv("password")
API_URL = "https://voxip.nl/api"

headers = {
    "Authorization": f"Bearer {HASS_TOKEN}",
    "Content-Type": "application/json",
}

def get_website_data():
    login_data = {"username": API_USERNAME, "password": API_PASSWORD}
    website_data_url = "https://voxip.nl/api"
    response = website_session.get(website_data_url, data=login_data)
    
    if response.ok:
        return response.json()
    else:
        return None

@app.route('/update-test-sensor', methods=['POST'])
def update_test_sensor():
    entity_id = "input_boolean.test_sensor"
    website_data = get_website_data()
    
    if website_data is not None:
        # Update de test sensor in Home Assistant met de verkregen waarden van de website
        url = f"{HASS_API}/states/{entity_id}"
        data = {"state": website_data["value"]}
        response = requests.post(url, headers=headers, json=data)
        
        if response.ok:
            return "Test sensor updated!", 200
        else:
            return "Failed to update test sensor.", 500
    else:
        return "Failed to retrieve website data.", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
