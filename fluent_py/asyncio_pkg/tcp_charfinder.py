import sys
import asyncio

from charfinder import UnicodeNameIndex

index = UnicodeNameIndex()
CRLF = b"\r\n"
PROMPT = b"?>"


async def handle_queries(reader, writer):
    while True:
        writer.write(PROMPT)
        await writer.drain()
        data = await reader.readline()
        try:
            query = data.decode().strip()
        except UnicodeDecodeError:
            query = "\x00"
        client = writer.get_extra_info("peername")
        print(f"Received from {client}:{query!r}")
        if query:
            if ord(query[:1]) < 32:
                break
            lines = list(index.find_description_strs(query))
            if lines:
                writer.writelines(line.encode() + CRLF for line in lines)
            writer.write(index.status(query, len(lines)).encode() + CRLF)
            await writer.drain()
            print(f"sent {len(lines)} results")
    print("Close the client socket")
    writer.close()


def main(address="127.0.0.1", port=2323):
    port = int(port)
    loop = asyncio.get_event_loop()
    server_coro = asyncio.start_server(handle_queries, address, port, loop=loop)
    server = loop.run_until_complete(server_coro)
    host = server.sockets[0].getsockname()
    print(f"Serving on {host}, ctrl+c to stop")
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    print("serving shut down")
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


main()
