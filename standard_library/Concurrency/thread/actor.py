from queue import Queue
from threading import Thread, Event
from collections import deque

# actor模式是一种最古老的也是最简单的并行和分布式计算解决方案
# 一个actor就是一个并发执行的任务，只是简单的执行发送给它的消息任务。
# 响应这些消息时，它可能还会给其他actor发送更进一步的消息。 actor之间的通信是单向和异步的。


# Sentinel used for shutdown
class ActorExit(Exception):
    pass


class Actor:
    def __init__(self):
        self._mailbox = Queue()
        self._terminated = None

    def send(self, msg):
        """
        Send a message to the actor
        """
        self._mailbox.put(msg)

    def recv(self):
        """
        Receive an incoming message
        """
        msg = self._mailbox.get()
        if msg is ActorExit:
            raise ActorExit()
        return msg

    def close(self):
        """
        Close the actor, thus shutting it down
        """
        self.send(ActorExit)

    def start(self):
        """
        Start concurrent execution
        """
        self._terminated = Event()
        t = Thread(target=self._bootstrap)

        t.daemon = True
        t.start()

    def _bootstrap(self):
        try:
            self.run()
        except ActorExit:
            pass
        finally:
            self._terminated.set()

    def join(self):
        self._terminated.wait()

    def run(self):
        """
        Run method to be implemented by the user
        """
        while True:
            msg = self.recv()


print("一、 发送简单消息")
# Sample ActorTask
class PrintActor(Actor):
    def run(self):
        while True:
            msg = self.recv()
            print("Got:", msg)


p = PrintActor()
p.start()
p.send("Hello")
p.send("World")
p.close()
p.join()


print()
print("二、 发送方法和参数")


class TaggedActor(Actor):
    def run(self):
        while True:
            tag, *payload = self.recv()
            getattr(self, "do_" + tag)(*payload)

    # Methods correponding to different message tags
    def do_A(self, x):
        print("Running A", x)

    def do_B(self, x, y):
        print("Running B", x, y)


a = TaggedActor()
a.start()
a.send(("A", 1))  # Invokes do_A(1)
a.send(("B", 2, 3))  # Invokes do_B(2,3)
a.close()
a.join()


print()
print("三、 提交任务并得到结果")


class Result:
    def __init__(self):
        self._evt = Event()
        self._result = None

    def set_result(self, value):
        self._result = value

        self._evt.set()

    def result(self):
        self._evt.wait()
        return self._result


class Worker(Actor):
    def submit(self, func, *args, **kwargs):
        r = Result()
        self.send((func, args, kwargs, r))
        return r

    def run(self):
        while True:
            func, args, kwargs, r = self.recv()
            r.set_result(func(*args, **kwargs))


worker = Worker()
worker.start()
r = worker.submit(pow, 2, 3)
print(r.result())
worker.close()
worker.join()


print()
print("四、 使用生成器代替线程")


class ActorScheduler:
    def __init__(self):
        self._actors = {}  # Mapping of names to actors
        self._msg_queue = deque()  # Message queue

    def new_actor(self, name, actor):
        """
        Admit a newly started actor to the scheduler and give it a name
        """
        self._msg_queue.append((actor, None))
        self._actors[name] = actor

    def send(self, name, msg):
        """
        Send a message to a named actor
        """
        actor = self._actors.get(name)
        if actor:
            self._msg_queue.append((actor, msg))

    def run(self):
        """
        Run as long as there are pending messages.
        """
        while self._msg_queue:
            actor, msg = self._msg_queue.popleft()
            try:
                actor.send(msg)
            except StopIteration:
                pass


def printer():
    while True:
        msg = yield
        print("Got:", msg)


def counter(sched):
    while True:
        # Receive the current count
        n = yield
        if n == 0:
            break
        # Send to the printer task
        sched.send("printer", n)
        # Send the next count to the counter task (recursive)

        sched.send("counter", n - 1)


sched = ActorScheduler()
# Create the initial actors
sched.new_actor("printer", printer())
sched.new_actor("counter", counter(sched))

# Send an initial message to the counter to initiate
sched.send("counter", 10)
sched.run()
