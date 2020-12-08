from __future__ import annotations
import random
import base64
import asyncio
import socket


IDENTITY_PASSWORD = bytearray(range(256))


class InvalidPasswordErr(Exception):
    pass


def validatePwd(pwd: bytearray) -> bool:
    return len(pwd) == 256 and len(set(pwd)) == 256


def loadsPwd(pwd: str) -> bytearray:
    try:
        pwd = base64.urlsafe_b64decode(pwd.encode("utf8", errors="strict"))
        pwd = bytearray(pwd)
    except:
        raise InvalidPasswordErr

    if not validatePwd(pwd):
        raise InvalidPasswordErr

    return pwd


def dumpsPwd(pwd: bytearray) -> str:
    """密码字节数组转为字符串，便于用户使用"""
    if not validatePwd(pwd):
        raise InvalidPasswordErr
    return base64.urlsafe_b64encode(pwd).decode("utf8", errors="strict")


def randomPwd() -> bytearray:
    """生成随机字节数组，这个数组由0~255这些数字组成，长度固定256"""
    pwd = IDENTITY_PASSWORD.copy()
    random.shuffle(pwd)
    return pwd


class Cipher:
    def __init__(self, encodePwd: bytearray, decodePwd: bytearray) -> None:
        self.encodePwd = encodePwd.copy()
        self.decodePwd = decodePwd.copy()

    def encode(self, bs: bytearray) -> None:
        for i, v in enumerate(bs):
            bs[i] = self.encodePwd[v]

    def decode(self, bs: bytearray) -> None:
        for i, v in enumerate(bs):
            bs[i] = self.decodePwd[v]

    @classmethod
    def NewCipher(cls, encodePwd: bytearray) -> Cipher:
        """
        编码的密码和解码的密码是一组反函数，例如密钥为:
        0   1   2   3   4   5   ...
        186 118 82  201 235 236 ...
        如果原数据为[5, 0, 1, 2, 3]，则加密后为[236,186,118,82,201]，同理也可以解密回来
        """
        decodePwd = encodePwd.copy()
        for i, v in enumerate(encodePwd):
            decodePwd[v] = i
        return cls(encodePwd, decodePwd)


class SecureSocket:
    """加密传输的socket"""

    def __init__(self, loop: asyncio.AbstractEventLoop, cipher: Cipher) -> None:
        self.loop = loop or asyncio.get_event_loop()
        self.cipher = cipher

    async def decodeRead(self, conn: socket.socket) -> bytearray:
        """从conn里读取加密过的数据，然后解密放在bs字节数组中"""
        data = await self.loop.sock_recv(conn, 1024)
        print(f"{conn.getsockname()} decodeRead {data}")
        bs = bytearray(data)
        self.cipher.decode(bs)
        return bs

    async def encodeWrite(self, conn: socket.socket, bs: bytearray) -> None:
        """把bs字节数组中的数据加密后通过conn发送出去"""
        print(f"{conn.getsockname()} encodeWrite {bytes(bs)}")
        bs = bs.copy()
        self.cipher.encode(bs)
        await self.loop.sock_sendall(conn, bs)

    async def encodeCopy(self, dst: socket.socket, src: socket.socket) -> None:
        """不断从src中读取数据，然后加密后写入dst"""
        print(f"{dst.getsockname()} encodeCopy to  {src.getsockname()}")
        while True:
            data = await self.loop.sock_recv(src, 1024)
            if not data:
                break
            await self.encodeWrite(dst, bytearray(data))

    async def decodeCopy(self, dst: socket.socket, src: socket.socket) -> None:
        """不断从src中读取数据，然后解密，再发送至dst中"""
        print(f"{dst.getsockname()} decodeCopy to  {src.getsockname()}")
        while True:
            bs = await self.decodeRead(src)
            if not bs:
                break
            await self.loop.sock_sendall(dst, bs)