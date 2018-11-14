import warnings
import osconfeed
import shelve

DB_NAME = "schedule1_db"


class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def load_db(db):
    raw_data = osconfeed.load()
    warnings.warn("loading " + DB_NAME)
    for collection, rec_list in raw_data["Schedule"].items():
        # 将 events 这样的转换为 event
        record_type = collection[:-1]
        for record in rec_list:
            key = f"{record_type}.{record['serial']}"
            record["serial"] = key
            db[key] = Record(**record)

db = shelve.open(DB_NAME)
# 判断数据库是否填充的一个方法
if 'conference.115' not in db:
    load_db(db)

speaker = db['speaker.3471']
print(speaker.name)
print(speaker.twitter)
db.close()