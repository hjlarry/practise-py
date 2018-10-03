import socket
import sys
import struct
import binascii

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ("localhost", 10000)
sock.connect(server_addr)

values = (1, b'abc', 2.7)
packer = struct.Struct('I 3s f')
packer_data = packer.pack(*values)

try:
    print('values ', values)
    print('sending ', binascii.hexlify(packer_data))
    sock.sendall(packer_data)
finally:
    print('closing')
    sock.close()

