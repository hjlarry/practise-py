from hashTable import HashTable


class SetAdt(HashTable):
    def add(self, key):
        super().set(key, value=1)

    def remove(self, key):
        super().remove(key)

    def pop(self):
        value = self._table[-1].value
        key = self._table[-1].key
        self.remove(key)
        return value

    def __and__(self, other):
        new_set = SetAdt()
        for item in self:
            if item in other:
                new_set.add(item)
        return new_set

    def __or__(self, other):
        new_set = SetAdt()
        for item in self:
            new_set.add(item)
        for item in other:
            new_set.add(item)
        return new_set

    def __sub__(self, other):
        new_set = SetAdt()
        for item in self:
            if item not in other:
                new_set.add(item)
        return new_set

    def __xor__(self, other):
        or_set = self.__or__(other)
        and_set = self.__and__(other)
        return or_set.__sub__(and_set)


def test_set_adt():
    sa = SetAdt()
    sa.add(1)
    sa.add(2)
    sa.add(3)
    assert 1 in sa  # 测试  __contains__ 方法，实现了 add 和 __contains__，集合最基本的功能就实现啦

    sb = SetAdt()
    sb.add(3)
    sb.add(4)
    sb.add(5)

    assert sorted(list(sa & sb)) == [3]
    assert sorted(list(sa - sb)) == [1, 2]
    assert sorted(list(sa | sb)) == [1, 2, 3, 4, 5]
