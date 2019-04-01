import logging
import threading
import time


def daemon():
    logging.debug("Daemon Starting")
    time.sleep(0.2)
    logging.debug("Daemon Exit")


def non_daemon():
    logging.debug("Starting")
    logging.debug("Exit")


# import random
#
# def worker():
#     pause = random.randint(1,5)/10
#     logging.debug('Daemon Starting sleep %0.2f', pause)
#     time.sleep(pause)
#     logging.debug('Daemon Exit')
#
# logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] (%(threadName)-10s) %(message)s")
# for i in range(3):
#     t = threading.Thread(target=worker, daemon=True)
#     t.start()
#
# main_thread = threading.main_thread()
#
# print(threading.enumerate())
#
# for t in threading.enumerate():
#     if t is main_thread:
#         continue
#     logging.debug('%s joining' , t.getName())
#     t.join()

import subprocess

cat = subprocess.Popen(["cat", "Concurrency/signal.ipynb"], stdout=subprocess.PIPE)
grep = subprocess.Popen(["grep", "def"], stdin=cat.stdout, stdout=subprocess.PIPE)
cut = subprocess.Popen(["cut", "-b", "-30"], stdin=grep.stdout, stdout=subprocess.PIPE)
end_of_pipe = cut.stdout

print("Included files:")
for line in end_of_pipe:
    print(line)

import string
import os

os.system("pwd")
# import sys

# workers = []
# for i in range(2):
#     print(f"Parent {os.getpid()} : Forking {i}")
#     worker_pid = os.fork()
#     if not worker_pid:
#         print(f"Worker {i} starting")
#         time.sleep(2+i)
#         print(f"Worker {i} finish")
#         sys.exit(i)
#     workers.append(worker_pid)

# for pid in workers:
#     print('Parent waiting for pid', pid)
#     done = os.waitpid(pid,0)
#     print('Parent child done ', done)

os.spawnlp(os.P_WAIT, "pwd", "pwd", "-P")

import asyncio
import functools


async def run_df(loop):
    print("in run_df")
    cmd_done = asyncio.Future(loop=loop)
    factory = functools.partial(DFProtocol, cmd_done)
    proc = loop.subprocess_exec(factory, "df", "-hl", stdin=None, stderr=None)
    try:
        print("launching process")
        transport, _ = await proc
        print("wait process to complete")
        await cmd_done
    finally:
        transport.close()
    return cmd_done.result()


class DFProtocol(asyncio.SubprocessProtocol):
    FD_NAMES = ["stdin", "stdout", "stderr"]

    def __init__(self, done_futures):
        self.done = done_futures
        self.buffer = bytearray()
        super().__init__()

    def connection_made(self, transport):
        print("process started ", transport.get_pid())
        self.transport = transport

    def pipe_data_received(self, fd, data):
        print(f"read {len(data)} bytes from {self.FD_NAMES[fd]}")
        if fd == 1:
            self.buffer.extend(data)

    def process_exited(self):
        print("process exited")
        return_code = self.transport.get_returncode()
        print("return code ", return_code)
        if not return_code:
            cmd_output = bytes(self.buffer).decode()
            results = self._parse_results(cmd_output)
        else:
            results = []
        self.done.set_result((return_code, results))

    def _parse_results(self, output):
        print("paesing results")
        if not output:
            return []
        lines = output.splitlines()
        headers = lines[0].split()
        devices = lines[1:]
        results = [dict(zip(headers, line.split())) for line in devices]
        return results


event_loop = asyncio.get_event_loop()
try:
    return_code, results = event_loop.run_until_complete(run_df(event_loop))
finally:
    event_loop.close()

if return_code:
    print("error exit", return_code)
else:
    print("\n Free space:")
    for r in results:
        print("{Mounted:25}:{Avail}".format(**r))
