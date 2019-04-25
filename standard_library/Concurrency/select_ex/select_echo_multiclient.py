import socket
import sys

messages = ["this is the message", "it will be repeat", "in parts"]
server_addr = ("localhost", 10000)
socks = [
    socket.socket(socket.AF_INET, socket.SOCK_STREAM),
    socket.socket(socket.AF_INET, socket.SOCK_STREAM),
    socket.socket(socket.AF_INET, socket.SOCK_STREAM),
]

for s in socks:
    s.connect(server_addr)

for message in messages:
    outgoing_data = message.encode()
    for s in socks:
        print(f"{s.getsockname()} sending {outgoing_data}", file=sys.stderr)
        s.send(outgoing_data)
    for s in socks:
        data = s.recv(1024)
        print(f"{s.getsockname()} receive {data}", file=sys.stderr)
        if not data:
            print(f"{s.getsockname()} close", file=sys.stderr)
            s.close()
