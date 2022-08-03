import asyncio

loop = asyncio.get_event_loop()


class ForwardProtocol(asyncio.Protocol):
    def __init__(self, peer):
        self.peer = peer
        self.transport = None
        self.buffer = []

    def connection_made(self, transport):
        peername = transport.get_extra_info("peername")
        print("Connection from {}".format(peername))
        self.transport = transport
        if len(self.buffer):
            self.transport.writelines(self.buffer)

    def data_received(self, data):
        message = data.decode()
        print("Data received: {!r}".format(message))
        self.peer.write(data)

    def connection_lost(self, exc):
        print("Close the client socket")
        self.peer.close()


class PortForward(asyncio.Protocol):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connection_made(self, transport):
        self.conn = ForwardProtocol(transport)
        coro = loop.create_connection(lambda: self.conn, self.host, self.port)
        asyncio.ensure_future(coro)

    def data_received(self, data):
        data = data.decode().replace("localhost:8888", "httpbin.org").encode()

        print("Request:", data.decode())
        if not self.conn.transport:
            self.conn.buffer.append(data)
        else:
            self.conn.transport.write(data)

    def connection_lost(self, exc):
        self.conn.transport.close()


# Each client connection will create a new protocol instance
coro = loop.create_server(lambda: PortForward("httpbin.org", 80), "127.0.0.1", 8888)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print("Serving on {}".format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
