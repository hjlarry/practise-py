def cls_name(obj_or_cls):
    cls = type(obj_or_cls)
    if cls is type:
        cls = obj_or_cls
    return cls.__name__.split(".")[-1]


def display(obj):
    cls = type(obj)
    if cls is type:
        return f"<class {obj.__name__}>"
    elif cls in [type(None), int]:
        return repr(obj)
    else:
        return f"<{cls_name(obj)} object>"


def print_args(name, *args):
    pseudo_args = ", ".join(display(x) for x in args)
    print(f"-> {cls_name(args[0])}.__{name}__({pseudo_args})")


class Overriding:
    def __get__(self, instance, owner):
        print_args("get", self, instance, owner)

    def __set__(self, instance, value):
        print_args("set", self, instance, value)


class OverridingNoGet:
    def __set__(self, instance, value):
        print_args("set", self, instance, value)


class NonOverriding:
    def __get__(self, instance, owner):
        print_args("get", self, instance, owner)


class Managed:
    over = Overriding()
    over_no_get = OverridingNoGet()
    none_over = NonOverriding()

    def spam(self):
        print(f"-> Managed.spam({display(self)})")


obj = Managed()
obj.over
Managed.over
obj.over = 7
obj.over
obj.__dict__["over"] = 8
print(vars(obj))
obj.over
print()

# 未实现get的描述符对象则需要print一下
print(obj.over_no_get)
print(Managed.over_no_get)
# 这种情况直接setattr修改无效，而改__dict__有效
obj.over_no_get = 7
print(obj.over_no_get)
obj.__dict__["over_no_get"] = 9
print(vars(obj))
print(obj.over_no_get)
print()

obj.none_over
Managed.none_over
# 设置值会覆盖掉其调用__get__方法
obj.none_over = 7
print(obj.none_over)
obj.__dict__["none_over"] = 9
print(vars(obj))
print(obj.none_over)
# 删除其值会恢复调用__get__方法
del obj.none_over
obj.none_over
print()

print(obj.spam)
print(Managed.spam)
obj.spam = 7
print(obj.spam)
