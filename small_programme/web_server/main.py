from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
import logging
import urllib


class RequestDispatcher(BaseHTTPRequestHandler):
    def __init__(self, request: bytes, client_address: tuple[str, int], server) -> None:
        self._middlewares = [ServerHandle(), Index(), NotFound()]
        self._catchall = GenericError()
        super().__init__(request, client_address, server)

    def do_GET(self):
        ctx = HttpContext(self)
        try:
            for middleware in self._middlewares:
                if middleware.handle(ctx):
                    ctx.response.send()
                    break
        except Exception as e:
            ctx.error = e
            self._catchall.handle(ctx)
            ctx.response.send()


class Request:
    def __init__(self, handler: BaseHTTPRequestHandler) -> None:
        self._handler = handler

    @property
    def path(self) -> str:
        path, _ = urllib.parse.splitquery(self._handler.path)
        return path

    def query_string(self, key: str, default: str = None) -> str:
        _, qs = urllib.parse.splitquery(self._handler.path)
        args = dict(urllib.parse.parse_qsl(qs))
        return args.get(key, default)


class Response:
    def __init__(self, handler: BaseHTTPRequestHandler) -> None:
        self._handler = handler
        self._status = 200
        self._headers = {}
        self._data = BytesIO()

    def header(self, key: str, value: str):
        self._headers[key] = value
        return self

    def status(self, code: int):
        self._status = code
        return self

    def html(self, text: str):
        self._data.write(text.encode("utf8"))
        self._headers.setdefault("Content-Type", "text/html; charset=utf-8")
        return self

    def send(self):
        self._handler.send_response(self._status)
        resp_data = self._data.getvalue()
        self._headers.setdefault("Content-Length", len(resp_data))
        for k, v in self._headers.items():
            self._handler.send_header(k, v)
        self._handler.end_headers()
        self._handler.wfile.write(resp_data)


class HttpContext:
    def __init__(self, handler: BaseHTTPRequestHandler) -> None:
        self.request = Request(handler)
        self.response = Response(handler)
        self.error = None


class Middleware:
    def handle(self, ctx: HttpContext) -> bool:
        raise NotImplementedError()


class ServerHandle(Middleware):
    def handle(self, ctx: HttpContext) -> bool:
        ctx.response.header("X-Server-Type", "500 lines testonly")
        return False


class Index(Middleware):
    def handle(self, ctx: HttpContext) -> bool:
        if ctx.request.path == "/":
            if ctx.request.query_string("err", "0") == "1":
                raise Exception("test error")
            else:
                ctx.response.html("<h1>Index</h1>")
            return True
        return False


class NotFound(Middleware):
    def handle(self, ctx: HttpContext) -> bool:
        ctx.response.status(404).html("<h2> File not found </h2>")
        return True


class GenericError(Middleware):
    def handle(self, ctx: HttpContext) -> bool:
        if ctx.error:
            logging.getLogger("Server").error(str(ctx.error))
        ctx.response.status(500).html("<h1>Internal Server Error</h1>")
        return True


def main():
    server = HTTPServer(("127.0.0.1", 8081), RequestDispatcher)
    print("server run....")
    server.serve_forever()


if __name__ == "__main__":
    main()
