import collections

# https://zhuanlan.zhihu.com/p/64991670
class Future:

    _FINISHED = "finished"
    _PENDING = "pending"
    _CANCELLED = "CANCELLED"

    def __init__(self, loop=None):
        if loop is None:
            self._loop = get_event_loop()
        else:
            self._loop = loop
        self._callbacks = []
        self.status = self._PENDING
        self._blocking = False
        self._result = None

    def _schedule_callbacks(self):
        # 将回调函数添加到事件队列里，eventloop 稍后会运行
        for callback in self._callbacks:
            self.loop.add_ready(callback)
        self._callbacks = []

    def set_result(self, result):
        # 给future设置结果，并将 future 置为结束状态
        self.status = self._FINISHED
        self._result = result
        self._schedule_callbacks()

    def add_done_callback(self, callback, *args):
        # 为future增加回调函数
        if self.done():
            self._loop.call_soon(callback, *args)
        else:
            handle = Handle(callback, self._loop, *args)
            self._callbacks.append(handle)

    def done(self):
        return self.status != self._PENDING

    def result(self):
        # 获取future 的结果
        if self.status != self._FINISHED:
            raise Exception("future is not ready")
        return self._result

    def __iter__(self):
        if not self.done():
            self._blocking = True
        yield self  # 返回自身
        assert self.done(), "future not done"  # 下一次运行 future 的时候，要确定 future 对应的事件已经运行完毕
        return self.result()


class Task(Future):
    def __init__(self, coro, loop=None):
        super().__init__(loop=loop)
        self._coro = coro
        self._loop.call_soon(self._step)  # 启动协程

    def _step(self, exc=None):
        try:
            if exc is None:
                result = self._coro.send(None)
            else:
                result = self._coro.throw(exc)  # 有异常则抛出
        except StopIteration as exc:  # 说明协程已执行完毕，为它设置值
            self.set_result(exc.value)
        else:
            if isinstance(result, Future):
                if result._blocking:
                    self._blocking = False
                    result.add_done_callback(self._wakeup, result)
                else:
                    self._loop.call_soon(self._step, RuntimeError("你是不是用了yield才导致这个错误"))
            elif result is None:
                self._loop.call_soon(self._step)
            else:
                self._loop.call_soon(self._step, RuntimeError("你产生了一个不合规范的值"))

    def _wakeup(self, future):
        try:
            future.result()  # 查看future是否运行有异常
        except Exception as exc:
            self._step(exc)
        else:
            self._step()


class Handle:
    # 对函数和参数的简单封装
    def __init__(self, callback, loop, *args):
        self._callback = callback
        self._args = args

    def _run(self):
        self._callback(*self._args)


class Eventloop:
    def __init__(self):
        self._ready = collections.deque()  # 事件队列
        self._stopping = False

    def stop(self):
        self._stopping = True

    def call_soon(self, callback, *args):
        # 将事件添加到队列里
        handle = Handle(callback, self, *args)
        self._ready.append(handle)

    def add_ready(self, handle):
        # 将事件添加到队列里
        if isinstance(handle, Handle):
            self._ready.append(handle)
        else:
            raise Exception("only handle is allowed to join in ready")

    def run_once(self):
        # 执行队列里的事件
        ntodo = len(self._ready)
        for i in range(ntodo):
            handle = self._ready.popleft()
            handle._run()

    def run_forever(self):
        while True:
            self.run_once()
            if self._stopping:
                break


_event_loop = None


def get_event_loop():
    global _event_loop
    if _event_loop is None:
        _event_loop = Eventloop()
    return _event_loop
