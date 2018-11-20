import socket
import sys
import os


server_addr = "/tmp/uds_socket"
# make sure the socket does not already exist
try:
    os.unlink(server_addr)
except OSError:
    if os.path.exists(server_addr):
        raise

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
print("starting up on ", server_addr)
sock.bind(server_addr)
sock.listen(1)


while True:
    print("Wait a connection")
    conn, client_addr = sock.accept()
    try:
        print("connection from ", client_addr)
        while True:
            data = conn.recv(15)
            print("received ", data)
            if data:
                print("send back to client")
                conn.sendall(data)
            else:
                print("no data from ", client_addr)
                break
    finally:
        conn.close()

