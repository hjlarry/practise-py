from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
import logging
import mimetypes
import os
import urllib
import re
from datetime import datetime


class RequestDispatcher(BaseHTTPRequestHandler):
    def __init__(self, request: bytes, client_address: tuple[str, int], server) -> None:
        self._middlewares = [
            ServerHandle(),
            routing,
            Index(),
            StaticFile(os.path.dirname(__file__) + "/static"),
            NotFound(),
        ]
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
        result = urllib.parse.urlparse(self._handler.path)
        return result.path

    def query_string(self, key: str, default: str = None) -> str:
        result = urllib.parse.urlparse(self._handler.path)
        args = dict(urllib.parse.parse_qsl(result.query))
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

    def data(self, content: bytes):
        self._data.write(content)
        return self


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


class StaticFile(Middleware):
    def __init__(self, root_path: str) -> None:
        self._root_path = root_path

    def handle(self, ctx: HttpContext) -> bool:
        full_path = os.path.normpath(self._root_path + ctx.request.path)
        if os.path.isfile(full_path):
            self.send_file(ctx.response, full_path)
            return True
        elif os.path.isdir(full_path):
            if self.process_index(ctx.response, full_path):
                return True
            else:
                html = self.build_dir_html(full_path)
                ctx.response.html(html)
                return True
        return False

    def send_file(self, resp: Response, file_path: str):
        content_type = mimetypes.guess_type(file_path)[0] or "application/octec-stream"
        with open(file_path, "rb") as f:
            resp.header("Content-Type", content_type).data(f.read())

    def process_index(self, resp: Response, dir_path: str):
        index_names = ["index.html", "index.htm", "default.html", "default.htm"]
        for name in index_names:
            index_path = os.path.join(dir_path, name)
            if os.path.isfile(index_path):
                self.send_file(resp, index_path)
                return True
        return False

    def build_dir_html(self, dir_path: str) -> str:
        lines = []
        lines.append(f"<h1>Direcdtory of {os.path.split(dir_path)[1]}:</h1>")
        lines.append("<hr/>")
        lines.append("<table>")
        lines.append("<thead><tr><th>Name</th><th>Size</th><th>Time</th></tr></thead>")
        lines.append("<tbody>")
        for file_name in os.listdir(dir_path):
            full_path = os.path.join(dir_path, file_name)
            lines.append("<tr>")
            lines.append(f"<td>{file_name}</td>")
            stat = os.stat(full_path)
            size_str = str(stat.st_size) if os.path.isfile(full_path) else ""
            lines.append(f"<td>{size_str}</td>")
            lines.append(f"<td>{datetime.fromtimestamp(stat.st_mtime)}</td>")
            lines.append("</tr>")
        lines.append("</tbody>")
        lines.append("</table>")
        return "\n".join(lines)


class Routing(Middleware):
    def __init__(self) -> None:
        self._routes = []

    def handle(self, ctx: HttpContext) -> bool:
        for pattern, handler in self._routes:
            kwargs = self.match(ctx.request.path, pattern)
            if kwargs is not None:
                handler(ctx.request, ctx.response, **kwargs)
                return True
        return False

    def match(self, url_path: str, pattern: str) -> dict:
        re_pattern = "^" + re.sub(r"<(\w+)>", r"(?P<\1>\\w+)", pattern) + "$"
        m = re.match(re_pattern, url_path)
        return m.groupdict() if m else None

    def route(self, path: str):
        def wrapper(f):
            self._routes.append((path, f))
            return f

        return wrapper


routing = Routing()


@routing.route("/aindex")
def another_index(req, resp):
    resp.html("<h1>Another Index</h1>")


@routing.route("/user/<name>")
def username(req, resp, name):
    resp.html(f"<h1>hello {name}</h1>")


def main():
    server = HTTPServer(("127.0.0.1", 8081), RequestDispatcher)
    print("server run....")
    server.serve_forever()


if __name__ == "__main__":
    main()
