import os
import requests
from flask import Flask, jsonify, render_template
from flask_assistant import Assistant, tell
from datetime import datetime, timedelta
import schedule
import time

app = Flask(__name__)
assist = Assistant(app)

# Gebruik het interne token verkregen door de supervisor
HASS_TOKEN = os.getenv("SUPERVISOR_TOKEN")
HASS_API = "http://supervisor/core/api"

AUTOMATION_CHEAPEST = "CS_cheapest_energy_automation"
AUTOMATION_EXPENSIVE = "CS_most_expensive_energy_automation"

SCHEDULE = "08:01"

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

@app.route('/toggle_switch', methods=['POST'])
def toggle_switch_route():
    switch_name = request.form.get('switch_name')
    
    # Implement your logic here to toggle the switch
    # You may need to interact with Home Assistant or another platform to perform the actual switch toggling
    # For now, let's print a message as a placeholder
    print(f'Toggling switch: {switch_name}')

    return "Switch toggled successfully."

@app.route('/admin')
def admin_panel():
    return render_template('admin_panel.html')  # Maak een HTML-sjabloon voor je admin-paneel

@app.route('/admin_panel', methods=['GET'])
def admin_panel():
    return render_template('toggle_switch.html')

@app.route('/energy_data', methods=['GET'])
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

schedule.every().day.at(SCHEDULE).do(get_energy_data)

def run_scheduled_job():
    print("Executing Schedule")
    while True:
        schedule.run_pending()
        time.sleep(1)

@assist.action('toggle-switch')
def toggle(switch):
    speech = 'Toggling switch for {}'.format(switch)
    hass.switch(switch)
    return tell(speech)

@assist.action('switch-on')
def switch_on(switch):
    speech = 'Flipping on {} switch'.format(switch)
    hass.switch(switch, service='turn_on')
    return tell(speech)


if __name__ == '__main__':
    # Start de Flask-app in een aparte thread
    import threading
    flask_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 8080})
    flask_thread.start()

    # Start de geplande job in de hoofdthread
    run_scheduled_job()
