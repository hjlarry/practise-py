# 适配器模式


class Target:
    @property
    def props(self):
        raise NotImplementedError


class Book(Target):
    @property
    def published_date(self):
        return "published date"


class Movie(Target):
    @property
    def realeased_date(self):
        return "released date"


class Adpter:
    def __init__(self, obj, **adapter_methods):
        self.obj = obj
        self.__dict__.update(adapter_methods)

    def __getattr__(self, attr):
        return getattr(self.obj, attr)


objs = []
book = Book()
movie = Movie()
objs.append(Adpter(book, props=book.published_date))
objs.append(Adpter(movie, props=movie.realeased_date))
for obj in objs:
    print(obj.props)
