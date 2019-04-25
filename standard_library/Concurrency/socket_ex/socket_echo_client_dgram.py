import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = ("localhost", 10000)


try:
    message = b"this is a message ahahaha, it will repeated"
    print("sending ", message)
    sent = sock.sendto(message, server_addr)

    data, server = sock.recvfrom(4096)
    print("received", data)
finally:
    print("closing")
    sock.close()
