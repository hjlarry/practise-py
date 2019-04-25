import asyncio

print("*** Starting a Task")


async def task_func():
    print("exe task")
    return "task_result"


async def main(loop):
    print("create task")
    task = loop.create_task(task_func())
    return_value = await task
    print(return_value)


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()


print("*** Canceling a Task")


async def task_func1():
    print("exe task")
    return "task_result"


async def main1(loop):
    print("create task")
    task = loop.create_task(task_func1())
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("canceled task")
    else:
        print(task.result())


event_loop = asyncio.new_event_loop()
try:
    event_loop.run_until_complete(main1(event_loop))
finally:
    event_loop.close()


print("*** Canceling a Task example2")


async def task_func2():
    print("in task func, sleeping")
    try:
        await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("task_func cancelled", 3)
        raise
    return "task_result"


def task_cancel2(t):
    print("in task_cancel")
    t.cancel()
    print("task_cancel", 2)


async def main2(loop):
    print("create task")
    task = loop.create_task(task_func2())
    loop.call_soon(task_cancel2, task)
    try:
        await task
    except asyncio.CancelledError:
        print("main also cancel", 4)
    else:
        print(task.result())


event_loop = asyncio.new_event_loop()
try:
    event_loop.run_until_complete(main2(event_loop))
finally:
    event_loop.close()


print("*** Creating Tasks from Coroutines")


async def wrapped():
    print(5)
    return "result-wrapped"


async def inner(task):
    print(4)
    print("inner", task)
    result = await task
    print("task return ", result)


async def starter():
    print(2)
    # 实际源码内也调用了create_task
    task = asyncio.ensure_future(wrapped())
    print(3)
    await inner(task)
    print(6)


event_loop = asyncio.new_event_loop()
try:
    print(1)
    event_loop.run_until_complete(starter())
finally:
    event_loop.close()


print("*** Canceling Tasks with ctrl-c")


async def get_html(t):
    print("get html started")
    await asyncio.sleep(t)
    print("get html done")
    return 1


task1 = get_html(2)
task2 = get_html(3)
task3 = get_html(3)
tasks = [task1, task2, task3]
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    loop.run_until_complete(asyncio.wait(tasks))
except KeyboardInterrupt as e:
    print("cancel tasks")
    all_tasks = asyncio.Task.all_tasks()
    for task in all_tasks:
        print(task.cancel())
    loop.stop()
    loop.run_forever()
finally:
    loop.close()
