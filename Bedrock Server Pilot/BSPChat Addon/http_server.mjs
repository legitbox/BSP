import * as http from "http";
import * as fs from "fs";

const messageLogFile = "message_log.txt"; // File to save the messages

// Function to save the message to a file
function saveMessageToFile(message) {
  fs.appendFileSync(messageLogFile, `${message}\n`);
}

// Create the message log file if it doesn't exist
if (!fs.existsSync(messageLogFile)) {
  fs.writeFileSync(messageLogFile, "");
}

// Create a simple HTTP server
const server = http.createServer((req, res) => {
  if (req.method === "POST") {
    let data = "";
    req.on("data", chunk => {
      data += chunk;
    });
    req.on("end", () => {
      const message = data.toString();
      saveMessageToFile(message);
      console.log("Received message:", message);
      res.writeHead(200);
      res.end();
    });
  } else {
    res.writeHead(404);
    res.end();
  }
});

// Start the HTTP server
server.listen(3000, () => {
  console.log("Server started on port 3000");
});
