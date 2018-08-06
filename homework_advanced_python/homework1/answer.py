import time
import types
import this


class cached_method:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

    def __call__(self, *args, **kwargs):
        print(f'args: {args}')
        return self.func(*args, **kwargs)


class Subject:
    def __init__(self, id):
        print(f'Init {id}')
        self.id = id

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id}>'

    @classmethod
    def get(cls, id):
        return cls(id)


class Review:
    def __init__(self, id):
        self.id = id

    @classmethod
    def gets(cls, review_ids):
        return [cls(id) for id in review_ids]

    # @cached_method(ttl=5)
    @cached_method
    def get_subject(self):
        return Subject.get(self.id)


reviews = Review.gets([1, 2, 3])
print(reviews[0].get_subject())
print([r.get_subject() for r in reviews])
print([r.get_subject() for r in reviews])
time.sleep(5)  # 让缓存超时
print([r.get_subject() for r in reviews])
