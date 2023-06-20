 w// this sends the sender name, message, and time to a local hosted http server made by other script (included)
// credits to ayy star for help, his discord server: discord.gg/v6ZF98cUTt

import { world, system } from "@minecraft/server";
//import * as mcnet from "@minecraft/server-net";

world.beforeEvents.chatSend.subscribe(e => {
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
	const message = `[${e.sender.name}] [${e.message}]`;
	console.log(message)
	//world.sendMessage(`§e<${e.sender.name}> §f${e.message}`);
});

//[2023-06-09 09:31:19:071 ERROR] [Scripting] Plugin [BSP Chat - 0.0.1] - [chat_relay.js] ran with error: [TypeError: cannot read property 'beforeChatSend' of undefined    at <anonymous> (chat_relay.js:23)
