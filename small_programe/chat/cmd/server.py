import socketserver
import logging
import struct
import json
import re

HOST = "127.0.0.1"
PORT = 8003
USER_MAP = {}
MATCH_REGEX = re.compile(r"@(.*?)\W+(.*)")

logging.basicConfig(level=logging.DEBUG, format="%(name)s: %(message)s")


class CHatRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger("EchoRequestHandler")
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        while True:
            try:
                chunk = self.request.recv(4)
            except ConnectionResetError:
                return

            if len(chunk) < 4:  # 前4个字节是本次传输的内容长度
                return

            addr = self.request.getpeername()
            slen = struct.unpack(">L", chunk)[0]  # 获得本次传输的内容长度
            chunk = self.request.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.request.recv(slen - len(chunk))

            chunk = chunk.decode("utf8")

            if chunk.startswith("/set"):
                name = chunk.split()[1]
                self.set_username(addr, name)
                self.request.sendall(b"set ok")
                print(USER_MAP)
            elif chunk.startswith("/list"):
                userlist = json.dumps(self.get_userlist())
                self.request.sendall(userlist.encode("utf8"))
            elif chunk == "/quit":
                self.request.close()
            else:
                match = MATCH_REGEX.search(chunk)
                if match:
                    username, content = match.groups()
                    content = content.encode("utf8")
                    if username == "all":
                        self.broadcast(content)
                    else:
                        sock = self.get_sock(username)
                        if not sock:
                            self.request.sendall(b"User not exists")
                        else:
                            sock.sendall(
                                f"{self.get_username(addr)} said:".encode("utf8")
                                + content
                            )
                else:
                    self.request.sendall(b"error cmd")

    @staticmethod
    def set_username(addr, name):
        USER_MAP[addr] = name

    @staticmethod
    def get_username(addr):
        return USER_MAP[addr]

    def broadcast(self, content):
        with socketserver._ServerSelector() as sel:
            for fd in sel._fd_to_key.values():
                sock = fd.fileobj
                if sock == self.request:
                    continue
                sock.sendall(content)

    @staticmethod
    def get_userlist():
        return list(USER_MAP.values())


class ChatServer(socketserver.TCPServer):
    def __init__(self, server_address, handler_class=CHatRequestHandler):
        self.logger = logging.getLogger("EchoServer")
        self.logger.debug("__init__")
        socketserver.TCPServer.__init__(self, server_address, handler_class)

    def serve_forever(self, poll_interval=0.5):
        self.logger.debug("waiting for request")
        self.logger.info("Handling requests, press <Ctrl-C> to quit")
        socketserver.TCPServer.serve_forever(self, poll_interval)


if __name__ == "__main__":
    server = ChatServer((HOST, PORT), CHatRequestHandler)
    ip, port = server.server_address
    server.serve_forever()
