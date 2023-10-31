const express = require('express');
const http = require('http');
const WebSocket = require('ws');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// Vervang 'jouw_entity_id' door de ID van de Home Assistant entity die je wilt volgen
const entityId = 'sensor.eettafel_lamp';

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

wss.on('connection', (ws) => {
  // Stuur de huidige status van de entity naar de client bij verbinding
  const currentState = {
    state: 'unknown', // Vervang door de juiste startstatus van de entity
  };
  ws.send(JSON.stringify(currentState));

  // Luister naar wijzigingen in de entity-status van Home Assistant
  const homeAssistantSocket = new WebSocket('ws://homeassistant.local:8123/api/websocket');
  homeAssistantSocket.on('message', (message) => {
    const msg = JSON.parse(message);
    if (msg.type === 'event' && msg.event.event_type === 'state_changed') {
      const newState = msg.event.data.new_state;
      if (newState.entity_id === entityId) {
        ws.send(JSON.stringify(newState));
      }
    }
  });

  ws.on('close', () => {
    homeAssistantSocket.close();
  });
});

server.listen(8099, () => {
  console.log('Addon is gestart op poort 8099');
});
