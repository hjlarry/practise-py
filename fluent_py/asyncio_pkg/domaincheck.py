import asyncio
import socket
import sys
from keyword import kwlist
from collections.abc import Iterable, AsyncIterator
from typing import NamedTuple, Optional


class Result(NamedTuple):
    domain: str
    found: bool


OptionalLoop = Optional[asyncio.AbstractEventLoop]


async def probe(domain: str, loop: OptionalLoop = None) -> Result:
    if loop is None:
        loop = asyncio.get_running_loop()
    try:
        await loop.getaddrinfo(domain, None)
    except socket.gaierror:
        return Result(domain, False)
    return Result(domain, True)


async def multi_probe(domains: Iterable[str]) -> AsyncIterator[Result]:
    loop = asyncio.get_running_loop()
    coros = [probe(domain, loop) for domain in domains]
    for coro in asyncio.as_completed(coros):
        result = await coro
        yield result


async def main(tld: str) -> None:
    tld = tld.strip(".")
    names = (kw for kw in kwlist if len(kw) <= 4)
    domains = (f"{name}.{tld}" for name in names)
    print("Found\t\tNot Found")
    print("=====\t\t=========")
    async for domain, found in multi_probe(domains):
        indent = "" if found else "\t\t"
        print(f"{indent}{domain}")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        asyncio.run(main(sys.argv[1]))
    else:
        print("Please provide a TLD.", f"Example: {sys.argv[0]} COM.BR")
