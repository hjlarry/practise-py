import asyncio
import socket
import unittest

from local import Local
from utils import randomPwd, Cipher


class TestLocal(unittest.TestCase):
    def setUp(self):
        self.listenAddr = ("127.0.0.1", 11111)
        self.remoteAddr = ("127.0.0.1", 22222)
        self.remoteServer = socket.socket()
        self.remoteServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.remoteServer.bind(self.remoteAddr)
        self.remoteServer.listen(socket.SOMAXCONN)
        self.remoteServer.setblocking(False)
        pwd = randomPwd()
        self.cipher = Cipher.NewCipher(pwd)
        self.loop = asyncio.new_event_loop()
        self.local = Local(
            loop=self.loop,
            pwd=pwd,
            listenAddr=self.listenAddr,
            remoteAddr=self.remoteAddr,
        )
        self.msg = bytearray(b"hello world")
        self.encrypted_msg = self.msg.copy()
        self.cipher.encode(self.encrypted_msg)

    def tearDown(self):
        self.remoteServer.close()
        self.loop.close()

    def test_dialRemote(self):
        async def test():
            with await self.local.dialRemote() as connection:
                await self.loop.sock_sendall(connection, self.msg)
                remoteConn, _ = await self.loop.sock_accept(self.remoteServer)
                received_msg = await self.loop.sock_recv(remoteConn, 1024)
                remoteConn.close()
                self.assertEqual(received_msg, self.msg)

        self.loop.run_until_complete(test())

        with self.assertRaises(ConnectionError):
            self.local.remoteAddr = ("127.0.0.1", 0)
            self.loop.run_until_complete(self.local.dialRemote())

    def test_run(self):
        def didListen(address):
            self.assertEqual(address[0], self.listenAddr[0])
            self.assertEqual(address[1], self.listenAddr[1])
            user_client = socket.create_connection(self.listenAddr)
            user_client.send(b"hello world")
            user_client.close()

            async def call_later():
                conn, _ = await self.loop.sock_accept(self.remoteServer)
                with conn:
                    received_msg = await self.loop.sock_recv(conn, 1024)
                await asyncio.sleep(0.001)
                self.assertEqual(received_msg, self.encrypted_msg)
                self.loop.stop()

            asyncio.ensure_future(call_later(), loop=self.loop)

        with self.assertRaises(RuntimeError):
            self.loop.run_until_complete(self.local.listen(didListen))