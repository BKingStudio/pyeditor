from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import json

class RequestHandler(BaseHTTPRequestHandler):
    # Serve HTML page for GET requests
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            with open("index.html", "rb") as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404, "File not found")

    # Handle code execution for POST requests
    def do_POST(self):
        if self.path == "/run":
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            data = json.loads(body)
            code = data.get("code", "")

            try:
                # Execute the Python code and capture output
                output = subprocess.check_output(
                    ["python", "-c", code],
                    stderr=subprocess.STDOUT,
                    text=True,  # Ensure output is returned as string
                    shell=False
                )
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"output": output}).encode())
            except subprocess.CalledProcessError as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"output": "Error: " + e.output}).encode())

# Start the server
if __name__ == "__main__":
    httpd = HTTPServer(("localhost", 8000), RequestHandler)
    print("Server started on http://localhost:8000")
    httpd.serve_forever()
    
