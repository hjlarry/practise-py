import socket
from urllib.parse import urlparse
import asyncio
import time


async def get_url(url):
    url = urlparse(url)
    host = url.netloc
    path = url.path
    if path == "":
        path = "/"

    reader, writer = await asyncio.open_connection(host, 80)
    writer.write(
        f"GET {path} HTTP/1.1\r\nHost:{host}\r\nConnection:close\r\n\r\n".encode("utf8")
    )
    all_lines = []
    async for line in reader:
        all_lines.append(line.decode("utf-8"))
    return "\n".join(all_lines)


async def main():
    tasks = []
    for i in range(20):
        url = f"http://shop.projectsedu.com/goods/{i}/"
        tasks.append(get_url(url))
    for task in asyncio.as_completed(tasks):
        result = await task
        print(result)


start = time.time()
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.close()
    print(time.time() - start)
