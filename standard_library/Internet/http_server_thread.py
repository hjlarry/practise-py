from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from socketserver import ThreadingMixIn


class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain;charset=utf-8")
        self.end_headers()
        message = threading.currentThread().getName()
        self.wfile.write(message.encode("utf-8"))


class ThreadedHttpServer(ThreadingMixIn, HTTPServer):
    pass


server = ThreadedHttpServer(("127.0.0.1", 8081), GetHandler)
print("server run....")
server.serve_forever()
