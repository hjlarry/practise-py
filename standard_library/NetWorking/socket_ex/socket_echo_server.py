import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ("localhost", 10000)
sock.bind(server_addr)

sock.listen(1)

while True:
    print("Wait a connection")
    conn, client_addr = sock.accept()
    try:
        print('connection from ', conn)
        while True:
            data = conn.recv(15)
            print('received ', data)
            if data:
                print('send back to client')
                conn.sendall(data)
            else:
                print('no data from ', client_addr)
                break
    finally:
        conn.close()

