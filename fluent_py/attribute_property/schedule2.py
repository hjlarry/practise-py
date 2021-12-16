import json
import inspect


JSON_PATH = "osconfeed.json"


class Record:
    __index = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f"<{cls_name}  serial={self.serial!r}>"

    @staticmethod
    def fetch(key):
        if Record.__index is None:
            Record.__index = load()
        return Record.__index[key]


class Event(Record):
    def __repr__(self):
        if hasattr(self, "name"):
            return f"<{self.__class__.__name__} {self.name!r}>"
        else:
            return super().__repr__()

    @property
    def venue(self):
        key = f"venue.{self.venue_serial}"
        return self.__class__.fetch(key)


def load(path=JSON_PATH):
    records = {}
    with open(path) as fp:
        raw_data = json.load(fp)
    for collection, raw_records in raw_data["Schedule"].items():
        record_type = collection[:-1]
        cls_name = record_type.capitalize()
        cls = globals().get(cls_name, Record)
        if inspect.isclass(cls) and issubclass(cls, Record):
            factory = cls
        else:
            factory = Record
        for raw_record in raw_records:
            key = f"{record_type}.{raw_record['serial']}"
            records[key] = factory(**raw_record)
    return records


if __name__ == "__main__":
    event = Record.fetch("event.33950")
    print(event)
    print(event.venue)
    print(event.venue.name)
    print(event.venue_serial)
