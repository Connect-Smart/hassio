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







headers = {
    "Authorization": f"Bearer {HASS_TOKEN}",
    "Content-Type": "application/json",
}

def login_to_website(username, password):
    login_url = "https://voxip.nl/api/"
    login_data = {"username": username, "password": password}

    response = requests.post(login_url, data=login_data)

    if response.ok:
        return True
    else:
        return False

def get_website_data():
    website_url = "https://voxip.nl/api"
    
    response = requests.get(website_url)

    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        value = float(soup.find(id='value').text)
        return {"value": value}
    else:
        return None

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
    entity_id = "sensor.test_sensor"
    
    # Inloggen op de website
    if login_to_website(WEBSITE_USERNAME, WEBSITE_PASSWORD):
        # Gegevens van de website ophalen
        website_data = get_website_data()

        if website_data is not None:
            update_url = f"{HASS_API}/states/{entity_id}"
            update_data = website_data

            response = requests.post(update_url, headers=headers, json=update_data)

            if response.ok:
                return "Test sensor updated!", 200
            else:
                return "Failed to update test sensor.", 500
        else:
            return "Failed to retrieve data from the website.", 500
    else:
        return "Failed to login to the website.", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
