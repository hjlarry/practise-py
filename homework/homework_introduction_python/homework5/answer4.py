import aiohttp
import asyncio
import random

loop = asyncio.get_event_loop()
session = aiohttp.ClientSession(loop=loop)


async def fetch(i):
    res = await session.get("http://httpbin.org/get?a=" + str(i), timeout=1)
    return await res.json()


async def _produce(queue):
    for num in random.sample(range(100), 5):
        print("producing {}".format(num))
        item = (num, num)
        await queue.put(item)


async def produce(queue):
    await _produce(queue)
    await asyncio.sleep(5)
    await _produce(queue)


async def consume(queue):
    while 1:
        item = await queue.get()
        num = item[0]
        try:
            rs = await fetch(num)
            print("consuming {}...".format(rs))
        except aiohttp.client_exceptions.ClientConnectorError:
            print("back time too long")
            await queue.put((num, num))
        queue.task_done()


async def run():
    queue = asyncio.PriorityQueue()
    consumer = asyncio.ensure_future(consume(queue))
    await produce(queue)
    await queue.join()
    consumer.cancel()


loop.run_until_complete(run())
loop.close()
