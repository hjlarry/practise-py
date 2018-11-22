import functools

# 不需要预激生成器的装饰器
def coroutine(func):
    @functools.wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return primer