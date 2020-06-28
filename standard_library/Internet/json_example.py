import json

# 一、基础用法
data = [{"a": "A", "c": 3.0, "b": (2, 4),}]
print(repr(data))
print(json.dumps(data))
decoded = json.loads(json.dumps(data))
print(data[0]["b"])
print(decoded[0]["b"])
first_sort = json.dumps(data, sort_keys=True)
print(first_sort)
print(json.dumps(data, sort_keys=True, indent=2))
print(json.dumps(data, separators=("!", "@")))
print()

# 二、长度比较
plain_dump = json.dumps(data)
small_indent = json.dumps(data, indent=2)
with_separators = json.dumps(data, separators=(",", ":"))
print("repr(data)             :", len(repr(data)))
print("dumps(data)            :", len(plain_dump))
print("dumps(data, indent=2)  :", len(small_indent))
print("dumps(data, separators):", len(with_separators))
print()

# 三、忽略错误
data = [{"a": "A", "b": (2, 4), "c": 3.0, ("d",): "D tuple"}]
print("First attempt")
try:
    print(json.dumps(data))
except TypeError as err:
    print("ERROR:", err)
print("Second attempt")
print(json.dumps(data, skipkeys=True))
print()

# 四、序列化自定义类型
class MyObj:
    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return f"<MyObj({self.s})>"


# 自定义类型直接序列化会报错
obj = MyObj("hahhaa sth")
try:
    print(json.dumps(obj))
except TypeError as err:
    print(err)

# 方法一，序列化时传入方法
def convert_to_builtin_type(obj):
    print("default:", obj)
    d = {"__class__": obj.__class__.__name__}
    d.update(obj.__dict__)
    return d


converted = json.dumps(obj, default=convert_to_builtin_type)
print(converted)


def dict_to_object(d):
    if "__class__" in d:
        class_name = d.pop("__class__")
        class_ = globals()[class_name]
        print(class_)
        args = {key: value for key, value in d.items()}
        inst = class_(**args)
    else:
        inst = d
    return inst


myobj_instance = json.loads(converted, object_hook=dict_to_object)
print(myobj_instance)
print()

# 方法二，使用自定义的编码解码类
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        d = {"__class__": obj.__class__.__name__}
        d.update(obj.__dict__)
        return d


converted = MyEncoder().encode(obj)
print(converted)


class MyDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.dict_to_object)

    def dict_to_object(self, d):
        if "__class__" in d:
            class_name = d.pop("__class__")
            class_ = globals()[class_name]
            print(class_)
            args = {key: value for key, value in d.items()}
            inst = class_(**args)
        else:
            inst = d
        return inst


myobj_instance = MyDecoder().decode(converted)
print(myobj_instance)
print()

# 五、 对于数据很大的时候，可能会写入类文件对象，这时可以用load和dump
import io

data = [{"a": "A", "b": (2, 4), "c": 3.0}]
f = io.StringIO()
json.dump(data, f)
print(f.getvalue())
f = io.StringIO('[{"a": "A", "c": 3.0, "b": [2, 4]}]')
print(json.load(f))

# 六、 json.tool 模块实现了一个命令行程序来格式化 JSON 数据使其在命令行下更易阅读
"""
$ python3 -m json.tool --sort-keys example.json

[
    {
        "a": "A",
        "b": [
            2,
            4
        ],
        "c": 3.0
    }
]
"""
