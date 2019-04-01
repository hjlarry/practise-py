import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = ("localhost", 10000)
sock.bind(server_addr)


while True:
    print("Wait to receive message")
    data, client_addr = sock.recvfrom(4096)
    print(f"received {len(data)} bytes from {client_addr}")
    print(data)
    if data:
        sent = sock.sendto(data, client_addr)
        print(f"sent {len(data)} bytes to {client_addr}")
