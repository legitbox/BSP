// this sends the sender name, message, and time to a local hosted http server made by other script (included)
// credits to ayy star for help, his discord server: discord.gg/v6ZF98cUTt

import { world, system } from "@minecraft/server";
import * as mcnet from "@minecraft/server-net";

const targetServerHost = "localhost";
const targetServerPort = 3000;

// Function to send messages to the target HTTP server
async function sendToServer(message) {
  const req = new mcnet.HttpRequest(`http://${targetServerHost}:${targetServerPort}`);
  req.body = message;
  req.method = mcnet.HttpRequestMethod.POST;
  req.headers = [
    new mcnet.HttpHeader("Content-Type", "text/plain"),
  ];

  await mcnet.http.request(req);
}

// Modify the event handlers to send messages to the target HTTP server
world.events.beforeChat.subscribe(e => {
	const currentDate = new Date();
	const formattedDate = currentDate.toLocaleString("en-US", {
		year: "numeric",
		month: "2-digit",
		day: "2-digit",
		hour: "2-digit",
		minute: "2-digit",
		second: "2-digit",
		hour12: false,
	  });
	const message = `[${e.sender.name}] [${e.message}] [${formattedDate}]`;
  	sendToServer(message);
  //world.sendMessage(`§e<${e.sender.name}> §f${e.message}`);
});
