import collections

print("一、 namedtuple基础使用")
Person = collections.namedtuple("Person", "name age")
bob = Person(name="bob", age=30)
print("Representation:", bob)

jane = Person(name="Jane", age=28)
print(jane.name)
print()

print("二、常见错误")
try:
    jane.age = 20
except AttributeError as e:
    # 不能直接设值
    print(e)
try:
    collections.namedtuple("Person", "name class age")
except ValueError as e:
    # 不能使用关键字class
    print(e)
try:
    collections.namedtuple("Person", "name age age")
except ValueError as e:
    # 不能使用重复的name
    print(e)
print()

# 创建时设置允许rename
with_class = collections.namedtuple("Person", "name class age", rename=True)
print(with_class._fields)
print(with_class._1)
two_ages = collections.namedtuple("Person", "name age age", rename=True)
print(two_ages._fields)
print()

print("三、_asdict和_replace")
print(bob)
print(bob._asdict())
print()

bob2 = bob._replace(name="robert")
print(bob2)
print(bob)
