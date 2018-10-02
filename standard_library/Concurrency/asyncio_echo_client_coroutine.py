import asyncio
import functools
import logging
import sys

MESSAGES = [b'This is the message', b'it will be sent', b'a part']
SERVER_ADDRESS = ("localhost", 10000)
logging.basicConfig(
    level=logging.DEBUG, format="%(name)s: %(message)s", stream=sys.stderr
)
log = logging.getLogger("main")
event_loop = asyncio.get_event_loop()


async def echo_client():
    pass

client_completed = asyncio.Future()
client_factory = functools.partial(EchoClient, messages=MESSAGES, future=client_completed)
factory_cor = event_loop.create_connection(client_factory, *SERVER_ADDRESS)

log.debug('waiting for client to complete')
try:
    event_loop.run_until_complete(factory_cor)
    event_loop.run_until_complete(client_completed)
finally:
    log.debug('closing event loop')
    event_loop.close()
    