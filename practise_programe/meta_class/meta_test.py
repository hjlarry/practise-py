def create_class(name):
    if name == "User":

        class User:
            def __str__(self):
                return "user obj"

        return User

    elif name == "Company":

        class Company:
            def __str__(self):
                return "company obj"

        return Company


a = create_class("User")


def say(self):
    return 456


def say1():
    return 789


b = type("User", (), {"name": 123, "say": say, "say1": say1})


class MyMeta(type):
    def __new__(cls, *args, **kwargs):
        print()
        print(cls)
        print(args)
        print(kwargs)
        print()
        return super().__new__(cls, *args, **kwargs)


class User(metaclass=MyMeta):
    def __str__(self):
        return 222


print(a())
print(a.__name__)
print(a().__class__)
print(b)
print(b.__dict__)
print(b().say())
print(b.name)
print(b.say1())
