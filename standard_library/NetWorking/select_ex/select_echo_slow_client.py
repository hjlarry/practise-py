import socket
import sys
import time

messages = ["this is the message", "it will be repeat", "in parts"]
server_addr = ("localhost", 10000)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_addr)
time.sleep(1)

amount_expected = len("".join(messages))

try:
    for message in messages:
        outgoing_data = message.encode()
        print(f"{sock.getsockname()} sending {outgoing_data}", file=sys.stderr)
        sock.sendall(outgoing_data)
        time.sleep(1.5)

        amount_received = 0

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print(f"{sock.getsockname()} receive {data}", file=sys.stderr)
finally:
    print(f"{sock.getsockname()} close", file=sys.stderr)
    sock.close()

