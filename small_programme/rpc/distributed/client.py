import json
import time
import struct
import socket
import random
from kazoo.client import KazooClient

zk_root = "/demo"
G = {"servers": None}


class RemoteServer:
    def __init__(self, addr):
        self.addr = addr
        self._socket = None

    @property
    def socket(self):
        if not self._socket:
            self.connect()
        return self._socket

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host, port = self.addr.split(":")
        sock.connect((host, int(port)))
        self._socket = sock

    def rpc(self, in_, params):
        sock = self.socket
        request = json.dumps({"in": in_, "params": params})
        length_prefix = struct.pack("I", len(request))
        sock.send(length_prefix)
        sock.sendall(request.encode())
        length_prefix = sock.recv(4)
        (length,) = struct.unpack("I", length_prefix)
        body = sock.recv(length).decode()
        response = json.loads(body)
        return response["out"], response["result"]

    def ping(self, twitter):
        return self.rpc("ping", twitter)

    def pi(self, n):
        return self.rpc("pi", n)

    def reconnect(self):
        self.close()
        self.connect()

    def close(self):
        if self._socket:
            self._socket.close()
            self._socket = None


def get_servers():
    zk = KazooClient()
    zk.start()
    current_addr = set()

    def watch_servers(*args):
        new_addr = set()
        for child in zk.get_children(zk_root, watch=watch_servers):
            node = zk.get(zk_root + "/" + child)
            addr = json.loads(node[0])
            new_addr.add(f"{addr['host']}:{addr['port']}")
        add_addrs = new_addr - current_addr
        del_addrs = current_addr - new_addr

        del_servers = []
        for addr in del_addrs:
            for s in G["servers"]:
                if s.addr == addr:
                    del_servers.append(s)
                    break

        for server in del_servers:
            G["servers"].remove(server)
            current_addr.remove(server.addr)

        for addr in add_addrs:
            G["servers"].append(RemoteServer(addr))
            current_addr.add(addr)

    for child in zk.get_children(zk_root, watch=watch_servers):
        node = zk.get(zk_root + "/" + child)
        addr = json.loads(node[0])
        current_addr.add(f"{addr['host']}:{addr['port']}")

    G["servers"] = [RemoteServer(s) for s in current_addr]
    return G["servers"]


def random_server():
    if G["servers"] is None:
        get_servers()
    if not G["servers"]:
        return
    return random.choice(G["servers"])


if __name__ == "__main__":
    for i in range(100):
        server = random_server()
        if not server:
            break
        time.sleep(0.5)
        try:
            out, result = server.ping(f"ireader {i}")
            print(server.addr, out, result)
        except Exception as ex:
            server.close()
            print(ex)

        server = random_server()
        if not server:
            break
        time.sleep(0.5)
        try:
            out, result = server.pi(i)
            print(server.addr, out, result)
        except Exception as ex:
            server.close()
            print(ex)
