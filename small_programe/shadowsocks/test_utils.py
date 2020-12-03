import unittest
import random
import base64
import socket
import asyncio

from utils import (
    randomPwd,
    validatePwd,
    dumpsPwd,
    loadsPwd,
    InvalidPasswordErr,
    IDENTITY_PASSWORD,
    Cipher,
    SecureSocket,
)


class TestPassword(unittest.TestCase):
    def test_randomPassword(self):
        for idx in range(0xFF):
            with self.subTest(idx):
                password = randomPwd()
                isValid = validatePwd(password)
                self.assertTrue(isValid)

    def test_dumps_and_loads_succeed(self):
        password = randomPwd()
        string = dumpsPwd(password)
        loaded_password = loadsPwd(string)
        self.assertEqual(password, loaded_password)

    def test_dumps_and_loads_fail(self):
        password = randomPwd()
        password[random.randint(1, 255)] = 0
        with self.assertRaises(InvalidPasswordErr):
            dumpsPwd(password)

        string = base64.encodebytes(password).decode("utf8", errors="strict")
        with self.assertRaises(InvalidPasswordErr):
            loadsPwd(string)

        password = randomPwd()
        password = password[:-2]
        with self.assertRaises(InvalidPasswordErr):
            dumpsPwd(password)

        string = dumpsPwd(IDENTITY_PASSWORD)
        string = string[:-3]
        with self.assertRaises(InvalidPasswordErr):
            loadsPwd(string)


class TestCipher(unittest.TestCase):
    def test_encryption(self):
        password = randomPwd()
        original_data = bytearray()
        for _ in range(0xFFFF):
            original_data.append(random.randint(0, 255))
        cipher = Cipher.NewCipher(password)
        data = original_data.copy()

        cipher.encode(data)
        self.assertNotEqual(data, original_data)
        cipher.decode(data)
        self.assertEqual(data, original_data)

    def test_no_encryption(self):
        password = IDENTITY_PASSWORD.copy()
        original_data = bytearray()
        for _ in range(0xFFFF):
            original_data.append(random.randint(0, 255))
        cipher = Cipher.NewCipher(password)
        data = original_data.copy()

        cipher.encode(data)
        self.assertEqual(data, original_data)
        cipher.decode(data)
        self.assertEqual(data, original_data)


class TestSecuresocket(unittest.TestCase):
    def setUp(self):
        self.ls_local, self.ls_server = socket.socketpair()
        password = randomPwd()
        self.loop = asyncio.new_event_loop()
        self.cipher = Cipher.NewCipher(password)
        self.securesocket = SecureSocket(loop=self.loop, cipher=self.cipher)
        self.msg = bytearray(b"hello world")
        self.encripted_msg = self.msg.copy()
        self.cipher.encode(self.encripted_msg)

    def tearDown(self):
        self.loop.close()
        self.ls_local.close()
        self.ls_server.close()

    def test_decodeRead(self):
        self.ls_local.send(self.encripted_msg)
        self.ls_server.setblocking(False)
        received_msg = self.loop.run_until_complete(
            self.securesocket.decodeRead(self.ls_server)
        )

        self.assertEqual(received_msg, self.msg)

    def test_encodeWrite(self):
        self.ls_local.setblocking(False)
        self.loop.run_until_complete(
            self.securesocket.encodeWrite(self.ls_local, self.msg)
        )
        received_msg = self.ls_server.recv(1024)

        self.assertEqual(bytearray(received_msg), self.encripted_msg)

    def test_decodeCopy(self):
        dstServer, ls_server_conn = socket.socketpair()
        ls_server_conn.setblocking(False)
        self.ls_server.setblocking(False)
        self.ls_local.sendall(self.encripted_msg * 10)
        self.ls_local.close()
        self.loop.run_until_complete(
            self.securesocket.decodeCopy(ls_server_conn, self.ls_server)
        )
        received_msg = dstServer.recv(1024)

        self.assertEqual(bytearray(received_msg), self.msg * 10)

        dstServer.close()
        ls_server_conn.close()

    def test_encodeCopy(self):
        user_client, ls_local_conn = socket.socketpair()
        ls_local_conn.setblocking(False)
        self.ls_local.setblocking(False)
        user_client.sendall(self.msg * 10)
        user_client.close()
        self.loop.run_until_complete(
            self.securesocket.encodeCopy(self.ls_local, ls_local_conn)
        )
        received_msg = self.ls_server.recv(1024)

        self.assertEqual(bytearray(received_msg), self.encripted_msg * 10)

        ls_local_conn.close()