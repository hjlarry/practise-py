import functools


class Handle:
    # 对函数和参数的简单封装
    def __init__(self, callback, loop, *args):
        self._callback = callback
        self._args = args

    def _run(self):
        self._callback(*self._args)


@functools.total_ordering
class TimeHandle(Handle):
    # 定时任务
    def __init__(self, when, callback, loop, *args):
        super().__init__(callback, loop, *args)
        self._when = when

    def __hash__(self):
        return hash(self._when)

    def __lt__(self, other):
        return self._when < other._when

    def __eq__(self, other):
        return self._when == other._when


class DelayHandle(Handle):
    # 间隔任务
    def __init__(self, delay, callback, loop, *args):
        super().__init__(callback, loop, *args)
        self._delay = delay
