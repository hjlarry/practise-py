print("<100>")


def deco_alpha(cls):
    print("<200>")

    def inner_1(self):
        print("<300>")

    cls.method_y = inner_1
    return cls


class MetaAlpha(type):
    print("<400>")

    def __init__(cls, object_or_name, bases, dict):
        print("<500>")

        def inner_2(self):
            print("<600>")

        cls.method_z = inner_2


print("<700>")
