import http.server
import os

message_log_file = "message_log.txt"  # File to save the messages
latest_message = ""  # Shared variable for the latest message

# Function to save the message to a file and update the latest_message variable
def save_message_to_file(message):
    global latest_message
    with open(message_log_file, "a") as file:
        file.write(message + "\n")
    latest_message = message

# Create the message log file if it doesn't exist
if not os.path.exists(message_log_file):
    open(message_log_file, "w").close()

# Create a simple HTTP server handler
class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        message = self.rfile.read(content_length).decode("utf-8")
        save_message_to_file(message)

        print(message)
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        self.send_response(404)
        self.end_headers()

# Function to start the HTTP server

server_address = ("", 3000)
httpd = http.server.HTTPServer(server_address, SimpleHTTPRequestHandler)
print("Server started on port 3000")
httpd.serve_forever()
