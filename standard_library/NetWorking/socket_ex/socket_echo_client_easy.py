import socket
import sys

server_addr = ("localhost", 10000)
# create_connection() uses getaddrinfo() to find candidate connection parameters,
# and returns a socket opened with the first configuration that creates a successful connection
sock = socket.create_connection(server_addr)

try:
    message = b"this is a message ahahaha, it will repeated"
    print("sending ", message)
    sock.sendall(message)

    # Look for response
    amount_received = 0
    amount_expected = len(message)
    while amount_expected > amount_received:
        data = sock.recv(5)
        print("received ", data)
        amount_received += len(data)
finally:
    print("closing")
    sock.close()
