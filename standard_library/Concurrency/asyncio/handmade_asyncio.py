import socket
import selectors
import time
import collections

selector = selectors.DefaultSelector()


class StopError(Exception):
    pass


def read(socket):
    f = Future()

    def on_readable():
        f.set_result(socket.recv(4096))

    selector.register(socket.fileno(), selectors.EVENT_READ, on_readable)
    chunk = yield from f
    selector.unregister(socket.fileno())
    return chunk


def read_all(socket):
    response = []
    chunk = yield from read(socket)
    while chunk:
        response.append(chunk)
        chunk = yield from read(socket)

    return b"".join(response)


class Future:
    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_done_callbacks(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for callback in self._callbacks:
            callback(self)

    def __iter__(self):
        yield self
        return self.result


class Task(Future):
    def __init__(self, coro):
        super().__init__()
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)

    def step(self, future):
        try:
            next_future = self.coro.send(future.result)
            if next_future is None:
                return
        except StopIteration as exc:
            self.set_result(exc.value)
            return
        next_future.add_done_callbacks(self.step)


class AsyncRequest:
    def __init__(self, host, url, port):

        self.host = host
        self.url = url
        self.port = port
        self.request = f"GET {self.url} HTTP/1.0\r\nHost: {self.host}\r\n\r\n"

    def process(self):
        sock = socket.socket()
        sock.setblocking(False)
        try:
            print("connected")
            sock.connect((self.host, self.port))
        except BlockingIOError:
            pass

        self.f = Future()
        selector.register(sock.fileno(), selectors.EVENT_WRITE, self.on_connected)
        yield self.f

        sock.send(self.request.encode("ascii"))
        selector.unregister(sock.fileno())
        chunk = yield from read_all(sock)
        print("done")
        return chunk

    def on_connected(self):
        self.f.set_result(None)


class EventLoop:
    stopped = False
    select_timeout = 5

    def run_until_complete(self, coros):
        tasks = [Task(coro) for coro in coros]
        try:
            self.run_forever()
        except StopError:
            pass

    def run_forever(self):
        while not self.stopped:
            events = selector.select(self.select_timeout)
            if not events:
                self.stopped = True
            for event_key, event_mask in events:
                callback = event_key.data
                callback()

    def close(self):
        pass


def fetch(url):
    request = AsyncRequest("www.baidu.com", url, 80)
    data = yield from request.process()
    return data


def get_page(url):
    page = yield from fetch(url)
    return page


def async_way():
    loop = EventLoop()
    loop.run_until_complete([get_page(f"/s?wd={i}") for i in range(30)])


def sync_way():
    for i in range(30):
        sock = socket.socket()
        sock.connect(("www.baidu.com", 80))
        print("connected")
        request = "GET {} HTTP/1.0\r\nHost: www.baidu.com\r\n\r\n".format(
            "/s?wd={}".format(i)
        )
        sock.send(request.encode("ascii"))
        response = b""
        chunk = sock.recv(4096)
        while chunk:
            response += chunk
            chunk = sock.recv(4096)
        print("done!!")


# start = time.time()
# sync_way()
# # async_way()
# print(f"Cost {time.time() - start} seconds")


class AsyncWorker:
    def __init__(self, coroutine, workers=10, loop_timeout=5):
        self._q = collections.deque()
        self.size = 0
        self.func = coroutine
        self.stopped = False
        self.ev_loop = EventLoop()
        self.ev_loop.select_timeout = loop_timeout
        self.workers = workers
        self.result_callbacks = []

    def work(self):
        def _work():
            while not self.stopped:
                item = None
                try:
                    item = self.get()
                except IndexError:
                    yield None
                result = yield from self.func(item)
                self.task_done()
                for callback in self.result_callbacks:
                    callback(result)
        self.tasks = []
        for _ in range(self.workers):
            self.tasks.append(_work())
        self.ev_loop.run_until_complete(self.tasks)

    def add_result_callback(self, func):
        self.result_callbacks.append(func)

    def empty_callback(self):
        self.ev_loop.close()

    def put(self, item):
        self.size += 1
        self._q.append(item)

    def get(self):
        item = self._q.popleft()
        return item

    def task_done(self):
        self.size -= 1
        if self.size == 0:
            self.empty_callback()

def print_content_length(data):
    print(len(data))

async_worker = AsyncWorker(get_page, workers=20)
async_worker.add_result_callback(print_content_length)
for i in range(15):
    async_worker.put('/s?wd={}'.format(i))
async_worker.work()