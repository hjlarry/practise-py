import json

JSON_PATH = "osconfeed.json"


class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f"<{cls_name}  serial={self.serial!r}>"


def load(path=JSON_PATH):
    records = {}
    with open(path) as fp:
        raw_data = json.load(fp)
    for collection, raw_records in raw_data["Schedule"].items():
        # 将 events 这样的转换为 event
        record_type = collection[:-1]
        for raw_record in raw_records:
            key = f"{record_type}.{raw_record['serial']}"
            records[key] = Record(**raw_record)
    return records


if __name__ == "__main__":
    records = load()
    speaker = records["speaker.3471"]
    print(speaker.name)
    print(speaker.twitter)
