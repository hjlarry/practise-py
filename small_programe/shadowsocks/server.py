"""
ss-server 的职责是在墙外服务器启动和监听一个服务，该服务监听来自本机的 ss-local 的请求
在收到来自 ss-local 转发过来的数据时，会先根据用户配置的加密方法和密码对数据进行对称解密，以获得加密后的数据的原内容
同时还会解 SOCKS5 协议，读出本次请求真正的目标服务地址(例如Google服务器地址)，再把解密后得到的原数据转发到真正的目标服务
python3 server.py
控制台输出用于local的密码
"""

import asyncio
import socket
import typing
import logging

from utils import SecureSocket, Cipher, randomPwd, dumpsPwd

logger = logging.getLogger(__name__)


class Server(SecureSocket):
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        pwd: bytearray,
        listenAddr: tuple,
    ) -> None:
        super().__init__(loop=loop, cipher=Cipher.NewCipher(pwd))
        self.listenAddr = listenAddr

    async def listen(self, didListen: typing.Callable = None) -> None:
        """运行服务端监听来自本地代理客户端的请求"""
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
        """处理来自ss-local的数据"""
        """
        先解socks5协议， https://www.ietf.org/rfc/rfc1928.txt
        客户端的请求数据:
        +----+----------+----------+
        |VER | NMETHODS | METHODS  |
        +----+----------+----------+
        | 1  |    1     | 1 to 255 |
        +----+----------+----------+
        """
        buf = await self.decodeRead(conn)
        if not buf or buf[0] != 0x05:
            conn.close()
            return
        """
        服务端需返回:
        +----+--------+
        |VER | METHOD |
        +----+--------+
        | 1  |   1    |
        +----+--------+
        """
        await self.encodeWrite(conn, bytearray((0x05, 0x00)))
        """
        接着客户端请求:
        +----+-----+-------+------+----------+----------+
        |VER | CMD |  RSV  | ATYP | DST.ADDR | DST.PORT |
        +----+-----+-------+------+----------+----------+
        | 1  |  1  | X'00' |  1   | Variable |    2     |
        +----+-----+-------+------+----------+----------+
        """
        buf = await self.decodeRead(conn)
        if len(buf) < 7 or buf[1] != 0x01:
            conn.close()
            return

        dstIP = None
        dstPort = int(buf[-2:].hex(), 16)
        dstFamily = None
        if buf[3] == 0x01:  # ipv4
            dstIP = socket.inet_ntop(socket.AF_INET, buf[4:8])
            dstFamily = socket.AF_INET
        elif buf[3] == 0x03:  # domain
            dstIP = buf[5:-2].decode()
        elif buf[3] == 0x04:  # ipv6
            dstIP = socket.inet_ntop(socket.AF_INET6, buf[4:20])
            dstFamily = socket.AF_INET6
        else:
            conn.close()
            return

        # 尝试连接目标服务器
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

        """
        返回连接目标服务器的结果:
        +----+-----+-------+------+----------+----------+
        |VER | REP |  RSV  | ATYP | BND.ADDR | BND.PORT |
        +----+-----+-------+------+----------+----------+
        | 1  |  1  | X'00' |  1   | Variable |    2     |
        +----+-----+-------+------+----------+----------+
        """
        await self.encodeWrite(
            conn,
            bytearray((0x05, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)),
        )

        # 数据转发
        conn2dst = asyncio.ensure_future(self.decodeCopy(dstServer, conn))
        dst2conn = asyncio.ensure_future(self.encodeCopy(conn, dstServer))
        task = asyncio.ensure_future(
            asyncio.gather(conn2dst, dst2conn, loop=self.loop, return_exceptions=True)
        )

        def cleanup():
            dstServer.close()
            conn.close()

        task.add_done_callback(cleanup)


def run_server():
    loop = asyncio.get_event_loop()
    listenAddr = ("0.0.0.0", 8388)
    pwd = randomPwd()
    server = Server(loop=loop, pwd=pwd, listenAddr=listenAddr)

    def didListen(address):
        print("Listen to %s:%d\n" % address)
        print(f"password is {dumpsPwd(pwd)}")

    asyncio.ensure_future(server.listen(didListen))
    loop.run_forever()


if __name__ == "__main__":
    run_server()