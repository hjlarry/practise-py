class classproperty:
    def __init__(self, fn=None):
        if fn:
            self.fn = fn

    def getter(cls, fn):
        return fn(cls)

    def __get__(self, instance, owner):
        return self.fn(owner)


class Subject:
    _name = "subject"

    def __init__(self):
        self._name = "movie"

    @classproperty
    def name(cls):
        return cls._name


class Movie:
    name = classproperty()

    @name.getter
    def name(cls):
        return "movie"


assert Subject.name == "subject"
assert Subject().name == "subject"
assert Movie.name == "movie"
assert Movie().name == "movie"
