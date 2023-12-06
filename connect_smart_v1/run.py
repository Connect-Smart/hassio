import os
import requests
from flask import Flask, jsonify
from datetime import datetime, timedelta
import schedule
import time

config_path = os.path.join(os.path.dirname(__file__), "config.json")

# Controleer of het configuratiebestand bestaat
if os.path.exists(config_path):
    # Lees de inhoud van het configuratiebestand
    with open(config_path, "r") as file:
        config_data = json.load(file)

    # Nu kun je toegang krijgen tot de configuratievariabelen
    if "entries" in config_data:
        entries = config_data["entries"]
        print("Configuratie-entries gevonden:", entries)
    else:
        print("Configuratie-entries niet gevonden in het configuratiebestand.")
else:
    print("Configuratiebestand niet gevonden op het verwachte pad:", config_path)

app = Flask(__name__)

# Gebruik het interne token verkregen door de supervisor
HASS_TOKEN = os.getenv("SUPERVISOR_TOKEN")
HASS_API = "http://supervisor/core/api"

AUTOMATION_CHEAPEST = os.getenv("cheapest_energy_automation")
AUTOMATION_EXPENSIVE = os.getenv("most_expensive_energy_automation")
SCHEDULE = os.getenv("schedule")
print(f"De waarde van mijn_var is: {SCHEDULE}")


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
    cheapest_time_str = datetime.strptime(cheapest_time, "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
    most_expensive_time_str = datetime.strptime(most_expensive_time, "%Y-%m-%d %H:%M:%S").strftime("%H:%M")

    # Update entities in Home Assistant
    update_entity(cheapest_entity_id, cheapest_time_str)
    update_entity(expensive_entity_id, most_expensive_time_str)

    return cheapest_time_str, most_expensive_time_str

def update_entity(entity_id, state):
    url = f"{HASS_API}/states/{entity_id}"
    data = {"state": state}
    response = requests.post(url, headers=headers, json=data)
    return response.ok

def create_automation(trigger_time, automation_name, automation_entity_id):
    # Create automation in Home Assistant
    automation_data = {
        "name": automation_name,
        "trigger": [
            {
                "platform": "time",
                "at": trigger_time
            }
        ],
        "action": [
            {
                "service": "light.toggle",  # Replace with the actual service for your device
                "target": {
                    "entity_id": "light.testaktor_dimaktor"
                }
            }
        ]
    }

    url = f"{HASS_API}/config/automation/create"
    response = requests.post(url, headers=headers, json=automation_data)

    return response.ok

@app.route('/admin', methods=['GET'])
def get_energy_data():
    energy_data = fetch_energy_data()

    if energy_data:
        cheapest_time, most_expensive_time = extract_times(energy_data)
        cheapest_trigger, expensive_trigger = save_times_to_home_assistant(cheapest_time, most_expensive_time)

        create_automation(cheapest_trigger, "Cheapest Energy Automation", AUTOMATION_CHEAPEST)
        create_automation(expensive_trigger, "Most Expensive Energy Automation", AUTOMATION_EXPENSIVE)

        return "Data and automations updated successfully.", 200
    else:
        return "Failed to fetch energy data.", 500

schedule.every().day.at(str(SCHEDULE)).do(get_energy_data)

def run_scheduled_job():
    print("Executing Schedule")
    while True:
        schedule.run_pending()
        time.sleep(1)

# Rest van je code blijft hetzelfde...

if __name__ == '__main__':
    # Start de Flask-app in een aparte thread
    import threading
    flask_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 8080})
    flask_thread.start()

    # Start de geplande job in de hoofdthread
    run_scheduled_job()
