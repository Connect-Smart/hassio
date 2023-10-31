const http = require('http');
const WebSocket = require('ws');
const homeassistant = require('homeassistant-api'); // Vereist 'homeassistant-api' of een soortgelijke bibliotheek

// Verbinding maken met Home Assistant
const ha = homeassistant({
  host: 'http://homeassistant.local',
  token: 'YOUR_LONG_LIVED_ACCESS_TOKEN',
});

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Dit is een Home Assistant add-on met WebSocket-ondersteuning!\n');
});

const wss = new WebSocket.Server({ server });

wss.on('connection', (ws) => {
  // Wanneer een client een WebSocket-verbinding tot stand brengt

  // Abonneer je op updates van een specifieke entiteit (bijv. een licht)
  const entityId = 'light.living_room';
  ha.subscribeState(entityId, (newState) => {
    // Verstuur de nieuwe entiteitstoestand naar de WebSocket-client
    ws.send(JSON.stringify({ entity: entityId, state: newState }));
  });

  ws.on('close', () => {
    // Wanneer de client de WebSocket-verbinding sluit, stop de entiteitssubscriptie
    ha.unsubscribeState(entityId);
  });
});

const port = process.env.PORT || 3000;

server.listen(port, () => {
  console.log(`Server draait op poort ${port}`);
});

process.on('SIGTERM', () => {
  console.log('Ontvangen SIGTERM, server wordt afgesloten...');
  server.close(() => {
    console.log('Server is gestopt.');
  });
});
