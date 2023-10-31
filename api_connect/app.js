const WebSocket = require("ws");
const http = require("http");
const fs = require("fs");

const server = http.createServer((req, res) => {
  if (req.url === "/") {
    res.writeHead(200, { "Content-Type": "text/html" });
    const html = fs.readFileSync("index.html", "utf-8");
    res.end(html);
  } else {
    res.writeHead(200, { "Content-Type": "text/html" });
    const html = fs.readFileSync("index.html", "utf-8");
    res.end(html);
  }
});

const wss = new WebSocket.Server({ noServer: true });

wss.on("connection", (ws) => {
  console.log("WebSocket client connected");

  // Simuleer periodieke updates
  const updateInterval = setInterval(() => {
    const entityName = "New Sensor";
    const entityValue = Math.floor(Math.random() * 100);
    ws.send(
      JSON.stringify({
        event_type: "state_changed",
        data: {
          entity_id: "sensor.energie_prijzen_CS",
          new_state: {
            attributes: {
              friendly_name: entityName,
            },
            state: entityValue.toString(),
          },
        },
      })
    );
  }, 5000);

  ws.on("close", () => {
    console.log("WebSocket client disconnected");
    clearInterval(updateInterval);
  });
});

server.on("upgrade", (request, socket, head) => {
  wss.handleUpgrade(request, socket, head, (ws) => {
    wss.emit("connection", ws, request);
  });
});

server.listen(8080, () => {
  console.log("Web server is running on port 8080");
});
