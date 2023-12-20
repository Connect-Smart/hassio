import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # SQLite database
#db = SQLAlchemy(app)
#migrate = Migrate(app, db)

# Gebruik het interne token verkregen door de supervisor
HASS_TOKEN = os.getenv("SUPERVISOR_TOKEN")
HASS_API = "http://supervisor/core/api"

headers = {
    "Authorization": f"Bearer {HASS_TOKEN}",
    "Content-Type": "application/json",
}

@app.route('/toggle-switch', methods=['POST'])
def toggle_switch():
    entity_id = "switch.jouw_switch_entity_id"
    url = f"{HASS_API}/services/switch/toggle"
    data = {"entity_id": entity_id}
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.ok:
        return response.json()
    else:
        return "Failed to toggle switch.", 500

@app.route('/admin', methods=['GET'])
def get_test_sensor():
    entity_id = "sensor.CS_solar_switch"
    url = f"{HASS_API}/states/{entity_id}"
    
    response = requests.get(url, headers=headers)
    
    if response.ok:
        return jsonify(response.json()), 200
    else:
        return "Failed to retrieve sensor data.", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)