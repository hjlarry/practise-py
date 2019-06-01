import socket
import selectors
import struct
import json
import re

HOST = "127.0.0.1"
PORT = 8003
USER_MAP = {}
MATCH_REGEX = re.compile(r"@(.*?)\W+(.*)")

sel = selectors.DefaultSelector()


class ChatServer:
    def __init__(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.bind((host, port))
        sock.listen(5)
        self.sock = sock

    def read(self, conn: socket.socket, mask):
        try:
            chunk = conn.recv(4)
        except ConnectionResetError:
            return

        if len(chunk) < 4:  # 前4个字节是本次传输的内容长度
            return

        addr = conn.getpeername()
        slen = struct.unpack(">L", chunk)[0]  # 获得本次传输的内容长度
        chunk = conn.recv(slen)
        while len(chunk) < slen:
            chunk = chunk + conn.recv(slen - len(chunk))

        chunk = chunk.decode("utf8")

        if chunk.startswith("/set"):
            name = chunk.split()[1]
            self.set_username(addr, name)
            conn.sendall(b"set ok")
            print(USER_MAP)
        elif chunk.startswith("/list"):
            userlist = json.dumps(self.get_userlist())
            conn.sendall(userlist.encode("utf8"))
        elif chunk == "/quit":
            sel.unregister(conn)
            conn.close()
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
                        conn.sendall(b"User not exists")
                    else:
                        sock.sendall(
                            f"{self.get_username(addr)} said:".encode("utf8") + content
                        )
            else:
                conn.sendall(b"error cmd")

    @staticmethod
    def set_username(addr, name):
        USER_MAP[addr] = name

    @staticmethod
    def get_username(addr):
        return USER_MAP[addr]

    @staticmethod
    def get_userlist():
        return list(USER_MAP.values())

    def broadcast(self, content):
        for fd in sel._fd_to_key.values():
            sock = fd.fileobj
            if sock == self.sock:
                continue
            sock.sendall(content)

    def get_sock(self, username):
        to_addr = next(
            (addr for addr, name in USER_MAP.items() if name == username), None
        )
        if not to_addr:
            return None

        for fd in sel._fd_to_key.values():
            sock = fd.fileobj
            if sock == self.sock:
                continue
            addr = sock.getpeername()
            if to_addr == addr:
                return sock

    def accept(self, sock, mask):
        conn, addr = sock.accept()
        conn.setblocking(False)
        sel.register(conn, selectors.EVENT_READ, self.read)

    def server_forever(self):
        sel.register(self.sock, selectors.EVENT_READ, self.accept)
        while True:
            events = sel.select(0.5)
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)


if __name__ == "__main__":
    server = ChatServer(HOST, PORT)
    server.server_forever()
