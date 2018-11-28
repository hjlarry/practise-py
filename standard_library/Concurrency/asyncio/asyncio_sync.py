import asyncio
import functools
import aiohttp

# 锁的意义，因为协程本身是单线程运行的，不需要数据间的同步，但考虑如下场景
# 如果有多个caller同时调用该协程，锁能保证http请求只发生一次
# 所以asyncio的锁和thread中的锁实现有很大不同
cache = {}


async def html_get(url, lock):
    async with lock:
        if url in cache:
            return cache[url]
        cache[url] = await aiohttp.get(url)
        return cache[url]


print("*** Locks")


def unlock(lock):
    print("callback release the lock")
    lock.release()


async def coro1(lock):
    print("coro1 wait the lock")
    with await lock:
        print("coro1 acquire lock")
    print("coro1 release lock")


async def coro2(lock):
    print("coro2 wait the lock")
    await lock
    try:
        print("coro2 acquire lock")
    finally:
        print("coro2 release lock")
        lock.release()


async def main(loop):
    lock = asyncio.Lock()
    await lock.acquire()
    print("lock acquired", lock.locked())

    # schedule a callback to unlock the lock
    loop.call_later(2, functools.partial(unlock, lock))

    await asyncio.wait([coro1(lock), coro2(lock)])


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()


print("*** Events")


def set_event(event):
    print("set event in callback ")
    event.set()


async def coro3(event):
    print("coro3 wait the event")
    await event.wait()
    print("coro3 triggled")


async def coro4(event):
    print("coro4 wait the event")
    await event.wait()
    print("coro4 triggled")


async def main2(loop):
    event = asyncio.Event()
    print("event state a", event.is_set())

    loop.call_later(2, functools.partial(set_event, event))

    await asyncio.wait([coro3(event), coro4(event)])
    print("event state b", event.is_set())


event_loop = asyncio.new_event_loop()
try:
    event_loop.run_until_complete(main2(event_loop))
finally:
    event_loop.close()

print("*** Conditions")


async def consumer(condition, n):
    with await condition:
        print(f"consumer {n} is waiting")
        await condition.wait()
        print(f"consumer {n} trigger")
    print(f"consumer {n} end")


async def manipulate_condition(condition):
    print("Starting manipulate")

    # wait for consumer start
    await asyncio.sleep(0.1)

    for i in range(1, 3):
        with await condition:
            print(f"notifying {i} consumers")
            condition.notify(n=i)
        await asyncio.sleep(2)
    with await condition:
        print("notifying remain consumers")
        condition.notify_all()


async def main3(loop):
    condition = asyncio.Condition()
    consumers = [consumer(condition, i) for i in range(5)]
    loop.create_task(manipulate_condition(condition))
    await asyncio.wait(consumers)


event_loop = asyncio.new_event_loop()
try:
    event_loop.run_until_complete(main3(event_loop))
finally:
    event_loop.close()


print("*** Queues")


async def consumer1(n, q):
    print(f"consumer {n} starting")
    while True:
        print(f"consumer {n} wait for item")
        item = await q.get()
        print(f"consumer {n} get {item}")
        if item is None:
            # None is the signal to stop.
            q.task_done()
            break
        else:
            await asyncio.sleep(0.01 * item)
            q.task_done()
    print(f"consumer {n} end")


async def producer1(q, num_workers):
    print("producer starting")
    # Add some numbers to the queue to simulate jobs
    for i in range(num_workers * 3):
        await q.put(i)
        print(f"producer add task {i} to queue")

    print("producer add stop signal to queue")
    for i in range(num_workers):
        await q.put(None)
    print("producer wait for queue to empty")
    await q.join()
    print("producer ending")


async def main4(loop, num_consumers):
    q = asyncio.Queue(maxsize=num_consumers)
    consumers = [loop.create_task(consumer1(i, q)) for i in range(num_consumers)]
    prod = loop.create_task(producer1(q, num_consumers))
    await asyncio.wait(consumers + [prod])


event_loop = asyncio.new_event_loop()
try:
    event_loop.run_until_complete(main4(event_loop, 2))
finally:
    event_loop.close()
