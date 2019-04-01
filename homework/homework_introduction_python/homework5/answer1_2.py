import aiohttp
import asyncio

loop = asyncio.get_event_loop()
session = aiohttp.ClientSession(loop=loop)


async def arange(i):
    n = 0
    while n < i:
        yield n
        n += 1


async def fetch(i):
    res = await session.get("http://httpbin.org/get?a=" + str(i))
    return await res.json()


async def result():
    async for i in arange(10):
        res = await fetch(i)
        print(res.get("args"))
        yield res


async def main():
    res = [res.get("args").get("a") async for res in result()]
    print(res)


loop.run_until_complete(main())
loop.close()
