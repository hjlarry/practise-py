import time
import threading
from contextlib import contextmanager

# 对象池模式
class ObjectPool:
    def __init__(self, which_class, *args, max_size=None, timeout=0.5, **kwargs):
        self._which_class = which_class
        self._max_size = max_size
        self._size = 0
        self._args = args
        self._kwargs = kwargs
        self._timeout = timeout
        self._items = []
        self._mutex = threading.Lock()
        self._item_available = threading.Condition(self._mutex)

    def get(self):
        with self._mutex:
            if not self._items and (
                self._max_size is None or self._size < self._max_size
            ):
                item = self._which_class(*self._args, **self._kwargs)
                self._size += 1
            else:
                while not self._items:
                    self._item_available.wait(self._timeout)
                item = self._items.pop()
        return item

    def put(self, item):
        with self._mutex:
            self._items.append(item)
            self._item_available.notify()

    @contextmanager
    def item(self):
        item = self.get()
        try:
            yield item
        finally:
            self.put(item)


class Test:
    def __init__(self, a, b=1):
        self.a = a
        self.b = b


pool = ObjectPool(Test, 10, b=2, max_size=3)


class MyThread(threading.Thread):
    def run(self):
        with pool.item() as item:
            print(f"<{item.__class__.__name__}> at {id(item)}")
            time.sleep(0.1)


threads = []
for i in range(10):
    t = MyThread()
    t.start()
    threads.append(t)

for t in threads:
    t.join()
