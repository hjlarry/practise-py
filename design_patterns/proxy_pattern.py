# 代理模式

# Lib/unittest/test/testmock/testpatch.py#L25
def _get_proxy(obj, get_only=True):
    class Proxy:
        def __getattr__(self, name):
            return getattr(obj, name)

    if not get_only:

        def __setattr__(self, name, value):
            return setattr(obj, name, value)

        def __delattr__(self, name):
            return delattr(obj, name)

        Proxy.__setattr__ = __setattr__
        Proxy.__delattr__ = __delattr__

    return Proxy()


class A:
    b = 1


a = A()
a1 = _get_proxy(a)
a2 = _get_proxy(a, get_only=False)

print(a.b, a1.b)

a1.b = 2
print(a.b, a1.b)

a2.b = 2
print(a.b, a2.b)
