import asyncio

print("*** Waiting for Multiple Coroutines")


async def phase(i):
    print("in phase", i)
    await asyncio.sleep(0.1 * i)
    print("done with phase", i)
    return f"phase result {i}"


async def main(num):
    print("main start")
    phases = [phase(i) for i in range(num)]
    print("wait phases complete")
    completed, pending = await asyncio.wait(phases)
    results = [t.result() for t in completed]
    print(results, 1)


event_loop = asyncio.get_event_loop()
try:
    print(1)
    event_loop.run_until_complete(main(3))
finally:
    event_loop.close()

print("*** Wait timeout")


async def phase1(i):
    print("in phase", i)
    try:
        await asyncio.sleep(0.1 * i)
    except asyncio.CancelledError:
        print("phase cancel", i)
        raise
    else:
        print("done with phase", i)
        return f"phase result {i}"


async def main1(num):
    print("main start")
    phases = [phase1(i) for i in range(num)]
    print("wait phases complete")
    completed, pending = await asyncio.wait(phases, timeout=0.1)
    print(f"{len(completed)} completed, {len(pending)} pending")
    if pending:
        print("to cancel tasks")
        for t in pending:
            t.cancel()
    print("exiting main")


event_loop = asyncio.new_event_loop()
try:
    print(1)
    event_loop.run_until_complete(main1(3))
finally:
    event_loop.close()


print("*** Gathering Results from Coroutines")
# gather比wait层次更高，切具备分组的功能
async def phase_1():
    print("in phase1")
    await asyncio.sleep(3)
    print("done with phase1")
    return f"phase result 1"


async def phase_2():
    print("in phase2")
    await asyncio.sleep(1)
    print("done with phase2")
    return f"phase result 2"


async def main2():
    result = await asyncio.gather(phase_1(), phase_2())
    print(result)


event_loop = asyncio.new_event_loop()
try:
    event_loop.run_until_complete(main2())
finally:
    event_loop.close()

print("*** Handling Background Operations as They Finish")


async def phase3(i):
    print("in phase", i)
    await asyncio.sleep((1 - 0.1 * i))
    print("done with phase", i)
    return f"phase result {i}"


async def main3(num):
    print("main start")
    phases = [phase3(i) for i in range(num)]
    print("wait phases complete")
    results = []
    for next_to_complete in asyncio.as_completed(phases):
        answer = await next_to_complete
        print("received ", answer)
        results.append(answer)
    print(results, 1)
    return results


event_loop = asyncio.new_event_loop()
try:
    event_loop.run_until_complete(main3(3))
finally:
    event_loop.close()
