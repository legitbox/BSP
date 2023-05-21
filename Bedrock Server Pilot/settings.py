# list of all settings in server.properties for the main file to make a gui out of.

# format is this: setting name, setting value, options, simple description

# setting name must be the same as the setting name in server.properties except without '-' and capatalized, format all others to None if you want it to be a divider.
# leave setting value emty when adding new settings, as that is filled in by with values from server.properties
# options is only for the values if the setting is a combo box, None otherwise
# simple description is what it sounds like, a simple descrpition that is displayed under the setting
# the tooltip is what shows when hovering over the question mark next to the setting

SETTINGS1 = [
    ('————————————Server Settings————————————', None, None, None, None),
    ('Server Name', '', None, 'The name of the server', 'The name of the server\nAllowed values: Any string without semicolon symbol'),
    ('Level Name', '', None, 'The name of the world to use', 'The name of the world to use\nAllowed values: Any string without semicolon symbol or symbols illegal for file name: n,r,t,f,`,?,*,\,/,<,>,|,":'),    
    ('Gamemode', '', ['Creative', 'Survival', 'Adventure'], 'The default gamemode for new players', 'The default gamemode for new players\nAllowed values: "survival", "creative", or "adventure"'),
    ('Difficulty', '', ['Peaceful', 'Easy', 'Normal', 'Hard'], 'The difficulty level of the world', 'Sets the difficulty of the world.\nAllowed values: "peaceful", "easy", "normal", or "hard"'),
    ('Default Player Permission Level', '', ['Visitor', 'Member', 'Operator'], 'The default permission level for new players', 'Permission level for new players joining for the first time.\nAllowed values: "visitor", "member", "operator"'),    
    ('View Distance', '', None, 'The maximum allowed view distance in number of chunks', 'The maximum allowed view distance in number of chunks.\nAllowed values: Positive integer equal to 5 or greater.'),
    ('Tick Distance', '4', None, 'The world will be ticked this many chunks away from any player', 'The world will be ticked this many chunks away from any player.\nAllowed values: Integers in the range [4, 12]'),
    ('Player Idle Timeout', '30', None, 'The amount of time in minutes before a player is kicked for being idle', 'After a player has idled for this many minutes they will be kicked. If set to 0 then players can idle indefinitely.\nAllowed values: Any non-negative integer'),
    ('Allow Cheats', '', None, 'If checked then cheats like commands can be used', 'If true then cheats like commands can be used.\nAllowed values: "true" or "false"'),
    ('Allow List', '', None, 'If checked, all players must be listed in allowlist.json', 'If true then all connected players must be listed in the separate allowlist.json file.\nAllowed values: "true" or "false"'),
    ('————————————Network Settings————————————', None, None, None, None),
    ('Server Port', '', None, 'Which IPv4 port the server should listen to', 'Which IPv4 port the server should listen to.\nAllowed values: Integers in the range [1, 65535]'),
    ('Server Portv6', '', None, 'Which IPv6 port the server should listen to', 'Which IPv6 port the server should listen to.\nAllowed values: Integers in the range [1, 65535]'),
    ('Online Mode', '', None, 'If true then all connected players must be authenticated to Xbox Live', 'If true then all connected players must be authenticated to Xbox Live.\nClients connecting to remote (non-LAN) servers will always require Xbox Live authentication regardless of this setting.\nIf the server accepts connections from the Internet, then its highly recommended to enable online-mode.\nAllowed values: "true" or "false"'),     
    ('Enable Lan Visibility', '', None, 'Whether the server should be visible on the local network', 'Listen and respond to clients that are looking for servers on the LAN. This will cause the server\nto bind to the default ports (19132, 19133) even when `server-port` and `server-portv6`\nhave non-default values. Consider turning this off if LAN discovery is not desirable, or when\nrunning multiple servers on the same host may lead to port conflicts.\nAllowed values: "true" or "false"'),

]    
    
