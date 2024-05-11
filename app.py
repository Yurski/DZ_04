from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from socketserver import UDPServer, BaseRequestHandler
import json
from datetime import datetime

class HttpGetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path == '/':
            self.send_html("index.html")
        elif url.path == '/message.html':
            self.send_html("message.html")
        elif url.path == '/logo.png':
            self.send_image("logo.png")
        elif url.path == '/style.css':
            self.send_css("style.css")
        else:
            self.send_html("error.html", 404)

    def send_html(self, html_filename, status=200):
        self.send_response(status)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        with open(html_filename, 'rb') as f:
            self.wfile.write(f.read())

    def send_image(self, image_filename, status=200):
        self.send_response(status)
        self.send_header('content-type', 'image/png')  
        self.end_headers()
        with open(image_filename, 'rb') as f:
            self.wfile.write(f.read())


    def send_css(self, css_filename, status=200):
        self.send_response(status)
        self.send_header('content-type', 'text/css')
        self.end_headers()
        with open(css_filename, 'rb') as f:
            self.wfile.write(f.read())



class UDPHandler(BaseRequestHandler):
    def handle(self):
        data = self.request[0].decode("utf-8")
        address = self.client_address
        received_data = json.loads(data)
        received_data["timestamp"] = datetime.now().isoformat()
        with open("storage/data.json", "a") as file:
            json.dump(received_data, file)
            file.write("\n")
        print(f"Received data from {address}: {received_data}")


def run_http_server(server_class=HTTPServer, handler_class=HttpGetHandler):
    server_address = ('', 3000)
    http_server = server_class(server_address, handler_class)
    http_server.serve_forever()


def run_udp_server(server_class=UDPServer, handler_class=UDPHandler):
    server_address = ('', 5000)
    udp_server = server_class(server_address, handler_class)
    udp_server.serve_forever()


if __name__ == "__main__":
    import threading
    http_thread = threading.Thread(target=run_http_server)
    udp_thread = threading.Thread(target=run_udp_server)
    http_thread.start()
    udp_thread.start()
