import asyncio
import functools
import logging
import sys
import ssl

MESSAGES = [b"This is the message", b"it will be sent", b"a part"]
SERVER_ADDRESS = ("localhost", 10000)
logging.basicConfig(
    level=logging.DEBUG, format="%(name)s: %(message)s", stream=sys.stderr
)
log = logging.getLogger("main")
event_loop = asyncio.get_event_loop()


async def echo_client(address, messages):
    log = logging.getLogger("echo_client")
    log.debug("connection to {} on {}".format(*address))

    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ssl_context.check_hostname = False
    ssl_context.load_verify_locations("pymotw.crt")

    reader, writer = await asyncio.open_connection(*address, ssl=ssl_context)
    for msg in messages:
        writer.write(msg)
        log.debug(f"sending {msg!r}")
    # SSL does not support eof ,so send a null byte to indicate the end of the message
    writer.write(b"\x00")
    await writer.drain()
    log.debug("waiting for response")
    while True:
        data = await reader.read(128)
        if data:
            log.debug(f"received {data!r}")
        else:
            log.debug("closing")
            writer.close()
            return


try:
    event_loop.run_until_complete(echo_client(SERVER_ADDRESS, MESSAGES))
finally:
    log.debug("closing event loop")
    event_loop.close()
