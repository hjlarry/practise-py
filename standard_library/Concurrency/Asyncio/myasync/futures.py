from .handles import Handle
from .eventloop import get_event_loop


def set_future_result(future, result):
    future.set_result(result)


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
            self._loop.add_ready(callback)
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
