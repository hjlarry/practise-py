# 发布订阅模式
"""
1. 观察者模式中，观察者是知道Subject的，Subject一直保持对观察者进行记录。
   然而在发布订阅模式中，发布者不知道订阅者的存在，它们通过消息代理进行通信。
2. 观察者模式大多是同步的，比如事件触发，Subject就会去调用观察者的方法。
   而发布订阅模式因为使用消息队列，大多是异步的
3. 观察者模式中Subject通常是无区分的通知观察者，是一个广播群发。
   而发布订阅模式，发布者和订阅者由于有消息队列进行调度，不会把消息发给不需要的订阅者
"""
from collections import defaultdict


class PubSubHub:
    def __init__(self):
        self.msg_queue = []
        self.subscribers = defaultdict(list)

    def notify(self, msg):
        self.msg_queue.append(msg)

    def subscribe(self, msg, subscriber):
        self.subscribers[msg].append(subscriber)

    def unsubscribe(self, msg, subscriber):
        self.subscribers[msg].remove(subscriber)

    def update(self):
        for msg in self.msg_queue:
            for sub in self.subscribers.get(msg, []):
                sub.run(msg)
        self.msg_queue = []


class Publisher:
    def __init__(self, hub):
        self.hub = hub

    def publish(self, msg):
        self.hub.notify(msg)


class Subscriber:
    def __init__(self, name, hub):
        self.name = name
        self.hub = hub

    def subscribe(self, msg):
        self.hub.subscribe(msg, self)

    def unsubscribe(self, msg):
        self.hub.unsubscribe(msg, self)

    def run(self, msg):
        print(f"{self.name} got {msg}")


hub = PubSubHub()
pptv = Publisher(hub)
# 订阅者订阅内容
jim = Subscriber("Jim", hub)
jack = Subscriber("Jack", hub)
tom = Subscriber("Tom", hub)
jim.subscribe("movie")
jack.subscribe("cartoon")
tom.subscribe("music")
# 发布者发布内容
pptv.publish("movie")
pptv.publish("music")
pptv.publish("music")
pptv.publish("abc")
# 消息代理控制订阅者什么时候接收到内容
hub.update()
