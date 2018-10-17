from http.server import BaseHTTPRequestHandler, HTTPServer
import multiprocessing
from socketserver import ForkingMixIn

class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain;charset=utf-8')
        self.end_headers()
        message = multiprocessing.current_process().name
        self.wfile.write(message.encode('utf-8'))

class ForkedHttpServer(ForkingMixIn, HTTPServer):
    pass

server = ForkedHttpServer(('127.0.0.1', 8081), GetHandler)
print('server run....')
server.serve_forever()