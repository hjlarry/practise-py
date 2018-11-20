import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ("localhost", 10000)
sock.connect(server_addr)


try:
    message = b'this is a message ahahaha, it will repeated'
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
    print('closing')
    sock.close()

