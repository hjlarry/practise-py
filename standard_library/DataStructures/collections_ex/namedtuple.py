import collections

Person = collections.namedtuple("Person", "name age")
bob = Person(name="bob", age=30)
print("Representation:", bob)

jane = Person(name="Jane", age=28)
print(jane.name)
print()

try:
    jane.age = 20
except AttributeError as e:
    print(e)
try:
    collections.namedtuple("Person", "name class age")
except ValueError as e:
    print(e)
try:
    collections.namedtuple("Person", "name age age")
except ValueError as e:
    print(e)
print()

with_class = collections.namedtuple("Person", "name class age", rename=True)
print(with_class._fields)
print(with_class._1)
two_ages = collections.namedtuple("Person", "name age age", rename=True)
print(two_ages._fields)
print()

print(bob)
print(bob._asdict())
print()

bob2 = bob._replace(name="robert")
print(bob2)
print(bob)
