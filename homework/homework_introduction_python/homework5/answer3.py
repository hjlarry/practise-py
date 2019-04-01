import aiohttp
import asyncio

loop = asyncio.get_event_loop()
session = aiohttp.ClientSession(loop=loop)


async def fetch(i):
    res = await session.get("http://httpbin.org/get?a=" + str(i))
    return await res.json()


tasks = [asyncio.ensure_future(fetch(i)) for i in range(10)]
loop.run_until_complete(asyncio.wait(tasks))
result = [task.result().get("args").get("a") for task in tasks]
print(result)
loop.close()
