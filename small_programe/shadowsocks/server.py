import asyncio
import socket
import typing
import logging

from utils import SecureSocket, Cipher

logger = logging.getLogger(__name__)


class Server(SecureSocket):
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        pwd: bytearray,
        listenAddr: str,
    ) -> None:
        super().__init__(loop=loop, cipher=Cipher.NewCipher(pwd))
        self.listenAddr = listenAddr

    async def listen(self, didListen: typing.Callable = None) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind(self.listenAddr)
            listener.listen(socket.SOMAXCONN)
            listener.setblocking(False)

            logger.info(f"Listen to {self.listenAddr}")
            if didListen:
                didListen(listener.getsockname())

            while True:
                conn, addr = await self.loop.sock_accept(listener)
                logger.info(f"Receive {addr}")
                asyncio.ensure_future(self.handleConn(conn))

    async def handleConn(self, conn: socket.socket) -> None:
        buf = await self.decodeRead(conn)
        if not buf or buf[0] != 0x05:
            conn.close()
            return

        await self.encodeWrite(conn, bytearray((0x05, 0x00)))

        buf = await self.decodeRead(conn)
        if len(buf) < 7 or buf[1] != 0x01:
            conn.close()
            return

        dstIP = None
        dstPort = int(buf[-2:].hex(), 16)
        dstFamily = None
        if buf[3] == 0x01:
            dstIP = socket.inet_ntop(socket.AF_INET, buf[4:8])
            dstFamily = socket.AF_INET
        elif buf[3] == 0x03:
            dstIP = buf[5:-2].decode()
        elif buf[3] == 0x04:
            dstIP = socket.inet_ntop(socket.AF_INET6, buf[4:20])
            dstFamily = socket.AF_INET6
        else:
            conn.close()
            return

        dstServer = None
        if dstFamily:
            dstServer = socket.socket(family=dstFamily, type=socket.SOCK_STREAM)
            dstServer.setblocking(False)
            try:
                await self.loop.sock_connect(dstServer, (dstIP, dstPort))
            except OSError:
                dstServer.close()
                dstServer = None
        else:
            for res in await self.loop.getaddrinfo(dstIP, dstPort):
                dstFamily, sockettype, proto, _, dstAddress = res
                dstServer = socket.socket(dstFamily, sockettype, proto)
                dstServer.setblocking(False)
                try:
                    await self.loop.sock_connect(dstServer, dstAddress)
                    break
                except OSError:
                    dstServer.close()
                    dstServer = None
        if dstServer is None:
            return

        await self.encodeWrite(
            conn,
            bytearray((0x05, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)),
        )

        conn2dst = asyncio.ensure_future(self.decodeCopy(dstServer, conn))
        dst2conn = asyncio.ensure_future(self.encodeCopy(conn, dstServer))
        task = asyncio.ensure_future(
            asyncio.gather(conn2dst, dst2conn, loop=self.loop, return_exceptions=True)
        )

        def cleanup():
            dstServer.close()
            conn.close()

        task.add_done_callback(cleanup)
