import random
import base64
import asyncio
import logging
import socket

IDENTITY_PASSWORD = bytearray(range(256))
logger = logging.getLogger(__name__)


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
    if not validatePwd(pwd):
        raise InvalidPasswordErr
    return base64.urlsafe_b64encode(pwd).decode("utf8", errors="strict")


def randomPwd() -> bytearray:
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
        decodePwd = encodePwd.copy()
        for i, v in enumerate(encodePwd):
            decodePwd[v] = i
        return cls(encodePwd, decodePwd)


class SecureSocket:
    def __init__(self, loop: asyncio.AbstractEventLoop, cipher: Cipher) -> None:
        self.loop = loop or asyncio.get_event_loop()
        self.cipher = cipher

    async def decodeRead(self, conn: socket.socket) -> bytearray:
        data = await self.loop.sock_recv(conn, 1024)
        logger.debug(f"{conn.getsockname()} decodeRead {data}")
        bs = bytearray(data)
        self.cipher.decode(bs)
        return bs

    async def encodeWrite(self, conn: socket.socket, bs: bytearray) -> None:
        logger.debug(f"{conn.getsockname()} encodeWrite {bytes(bs)}")
        bs = bs.copy()
        self.cipher.encode(bs)
        await self.loop.sock_sendall(conn, bs)

    async def encodeCopy(self, dst: socket.socket, src: socket.socket) -> None:
        logger.debug(f"{dst.getsockname()} encodeCopy to  {src.getsockname()}")
        while True:
            data = await self.loop.sock_recv(src, 1024)
            if not data:
                break
            await self.encodeWrite(dst, bytearray(data))

    async def decodeCopy(self, dst: socket.socket, src: socket.socket) -> None:
        logger.debug(f"{dst.getsockname()} decodeCopy to  {src.getsockname()}")
        while True:
            bs = await self.decodeRead(src)
            if not bs:
                break
            await self.loop.sock_sendall(dst, bs)