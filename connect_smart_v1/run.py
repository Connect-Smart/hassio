import os
import requests
from flask import Flask, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

# Gebruik het interne token verkregen door de supervisor
HASS_TOKEN = os.getenv("SUPERVISOR_TOKEN")
HASS_API = "http://supervisor/core/api"

# Instellingen voor de inloggegevens van de website
WEBSITE_USERNAME = os.getenv("username")
WEBSITE_PASSWORD = os.getenv("password")

headers = {
    "Authorization": f"Bearer {HASS_TOKEN}",
    "Content-Type": "application/json",
}

def login_to_website(username, password):
    # Hier implementeer je de logica om in te loggen op de website
    # Vervang de onderstaande code door de echte inloglogica van de website
    login_url = "https://voorbeeld-website.com/login"
    login_data = {"username": username, "password": password}

    response = requests.post(login_url, data=login_data)

    if response.ok:
        return True
    else:
        return False

def get_website_data():
    # Hier implementeer je de logica om gegevens van de website te halen
    # Vervang de onderstaande code door de echte logica om gegevens van de website te halen
    website_url = "https://voxip.nl/api"
    
    # In dit voorbeeld gebruiken we requests en BeautifulSoup voor webscraping
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
