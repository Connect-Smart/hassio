const WebSocket = require('ws');
const http = require('http');
const url = require('url');
const fs = require('fs');
const path = require('path');

const ENTITY_ID = 'sensor.example_sensor'; // Vervang dit door de entiteit die je wilt volgen

const server = http.createServer((req, res) => {
  const { pathname } = url.parse(req.url, true);

  if (pathname === '/') {
    const filePath = path.join(__dirname, 'index.html');
    const readStream = fs.createReadStream(filePath);
    readStream.pipe(res);
  }
});

const wss = new WebSocket.Server({ server });
let currentValue = 'unknown';

wss.on('connection', (ws) => {
  ws.send(currentValue);

  const interval = setInterval(() => {
    ws.send(currentValue);
  }, 1000);

  ws.on('close', () => {
    clearInterval(interval);
  });
});

// Update deze functie om de status van de entiteit te verkrijgen
function getEntityState() {
  // Hier zou je de huidige status van de entiteit van Home Assistant moeten ophalen
  // Je kunt hier de juiste Home Assistant API gebruiken
  // In dit voorbeeld wordt gewoon een willekeurige waarde geretourneerd
  return Math.random() > 0.5 ? 'on' : 'off';
}

setInterval(() => {
  const newState = getEntityState();
  if (newState !== currentValue) {
    currentValue = newState;
    wss.clients.forEach((client) => {
      client.send(currentValue);
    });
  }
}, 2000);

server.listen(8099, () => {
  console.log('Server running on port 8099');
});