SETTINGS2 = [   
    ('Emit Server Telemetry', '', None, 'A boolean indicating whether to emit telemetry from the server','Idk'),    
    ('Enable Query', '', None, 'A boolean indicating whether to enable server query', 'Idk'),      
    ('———————————Advanced Settings———————————', None, None, None, None),
    ('Compression Threshold', '', None, 'Determines the smallest size of raw network payload to compress', 'Determines the smallest size of raw network payload to compress.\nAllowed values: 0-65535'),
    ('Compression Algorithm', '', ['Zlib', 'Snappy'], 'Determines the compression algorithm to use for networking', 'Determines the compression algorithm to use for networking.\nAllowed values: "zlib", "snappy"'),
    ('Max Threads', '', None, 'Maximum number of threads the server will try to use.', 'Maximum number of threads the server will try to use. If set to 0 or removed then it will use as many as possible.\nAllowed values: Any positive integer.'),        
    ('Server Authoritative Movement', '', ['Server Auth', 'Client Auth', 'Server Auth With Rewind'], 'Enables server authoritative movement with corrections. Requires correct-player-movement to be true.', 'Enables server authoritative movement. If "server-auth", the server will replay local user input on\nthe server and send down corrections when the clients position doesnt match the servers.\nIf "server-auth-with-rewind" is enabled and the server sends a correction, the clients will be instructed\nto rewind time back to the correction time, apply the correction, then replay all the players inputs since then. This results in smoother and more frequent corrections.\nCorrections will only happen if correct-player-movement is set to true.\mAllowed values: "client-auth", "server-auth", "server-auth-with-rewind"'),
    ('Player Movement Score Threshold', '', None, 'The number of incongruent time intervals needed before abnormal behavior is reported', 'The number of incongruent time intervals needed before abnormal behavior is reported.\nDisabled by server-authoritative-movement.'),
    ('Player Movement Action Direction Threshold', '', None, 'The amount that the players attack direction and look direction can differ', 'The amount that the players attack direction and look direction can differ.\nAllowed values: Any value in the range of [0, 1] where 1 means that the\ndirection of the players view and the direction the player is attacking\nmust match exactly and a value of 0 means that the two directions can\ndiffer by up to and including 90 degrees.'),
    ('Player Movement Distance Threshold', '', None, 'Position threshold for detecting abnormal behavior between server and client', 'The difference between server and client positions that needs to be exceeded before abnormal behavior is detected.\nDisabled by server-authoritative-movement.'),
    ('Player Movement Duration Threshold In Ms', '', None, 'The duration of time the server and client positions can be out of sync', 'The duration of time the server and client positions can be out of sync (as defined by player-movement-distance-threshold)\nbefore the abnormal movement score is incremented. This value is defined in milliseconds.\nDisabled by server-authoritative-movement.'),
    ('Correct Player Movement', '', None, 'Corrects client position to server position if movement score is above threshold.', 'If true, the client position will get corrected to the server position if the movement score exceeds the threshold.'),     
    ('Client Side Chunk Generation Enabled', '', None, 'Server allows clients to generate visual level chunks outside player interaction distances', 'If true, the server will inform clients that they have the ability to generate visual level chunks outside of player interaction distances.'),
    ('Server Authoritative Block Breaking', '', None, 'The server validates block mining based on client actions for block breaking.', 'If true, the server will compute block mining operations in sync with the client so it can verify that the client should be able to break blocks when it thinks it can.'),       
    ('Block Network Ids Are Hashes', '', None, 'Server sends hashed block network IDs, instead of sequential IDs starting from 0', 'If true, the server will send hashed block network IDs instead of ids that start from 0 and go up.  These ids are stable and wont change regardless of other block changes.'),

]

SETTINGS3 = [
    ('————————————Misc. Settings————————————', None, None, None, None),    
    ('Max Players', '', None, 'The maximum number of players allowed on the server', 'The maximum number of players that can play on the server.\nAllowed values: Any positive integer'),
    ('Level Seed', '', None, 'The seed used to generate the level/world', 'Use to randomize the world\nAllowed values: Any string'),    
    ('Server Build Radius Ratio', '', ['Disabled', 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], 'Server either dynamically or manually sets the players view generation ratio', 'Allowed values: "Disabled" or any value in range [0.0, 1.0]\nIf "Disabled" the server will dynamically calculate how much of the players view it will generate, assigning the rest to the client to build.\nOtherwise from the overridden ratio tell the server how much of the players view to generate, disregarding client hardware capability.\nOnly valid if client-side-chunk-generation-enabled is enabled'),
    ('Chat Restriction', '', ['None', 'Dropped', 'Disabled'], 'The level of restriction applied to the chat for each player', 'Allowed values: "None", "Dropped", "Disabled"\nThis represents the level of restriction applied to the chat for each player that joins the server.\n"None" is the default and represents regular free chat.\n"Dropped" means the chat messages are dropped and never sent to any client. Players receive a message to let them know the feature is disabled.\n"Disabled" means that unless the player is an operator, the chat UI does not even appear. No information is displayed to the player.'),     
    ('Content Log File Enabled', '', None, 'Enables logging content errors to a file', 'Enables logging content errors to a file\nAllowed values: "true" or "false"'),    
    ('Force Gamemode', '', None, 'Disable non-default gamemode values even if set in server.properties after world creation', 'force-gamemode=false (or force-gamemode is not defined in the server.properties)\nprevents the server from sending to the client gamemode values other\nthan the gamemode value saved by the server during world creation\neven if those values are set in server.properties after world creation.\n\nforce-gamemode=true forces the server to send to the client gamemode values\nother than the gamemode value saved by the server during world creation\nif those values are set in server.properties after world creation.'),
    ('Texturepack Required', '', None, 'Force clients to use texture packs in the current world', 'Force clients to use texture packs in the current world\nAllowed values: "true" or "false"'),
    ('Disable Player Interaction', False, None, 'When checked, clients will ignore other players/interactions with the world', 'If true, the server will inform clients that they should ignore other players when interacting with the world. This is not server authoritative.'),
    ('Disable Persona', '', None, 'Internal use only?', 'Internal Use Only'),
    ('Disable Custom Skins', '', None, 'If checked, block non-store/non-game customized skins', 'If true, disable players customized skins that were customized outside of the Minecraft store assets or in game assets.\nThis is used to disable possibly offensive custom skins players make.'),
]
