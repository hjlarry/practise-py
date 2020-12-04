import asyncio
import typing
import socket
import logging

from utils import SecureSocket, Cipher

logger = logging.getLogger(__name__)


class Local(SecureSocket):
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        pwd: bytearray,
        listenAddr: str,
        remoteAddr: str,
    ) -> None:
        super().__init__(loop=loop, cipher=Cipher.NewCipher(pwd))
        self.listenAddr = listenAddr
        self.remoteAddr = remoteAddr

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
        remoteServer = await self.dialRemote()
        local2remote = asyncio.ensure_future(self.decodeCopy(conn, remoteServer))
        remote2local = asyncio.ensure_future(self.encodeCopy(remoteServer, conn))
        task = asyncio.ensure_future(
            asyncio.gather(
                local2remote, remote2local, loop=self.loop, return_exceptions=True
            )
        )

        def cleanup():
            remoteServer.close()
            conn.close()

        task.add_done_callback(cleanup)

    async def dialRemote(self) -> socket.socket:
        remoteConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remoteConn.setblocking(False)
        try:
            await self.loop.sock_connect(remoteConn, self.remoteAddr)
        except Exception as e:
            raise ConnectionError(
                f"connect to remote server {self.remoteAddr} err: {e} "
            )
        return remoteConn
