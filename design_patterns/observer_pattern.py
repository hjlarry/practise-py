# 观察者模式
"""
1. 观察者模式中，观察者是知道Subject的，Subject一直保持对观察者进行记录。
   然而在发布订阅模式中，发布者不知道订阅者的存在，它们通过消息代理进行通信。
2. 观察者模式大多是同步的，比如事件触发，Subject就会去调用观察者的方法。
   而发布订阅模式因为使用消息队列，大多是异步的
3. 观察者模式中Subject通常是无区分的通知观察者，是一个广播群发。
   而发布订阅模式，发布者和订阅者由于有消息队列进行调度，不会把消息发给不需要的订阅者
"""


class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        # 注册要观察的对象
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, modifier=None):
        # 通知已注册对象有新的变化
        for observer in self._observers:
            # 可设置更多过滤条件，对部分对象更新
            if modifier != observer:
                observer.update(self)


class Data(Subject):
    # 观察者类
    def __init__(self, name=""):
        super().__init__()
        self.name = name
        self._data = 0

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self.notify()


class Viewer:
    def update(self, subject):
        print(f"{self.__class__.__name__} received: {subject.name}")


class InterestView(Viewer):
    pass


class CommentView(Viewer):
    pass


data = Data("1001")
data.attach(InterestView())
data.attach(CommentView())
data.data = 123
