import socket
import struct
import sys
import json
import time
from threading import Thread

HOST = '127.0.0.1'
PORT = 8003


class ChatClient:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.name = ''
        self.userlist = []

    def send_msg(self, msg):
        outgoing_data = struct.pack('>I', len(msg)) + bytes(msg, 'utf-8')
        self.sock.send(outgoing_data)

    def send_handle(self):
        while True:
            time.sleep(0.5)
            message = input(f'{self.name} >> ')
            self.send_msg(message)
            if message.startswith('/set'):
                self.name = message.split()[1]
            if message == '/quit':
                print('bye bye')
                sys.exit(0)

    def recv_handle(self):
        while True:
            res = self.sock.recv(1024)
            if res:
                res = res.decode('utf-8')
                print(res)
            if res.startswith('['):
                self.userlist = json.loads(res)
            time.sleep(1)

    def updata_user_list(self):
        while True:
            self.send_msg('/list')
            time.sleep(5)

    def run(self):
        threads = []

        while True:
            nickname = input('请输入名字:')
            if nickname:
                break
        self.send_msg(f'/set {nickname}')
        self.name = nickname

        for func in (self.recv_handle, self.send_handle):
            t = Thread(target=func)
            t.setDaemon(True)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()


if __name__ == '__main__':
    client = ChatClient(HOST, PORT)
    client.run()
