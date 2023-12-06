import os
import requests
from flask import Flask, jsonify
from datetime import datetime, timedelta

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

def fetch_energy_data():
    login_data = {"username": API_USERNAME, "password": API_PASSWORD}
    website_data_url = "https://voxip.nl/api"
    response = requests.get(website_data_url, data=login_data)

    if response.ok:
        return response.json()
    else:
        return None

def extract_times(energy_data):
    cheapest_time = energy_data.get("cheapest_time")
    most_expensive_time = energy_data.get("most_expensive_time")

    return cheapest_time, most_expensive_time

def save_times_to_home_assistant(cheapest_time, most_expensive_time):
    cheapest_entity_id = "sensor.cheapest_energy_time"
    expensive_entity_id = "sensor.expensive_energy_time"

    # Format times as HH:MM
    cheapest_time_str = datetime.strptime(cheapest_time, "%Y-%m-%dT%H:%M:%S").strftime("%H:%M")
    most_expensive_time_str = datetime.strptime(most_expensive_time, "%Y-%m-%dT%H:%M:%S").strftime("%H:%M")

    # Update entities in Home Assistant
    update_entity(cheapest_entity_id, cheapest_time_str)
    update_entity(expensive_entity_id, most_expensive_time_str)

def update_entity(entity_id, state):
    url = f"{HASS_API}/states/{entity_id}"
    data = {"state": state}
    response = requests.post(url, headers=headers, json=data)
    return response.ok

def create_automation(cheapest_time, most_expensive_time):
    automation_entity_id = "automation.SC_energy_scheduler"

    automation_data = {
        "entity_id": automation_entity_id,
        "at": [cheapest_time, most_expensive_time]
    }

    url = f"{HASS_API}/services/automation/trigger"
    response = requests.post(url, headers=headers, json=automation_data)

    return response.ok

@app.route('/admin', methods=['GET'])
def get_energy_data():
    energy_data = fetch_energy_data()

    if energy_data:
        cheapest_time, most_expensive_time = extract_times(energy_data)
        save_times_to_home_assistant(cheapest_time, most_expensive_time)
        create_automation(cheapest_time, most_expensive_time)
        return "Data updated successfully.", 200
    else:
        return "Failed to fetch energy data.", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

