import asyncio
import logging
import sys
import ssl

SERVER_ADDRESS = ("localhost", 10000)
logging.basicConfig(
    level=logging.DEBUG, format="%(name)s: %(message)s", stream=sys.stderr
)
log = logging.getLogger("main")
event_loop = asyncio.get_event_loop()


async def echo(reader, writer):
    address = writer.get_extra_info("peername")
    log = logging.getLogger("Echo_{}_{}".format(*address))
    log.debug("connection accepted")
    while True:
        data = await reader.read(128)
        terminate = data.endswith(b'\x00')
        data = data.rstrip(b'\x00')
        if data:
            log.debug(f"received {data!r}")
            writer.write(data)
            await writer.drain()
            log.debug(f"sent {data!r}")
        if not data or terminate:
            log.debug("message terminated, closing")
            writer.close()
            return


ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.check_hostname = False
ssl_context.load_cert_chain('pymotw.crt', 'pymotw.key')

factory = asyncio.start_server(echo, *SERVER_ADDRESS, ssl=ssl_context)
server = event_loop.run_until_complete(factory)
log.debug(f"starting up on {SERVER_ADDRESS[0]} port {SERVER_ADDRESS[1]}")
try:
    event_loop.run_forever()
finally:
    log.debug("closing server")
    server.close()
    event_loop.run_until_complete(server.wait_closed())
    log.debug("closing event loop")
    event_loop.close()

