import warnings
import osconfeed
import shelve
import inspect

DB_NAME = "schedule2_db"


class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __eq__(self, other):
        if isinstance(other, Record):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented


class DbRecord(Record):
    __db = None

    @staticmethod
    def set_db(db):
        DbRecord.__db = db

    @staticmethod
    def get_db():
        return DbRecord.__db

    @classmethod
    def fetch(cls, ident):
        db = cls.get_db()
        try:
            return db[ident]
        except TypeError:
            if db is None:
                raise RuntimeError("missing to set db")
            else:
                raise

    def __repr__(self):
        if hasattr(self, "serial"):
            return f"<{self.__class__.__name__} serial={self.serial !r}>"
        else:
            return super().__repr__()


class Event(DbRecord):
    @property
    def venue(self):
        key = f"venue.{self.venue_serial}"
        return self.__class__.fetch(key)

    @property
    def speakers(self):
        if not hasattr(self, "_speaker_objs"):
            spkr_serials = self.__dict__["speakers"]
            self._speaker_objs = [
                self.__class__.fetch(f"speaker.{key}") for key in spkr_serials
            ]
        return self._speaker_objs

    def __repr__(self):
        if hasattr(self, "name"):
            return f"<{self.__class__.__name__} name={self.name !r}>"
        else:
            return super().__repr__()


def load_db(db):
    raw_data = osconfeed.load()
    warnings.warn("loading " + DB_NAME)
    for collection, rec_list in raw_data["Schedule"].items():
        record_type = collection[:-1]
        cls_name = record_type.capitalize()
        cls = globals().get(cls_name, DbRecord)
        # 确定cls是一个类，且可能是DbRecord的任一子类
        if inspect.isclass(cls) and issubclass(cls, DbRecord):
            factory = cls
        else:
            factory = DbRecord
        for record in rec_list:
            key = f"{record_type}.{record['serial']}"
            record["serial"] = key
            db[key] = factory(**record)


db = shelve.open(DB_NAME)
# 判断数据库是否填充的一个方法
if "conference.115" not in db:
    load_db(db)

DbRecord.set_db(db)
event = DbRecord.fetch("event.33950")
print(event)
print(event.venue)
print(event.venue.name)
print(event.speakers)

speaker = DbRecord.fetch("speaker.3471")
print(speaker)
print(speaker.name)
print(speaker.twitter)
db.close()
