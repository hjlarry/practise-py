# usage: netcat 127.0.0.1 2323
import asyncio
import functools
from typing import cast
from asyncio.trsock import TransportSocket

from charindex import InvertedIndex, format_results

CRLF = b"\r\n"
PROMPT = b"?>"


async def finder(
    index: InvertedIndex, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    client = writer.get_extra_info("peername")
    while True:
        writer.write(PROMPT)
        await writer.drain()
        data = await reader.readline()
        if not data:
            break
        try:
            query = data.decode().strip()
        except UnicodeDecodeError:
            query = "\x00"
        print(f"Received from {client}:{query!r}")
        if query:
            if ord(query[:1]) < 32:
                break
            results = await search(query, index, writer)
            print(f"sent to {client}: {results} results")

    writer.close()
    await writer.wait_closed()
    print("Close the client {client}")


async def search(query: str, index: InvertedIndex, writer: asyncio.StreamWriter) -> int:
    chars = index.search(query)
    lines = (line.encode() + CRLF for line in format_results(chars))
    writer.writelines(lines)
    await writer.drain()
    writer.write(f"{'-'*66}".encode() + CRLF + f"{len(chars)} founded".encode() + CRLF)
    await writer.drain()
    return len(chars)


async def supervisor(index: InvertedIndex, host: str, port: int) -> None:
    server = await asyncio.start_server(functools.partial(finder, index), host, port)
    socket_list = cast(tuple[TransportSocket, ...], server.sockets)
    addr = socket_list[0].getsockname()
    print(f"Serving on {addr}. Hit Ctrl-C to Stop")
    await server.serve_forever()


def main(host: str = "127.0.0.1", port_arg: str = "2323"):
    port = int(port_arg)
    print("Building Index.")
    index = InvertedIndex()
    try:
        asyncio.run(supervisor(index, host, port))
    except KeyboardInterrupt:
        print("serving shut down")


if __name__ == "__main__":
    main()
