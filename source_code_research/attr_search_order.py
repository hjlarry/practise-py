# 知乎文章 对象属性查找顺序的伪码
# https://www.zhihu.com/question/25391709/answer/30634637


def class_lookup(cls, name):
    "Look for attribute /name/ in class /cls/ and bases."
    v = cls.__dict__.get(name)
    if v is not None:
        # found in this class
        return v, cls
    # search in base classes
    for i in cls.__bases__:
        v, c = class_lookup(i, name)
        if v is not None:
            return v, c
    # not found
    return None


def object_getattr(obj, name):
    "Look for attribute /name/ in object /obj/."
    # First look in class and base classes.
    v, cls = class_lookup(obj.__class__, name)
    if (v is not None) and hasattr(v, "__get__") and hasattr(v, "__set__"):
        # Data descriptor.  Overrides instance member.
        return v.__get__(obj, cls)
    w = obj.__dict__.get(name)
    if w is not None:
        # Found in object
        return w
    if v is not None:
        if hasattr(v, "__get__"):
            # Function-like descriptor.
            # 如果v是一个方法，那么func本身实现了描述符协议，应该会走这里处理
            return v.__get__(obj, cls)
        else:
            # Normal data member in class
            return v
    raise AttributeError(obj.__class__, name)
