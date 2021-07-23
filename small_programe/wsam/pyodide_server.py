# 该文件只是对于低版本的python3，高版本的直接运行python3 -m http.server 8000
import sys
import socketserver
from http.server import SimpleHTTPRequestHandler


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable Cross-Origin Resource Sharing (CORS)
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()


if sys.version_info < (3, 7, 5):
    # Fix for WASM MIME type for older Python versions
    Handler.extensions_map[".wasm"] = "application/wasm"


if __name__ == "__main__":
    port = 8000
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print("Serving at: http://127.0.0.1:{}".format(port))
        httpd.serve_forever()