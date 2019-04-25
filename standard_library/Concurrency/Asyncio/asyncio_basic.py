import asyncio
import time
import functools

print("一、 启动一个协程")


async def coroutine():
    print("in coroutine")


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(coroutine())
finally:
    event_loop.close()

print()
print("二、 得到协程的返回值")


async def coroutine_result():
    print("in coroutine")
    return 1234


event_loop = asyncio.new_event_loop()
try:
    result = event_loop.run_until_complete(coroutine_result())
    print(result)
finally:
    event_loop.close()

print()
print("三、 链接多个协程")


async def outter():
    result1 = await phase1()
    result2 = await phase2(result1)
    return result1, result2


async def phase1():
    return "hahha"


async def phase2(arg):
    return arg + "recived"


event_loop = asyncio.new_event_loop()
try:
    result = event_loop.run_until_complete(outter())
    print(result)
finally:
    event_loop.close()

print()
print("四、 立即回调")


def callback(arg, *, kwargs="default"):
    print(f"callback with {arg} and {kwargs}")


async def main(loop):
    print("registering callbacks")
    loop.call_soon(callback, 1)
    wrapped = functools.partial(callback, kwargs="not_default")
    loop.call_soon(wrapped, 2)
    await asyncio.sleep(1)


event_loop = asyncio.new_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()

print()
print("五、 延迟回调")


def callback1(n):
    print(f"callback with {n} ")


async def main1(loop):
    print("registering callbacks")
    loop.call_later(0.2, callback1, 1)
    loop.call_later(0.1, callback1, 2)
    loop.call_soon(callback1, 3)
    await asyncio.sleep(1)


event_loop = asyncio.new_event_loop()
try:
    event_loop.run_until_complete(main1(event_loop))
finally:
    event_loop.close()

print()
print("六、 在某个特定时间回调")


def callback2(n, loop):
    print(f"callback with {n} at {loop.time()} ")


async def main2(loop):
    # 必须是事件循环的时间, call_later实际上也是调用call_at
    now = loop.time()
    print("clock time ", time.time())
    print("loop time ", now)
    loop.call_at(0.2 + now, callback2, 1, loop)
    loop.call_at(0.1 + now, callback2, 2, loop)
    loop.call_soon(callback2, 3, loop)
    await asyncio.sleep(1)


event_loop = asyncio.new_event_loop()
try:
    event_loop.run_until_complete(main2(event_loop))
finally:
    event_loop.close()
