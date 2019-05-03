# 观察者模式
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
