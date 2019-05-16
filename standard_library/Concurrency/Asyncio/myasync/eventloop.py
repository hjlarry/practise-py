import collections
import heapq
import time

from .handles import Handle, TimeHandle, DelayHandle

_event_loop = None


class Eventloop:
    def __init__(self):
        self._ready = collections.deque()  # 事件队列
        self._stopping = False
        self._scheduled = []  # 存放定时任务的队列
        self._current_handle = None

    def stop(self):
        self._stopping = True

    def call_soon(self, callback, *args):
        # 将事件添加到队列里
        handle = Handle(callback, self, *args)
        self._ready.append(handle)

    def call_later(self, delay, callback, *args):
        if not delay or delay < 0:
            self.call_soon(callback, *args)
        else:
            when = time.time() + delay
            time_handle = TimeHandle(when, callback, self, *args)
            self._scheduled.append(time_handle)
            heapq.heapify(self._scheduled)

    def add_ready(self, handle):
        # 将事件添加到队列里
        if isinstance(handle, Handle):
            self._ready.append(handle)
        else:
            raise Exception("only handle is allowed to join in ready")

    def add_delay(self, handle):
        if isinstance(handle, DelayHandle):
            self.call_later(handle._delay, handle._callback, *handle._args)

    def run_once(self):
        if (not self._ready) and self._scheduled:
            while self._scheduled[0]._when <= time.time():
                time_handle = heapq.heappop(self._scheduled)
                self._ready.append(time_handle)
                if not self._scheduled:
                    break
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

    def run_until_complete(self, fut):
        from .tasks import ensure_task

        future = ensure_task(fut, self)
        future.add_done_callback(_complete_eventloop, future)
        self.run_forever()

    def run_not_complete(self, fut):
        from .tasks import ensure_task

        future = ensure_task(fut, self)
        self.run_forever()


def get_event_loop():
    global _event_loop
    if _event_loop is None:
        _event_loop = Eventloop()
    return _event_loop


def _complete_eventloop(fut):
    fut._loop.stop()
