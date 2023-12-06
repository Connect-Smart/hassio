import os
import requests
from flask import Flask, jsonify
from datetime import datetime, time
import json
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# Gebruik het interne token verkregen door de supervisor
HASS_TOKEN = os.getenv("SUPERVISOR_TOKEN")
HASS_API = "http://supervisor/core/api"

API_USERNAME = os.getenv("username")
API_PASSWORD = os.getenv("password")
API_URL = "https://voxip.nl/api"

headers = {
    "Authorization": f"Bearer {HASS_TOKEN}",
    "Content-Type": "application/json",
}

# Variabelen om de goedkoopste en duurste tijd op te slaan
goedkoopste_tijd = None
duurste_tijd = None

def haal_en_verwerk_tijdinformatie():
    login_data = {"username": API_USERNAME, "password": API_PASSWORD}
    website_data_url = "https://voxip.nl/api"
    response = requests.get(website_data_url, data=login_data)
    
    if response.ok:
        # Verwerk de JSON en sla de tijden op
        data = response.json()
        global goedkoopste_tijd, duurste_tijd
        goedkoopste_tijd = datetime.strptime(data["goedkoopste_tijd"], "%H:%M:%S").time()
        duurste_tijd = datetime.strptime(data["duurste_tijd"], "%H:%M:%S").time()
    else:
        print("Fout bij het ophalen van tijdinformatie")

scheduler = BackgroundScheduler()
scheduler.add_job(haal_en_verwerk_tijdinformatie, 'interval', minutes=30)
scheduler.start()

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
    # Hier kun je de goedkoopste en duurste tijdgegevens retourneren
    return jsonify({"goedkoopste_tijd": str(goedkoopste_tijd), "duurste_tijd": str(duurste_tijd)}), 200

if __name__ == '__main__':
    # Voer de functie een keer uit om de initiële tijdinformatie op te halen
    haal_en_verwerk_tijdinformatie()
    
    # Start de Flask-applicatie
    app.run(host='0.0.0.0', port=8080)
