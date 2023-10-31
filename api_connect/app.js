const express = require('express');
const http = require('http');
const WebSocket = require('ws');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// Vervang 'jouw_entity_id' door de ID van de Home Assistant entity die je wilt volgen
const entityId = 'sensor.eettafel_lamp';

// Houd de huidige status bij
let currentState = {
  state: 'unknown', // Vervang door de juiste startstatus van de entity
};

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

wss.on('connection', (ws) => {
  // Stuur de huidige status van de entity naar de client bij verbinding
  ws.send(JSON.stringify(currentState));
});

// Luister naar wijzigingen in de entity-status van Home Assistant
const homeAssistantSocket = new WebSocket('ws://homeassistant.local:8123/api/websocket');

homeAssistantSocket.on('open', () => {
  homeAssistantSocket.send(
    JSON.stringify({
      type: 'subscribe_events',
      event_type: 'state_changed',
    })
  );
});

homeAssistantSocket.on('message', (message) => {
  const msg = JSON.parse(message);
  if (msg.type === 'event' && msg.event.event_type === 'state_changed') {
    const newState = msg.event.data.new_state;
    if (newState.entity_id === entityId) {
      currentState = newState;
      // Stuur de bijgewerkte status naar alle aangesloten clients
      wss.clients.forEach((client) => {
        if (client.readyState === WebSocket.OPEN) {
          client.send(JSON.stringify(currentState));
        }
      });
    }
  }
});

server.listen(8099, () => {
  console.log('Addon is gestart op poort 8099');
});
