const express = require('express');
const WebSocket = require('home-assistant-js-websocket');
const app = express();

// Verander dit naar het IP-adres en het wachtwoord van je Home Assistant-installatie.
const haUrl = 'http://10.0.0.20:8123';
const haAuthToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI0MmJiYzgzOTA3YTQ0NjgyYTIwMDU3YTg0MWM4ZDZmMSIsImlhdCI6MTY5ODc5MTcxMSwiZXhwIjoyMDE0MTUxNzExfQ.AgCMiPY7svqVC3fs_PxiePBFWtEg6cQYG-eISc1q18Y';

const haSocket = new WebSocket.Connection({
  createSocketUrl: (path) => `${haUrl}/api/websocket`,
  accessToken: haAuthToken,
});

haSocket.connect();

app.get('/', (req, res) => {
  res.send(`
    <h1>Status van de entiteit</h1>
    <p id="entityStatus">Laden...</p>
    <script>
      const entityStatus = document.getElementById('entityStatus');
      const socket = new WebSocket('${haUrl}/api/websocket');
      socket.onopen = () => {
        socket.send(JSON.stringify({ type: 'auth', access_token: '${haAuthToken}' }));
        socket.send(JSON.stringify({ id: 1, type: 'subscribe_events', event_type: 'state_changed' }));
      };
      socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'event' && data.event.event_type === 'state_changed') {
          entityStatus.innerText = 'Status: ' + data.event.data.new_state.state;
        }
      };
    </script>
  `);
});

app.listen(8099, () => {
  console.log('Server gestart op poort 8099');
});
