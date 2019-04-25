import socket
import selectors
import time
import collections

selector = selectors.DefaultSelector()


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
        print("第十三步: Future在这里暂停")
        yield self
        print("第十五步: 返回结果")
        return self.result


class Task(Future):
    def __init__(self, coro):
        print("第二步:为每个生成器新建一个任务对象")
        super().__init__()
        self.coro = coro
        f = Future()
        print("第三步: 为了在step中先预激生成器，先新建一个result为None的Future")
        self.step(f)

    def step(self, future):
        try:
            next_future = self.coro.send(future.result)
            print("第七步: 拿到process中新建的Future")
            if next_future is None:
                return
        except StopIteration as exc:
            print("第十六步: f2已经迭代完，得到结果存在Task对象中")
            self.set_result(exc.value)
            return
        print("第八步: 给这个Future添加step回调")
        next_future.add_done_callbacks(self.step)


class EventLoop:
    stopped = False
    select_timeout = 5

    def run_until_complete(self, coros):
        print("第一步:新建事件循环，传入的coros是一组生成器列表")
        tasks = [Task(coro) for coro in coros]
        self.run_forever()
        print("第十七步:查看Task的结果:", tasks[0].result)

    def run_forever(self):
        while not self.stopped:
            print("第九步: 开始selector事件循环")
            events = selector.select(self.select_timeout)
            if not events:
                self.stopped = True
            for event_key, event_mask in events:
                callback = event_key.data
                callback(event_key, event_mask)

    def close(self):
        pass


def read(sock):
    f2 = Future()

    def on_readable(event, mask):
        print("第十四步: 改变f2的result，调用回调step，传入的参数是f2")
        f2.set_result(sock.recv(4096))

    print("第十二步: 进入接收返回的过程，监听相应的描述符")
    selector.register(sock.fileno(), selectors.EVENT_READ, on_readable)
    chunk = yield from f2
    selector.unregister(sock.fileno())
    return chunk


def read_all(sock):
    response = b""
    chunk = yield from read(sock)
    while chunk:
        response += chunk
        chunk = yield from read(sock)
    return response


def process(host, url, port):
    f1 = Future()

    def on_connected(sock, mask):
        print("第十步: set_result执行了第八步中的回调，又进入了step，但是传入的参数是f1这个future")
        f1.set_result(None)

    request_str = f"GET {url} HTTP/1.0\r\nHost: {host}\r\n\r\n"
    sock = socket.socket()
    sock.setblocking(False)
    try:
        print("connected")
        print("第四步: 预激之后建立连接")
        sock.connect((host, port))
    except BlockingIOError:
        pass
    print("第五步: 监听若文件描述符可写，说明可以发送请求，调用回调")
    selector.register(sock.fileno(), selectors.EVENT_WRITE, on_connected)
    print("第六步: 返回一个新建的future对象，生成器暂停")
    yield f1
    print("第十一步: 这时发送了请求")
    sock.send(request_str.encode("ascii"))
    selector.unregister(sock.fileno())

    # 为了使流程清晰，这里只接收一个chunk的内容
    chunk = yield from read(sock)
    # chunk = yield from read_all(sock)
    print("done", chunk[:10])
    return chunk


def get_page(url):
    data = yield from process("www.baidu.com", url, 80)
    return data


def async_way():
    loop = EventLoop()
    loop.run_until_complete([get_page(f"/s?wd={i}") for i in range(1)])


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


start = time.time()
# sync_way()
async_way()
print(f"Cost {time.time() - start} seconds")

# 使用AsyncWorker可以对上述EventLoop逻辑再封装一层
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


# async_worker = AsyncWorker(get_page, workers=20)
# async_worker.add_result_callback(print_content_length)
# for i in range(15):
#     async_worker.put("/s?wd={}".format(i))
# async_worker.work()
