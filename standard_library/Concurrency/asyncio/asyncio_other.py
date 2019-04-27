import asyncio
import logging
import socket
import sys
import signal
import os
import functools
import time
import concurrent.futures


print("一、 和DNS服务器交互")
TARGETS = [
    ("pymotw.com", "https"),
    ("doughellmann.com", "https"),
    ("python.org", "https"),
]


async def main(loop, targets):
    for target in targets:
        info = await loop.getaddrinfo(*target, proto=socket.IPPROTO_TCP)
        print(info)


event = asyncio.get_event_loop()
try:
    event.run_until_complete(main(event, TARGETS))
finally:
    event.close()


TARGETS1 = [("66.33.211.242", 443), ("104.130.43.121", 443)]


async def main1(loop, targets):
    for target in targets:
        info = await loop.getnameinfo(target)
        print(info)


event = asyncio.new_event_loop()
try:
    event.run_until_complete(main1(event, TARGETS1))
finally:
    event.close()

print()
print("二、 接收Unix信号")


def signal_handle(name):
    print(f"signal_handler{name!r}")


event_loop = asyncio.new_event_loop()
event_loop.add_signal_handler(
    signal.SIGHUP, functools.partial(signal_handle, name="SIGHUP")
)
event_loop.add_signal_handler(
    signal.SIGUSR1, functools.partial(signal_handle, name="SIGUSR1")
)
event_loop.add_signal_handler(
    signal.SIGINT, functools.partial(signal_handle, name="SIGINT")
)


async def send_signals():
    pid = os.getpid()
    print("Starting send_signal for ", pid)
    for name in ["SIGHUP", "SIGHUP", "SIGUSR1", "SIGINT"]:
        print("sending ", name)
        os.kill(pid, getattr(signal, name))
        # yielding control to allow the signal handler to run ,
        # since the signal does not interrupt the program flow otherwise.
        print("yielding control")
        await asyncio.sleep(0.1)
    return


try:
    event_loop.run_until_complete(send_signals())
finally:
    event_loop.close()

print()
print("三、协程结合多线程多进程")
print("【ThreadPoolExecutor】")


def blocks(n):
    log = logging.getLogger(f"blocks({n})")
    log.info("running")
    time.sleep(0.1)
    log.info("done")
    return n ** 2


async def run_blocking_tasks(executor):
    log = logging.getLogger("run_blocking_tasks")
    log.info("starting")
    log.info("create executor tasks")
    loop = asyncio.get_event_loop()
    blocking_tasks = [loop.run_in_executor(executor, blocks, i) for i in range(6)]
    log.info("waiting executor tasks")
    completed, pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    log.info("results:{!r}".format(results))
    log.info("exiting")


logging.basicConfig(
    level=logging.INFO,
    format="%(threadName)10s %(name)18s: %(message)s",
    stream=sys.stderr,
)
executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
event_loop = asyncio.new_event_loop()
try:
    event_loop.run_until_complete(run_blocking_tasks(executor))
finally:
    event_loop.close()

print()
print("【ProcessPoolExecutor】")


def blocks1(n):
    log = logging.getLogger(f"blocks({n})")
    log.info("running")
    time.sleep(0.1)
    log.info("done")
    return n ** 2


async def run_blocking_tasks1(executor):
    log = logging.getLogger("run_blocking_tasks")
    log.info("starting")
    log.info("create executor tasks")
    loop = asyncio.get_event_loop()
    blocking_tasks = [loop.run_in_executor(executor, blocks, i) for i in range(6)]
    log.info("waiting executor tasks")
    completed, pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    log.info("results:{!r}".format(results))
    log.info("exiting")


executor = concurrent.futures.ProcessPoolExecutor(max_workers=3)
event_loop = asyncio.new_event_loop()
try:
    event_loop.run_until_complete(run_blocking_tasks(executor))
finally:
    event_loop.close()
