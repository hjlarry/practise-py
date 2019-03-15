"""
当子类化内置类型并覆盖一些特殊方法时，在一些隐式调用的场景，这些方法可能不会被调用到

比如以下示例中的__setitem__，字典初始化时会调用，但直接继承自dict的不会被调用
"""

import collections


class ADict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)


class ADict2(collections.UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)


dd = ADict(one=1)
ee = ADict2(one=1)
print(dd)
print(ee)

dd['two'] = 2
ee['two'] = 2
print(dd)
print(ee)
