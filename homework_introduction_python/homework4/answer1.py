import requests
import json
import threading
import queue
import collections

s = requests.session()


def req(url):
    return json.loads(s.get(url).content)['args']


class Worker(threading.Thread):
    def __init__(self, exeq, resq):
        super().__init__()
        self._exeq = exeq
        self._resq = resq
        self.daemon = True
        self.start()

    def run(self):
        while 1:
            f, args = self._exeq.get()
            try:
                res = f(args)
                self._resq.put((self.name, res))
            except Exception as e:
                print(e)
            self._exeq.task_done()


class ThreadPool:
    def __init__(self):
        self._exeq = queue.Queue()
        self._resq = queue.Queue()
        for _ in range(3):
            Worker(self._exeq, self._resq)

    def add_task(self, f, arg):
        self._exeq.put((f, arg))

    def wait_complete(self):
        self._exeq.join()


pool = ThreadPool()
for i in range(10):
    pool.add_task(req, 'http://httpbin.org/get?a=' + str(i))
pool.wait_complete()

result = collections.defaultdict(list)
while not pool._resq.empty():
    name, res = pool._resq.get()
    result[name].append(res)

print(result)