import asyncio
import itertools
import sys
import time


async def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle("|/-\\"):
        status = char + " " + msg
        write(status)
        flush()
        # 使用退格符移回光标
        write("\x08" * len(status))
        try:
            await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            break
    write(" " * len(status) + "\x08" * len(status))


async def slow_function():
    # 假装io等待
    await asyncio.sleep(3)
    return 42


async def supervisor(loop):
    spinner = loop.create_task(spin("thinking"))
    print("spinner obj", spinner)
    result = await slow_function()
    spinner.cancel()
    return result


loop = asyncio.get_event_loop()
try:
    result = loop.run_until_complete(supervisor(loop))
finally:
    loop.close()
    print("Answer:", result)
