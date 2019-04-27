import asyncio
import functools

print("一、 使用抽象协议执行子进程")


async def run_df(loop):
    print("in run_df")
    cmd_done = asyncio.Future(loop=loop)
    factory = functools.partial(DFProtocol, cmd_done)
    # 使用subprocess_exec() 可以进入子进程执行，并将其连接至一个协议类以便解析它
    proc = loop.subprocess_exec(factory, "df", "-hl", stdin=None, stderr=None)
    try:
        print("launching process")
        transport, protocol = await proc
        print("wait process to complete")
        await cmd_done
    finally:
        transport.close()
    return cmd_done.result()


# SubprocessProtocol中的方法会被自动调用，基于子进程的IO事件
# 本例中由于没有设置stdin和stderr参数，这些通道并没有连接至子进程中
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
    print("Free space:")
    for r in results:
        print("{Mounted:25}:{Avail}".format(**r))

print()
print("二、 使用协程和流调用子进程")


def _parse_results(output):
    print("parseing results")
    if not output:
        return []
    lines = output.splitlines()
    headers = lines[0].split()
    devices = lines[1:]
    results = [dict(zip(headers, line.split())) for line in devices]
    return results


async def run_df1():
    print("in run_df1")
    buffer = bytearray()
    create = asyncio.create_subprocess_exec("df", "-hl", stdout=asyncio.subprocess.PIPE)
    print("launching process")
    proc = await create
    print("process started at ", proc.pid)
    while True:
        line = await proc.stdout.readline()
        print(f"read {line!r}")
        if not line:
            print("no more output from command")
            break
        buffer.extend(line)
    print("waiting for process to complete")
    await proc.wait()
    return_code = proc.returncode
    print("return code ", return_code)
    if not return_code:
        cmd_output = bytes(buffer).decode()
        results = _parse_results(cmd_output)
    else:
        results = []
    return (return_code, results)


event_loop = asyncio.new_event_loop()
asyncio.set_event_loop(event_loop)
try:
    return_code, results = event_loop.run_until_complete(run_df1())
finally:
    event_loop.close()

if return_code:
    print("error exit", return_code)
else:
    print("\n Free space:")
    for r in results:
        print("{Mounted:25}:{Avail}".format(**r))


print()
print("三、 向子进程发送数据")


async def to_upper(input):
    print("in to_upper")
    create = asyncio.create_subprocess_exec(
        "tr",
        "[:lower:]",
        "[:upper:]",
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE,
    )
    print("lanuching process")
    proc = await create
    print("pid ", proc.pid)
    print("communication with process")
    stdout, stderr = await proc.communicate(input.encode())
    print("waiting for process to complete")
    await proc.wait()
    return_code = proc.returncode
    print("return code ", return_code)
    if not return_code:
        results = bytes(stdout).decode()
    else:
        results = ""
    return (return_code, results)


MESSAGE = """
this message Will be converted to all caps
"""
event_loop = asyncio.new_event_loop()
asyncio.set_event_loop(event_loop)
try:
    return_code, results = event_loop.run_until_complete(to_upper(MESSAGE))
finally:
    event_loop.close()

if return_code:
    print("error exit", return_code)
else:
    print(f"Original: {MESSAGE!r}")
    print(f"Changed: {results!r}")
