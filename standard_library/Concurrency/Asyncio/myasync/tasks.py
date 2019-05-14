from .futures import Future, set_future_result


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
                print("exception:", exc)
                result = self._coro.throw(exc)  # 有异常则抛出
        except StopIteration as exc:  # 说明协程已执行完毕，为它设置值
            self.set_result(exc.value)
        else:
            if isinstance(result, Future):
                if result._loop is not self._loop:
                    self._loop.call_soon(
                        self._step, RuntimeError("future 与 task不在同一个事件循环中")
                    )
                elif result._blocking:
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


def ensure_task(coro_or_future, loop=None):
    if isinstance(coro_or_future, Future):
        return coro_or_future
    else:
        task = Task(coro_or_future, loop)
        return task


def sleep(delay, result=None, loop=None):
    if delay == 0:
        yield
        return result
    future = Future(loop=loop)
    future._loop.call_later(delay, set_future_result, future, result)
    yield from future
