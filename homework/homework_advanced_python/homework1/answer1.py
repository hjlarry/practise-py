import time


def cached_method(ttl=None):
    cache_dict = {}

    def wrapper(fn):
        def wrap(*args, **kwargs):
            instance = args[0]
            result = cache_dict.get(id(instance))
            if result and not result["expires"]:  # 没有ttl
                result = result["value"]
            elif (
                result and result["expires"] and result["expires"] > time.time()
            ):  # 有ttl但没有过期
                result = result["value"]
            else:
                result = None

            if not result:
                result = fn(*args, **kwargs)
                expires = time.time() + ttl if ttl else None
                this_dict = {id(instance): {"value": result, "expires": expires}}
                cache_dict.update(this_dict)
            return result

        return wrap

    return wrapper


class Subject:
    def __init__(self, id):
        print(f"Init {id}")
        self.id = id

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"

    @classmethod
    def get(cls, id):
        return cls(id)


class Review:
    def __init__(self, id):
        self.id = id

    @classmethod
    def gets(cls, review_ids):
        return [cls(id) for id in review_ids]

    @cached_method(ttl=5)
    # @cached_method()  # 这里很尴尬，必须加()调用才能执行
    def get_subject(self):
        return Subject.get(self.id)


reviews = Review.gets([1, 2, 3])
print(reviews[0].get_subject())
print([r.get_subject() for r in reviews])
print([r.get_subject() for r in reviews])
time.sleep(5)  # 让缓存超时
print([r.get_subject() for r in reviews])
