import socket
import sys
import binascii
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ("localhost", 10000)
sock.bind(server_addr)

sock.listen(1)

unpacker = struct.Struct('I 3s f')

while True:
    print("Wait a connection")
    conn, client_addr = sock.accept()
    try:
        print('connection from ', conn)
        data = conn.recv(unpacker.size)
        print('received ', binascii.hexlify(data))
        print('unpacked ', unpacker.unpack(data))
            
    finally:
        conn.close()

