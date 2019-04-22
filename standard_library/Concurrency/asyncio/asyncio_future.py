import asyncio
import functools

print("一、 Future对象")


def mark_done(future, result):
    print(f"setting future result for {result!r}")
    future.set_result(result)


event_loop = asyncio.get_event_loop()
try:
    all_done = asyncio.Future()
    print("scheduling mark_done")
    event_loop.call_soon(mark_done, all_done, "the result111")
    result = event_loop.run_until_complete(all_done)
    print("return result", result)
finally:
    event_loop.close()
print("final result ", all_done.result())

print()
print("二、 await Future对象")


def mark_done1(future, result):
    print(f"setting future result for {result!r}")
    future.set_result(result)


async def main1(loop):
    all_done = asyncio.Future()
    print("scheduling mark_done")
    loop.call_soon(mark_done1, all_done, "the result222")
    result = await all_done
    print("return result", result)


event_loop = asyncio.new_event_loop()
try:
    event_loop.run_until_complete(main1(event_loop))
finally:
    event_loop.close()


print()
print("三、 为Future添加回调函数")


def callback(future, n):
    print(f"{n}: future done: {future.result()}")


async def reg_callbacks(all_done):
    all_done.add_done_callback(functools.partial(callback, n=1))
    all_done.add_done_callback(functools.partial(callback, n=3))


async def main2(all_done):
    await reg_callbacks(all_done)
    all_done.set_result("sdasdsa")


event_loop = asyncio.new_event_loop()
# 这里必须set_event_loop才不会出错  而其他地方没有这个问题
asyncio.set_event_loop(event_loop)
try:
    all_done = asyncio.Future()
    event_loop.run_until_complete(main2(all_done))
finally:
    event_loop.close()
