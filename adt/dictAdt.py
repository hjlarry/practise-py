from hashTable import HashTable


class DictAdt(HashTable):
    def __getitem__(self, index):
        return self.get(index)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __delitem__(self, key):
        return self.remove(key)

    def _iter_slot(self):
        for slot in self._table:
            if slot not in (HashTable.UNUSED, HashTable.EMPTY):
                yield slot

    def items(self):
        for slot in self._iter_slot():
            yield (slot.key, slot.value)

    def keys(self):
        for slot in self._iter_slot():
            yield slot.key

    def values(self):
        for slot in self._iter_slot():
            yield slot.value


def test_dict_adt():
    import random

    d = DictAdt()

    d["a"] = 1
    assert d["a"] == 1
    d.remove("a")

    ll = list(range(30))
    random.shuffle(ll)
    for i in ll:
        d.set(i, i)

    for i in range(30):
        assert d.get(i) == i

    assert sorted(list(d.keys())) == sorted(ll)
