class Array:
    def __init__(self, size=32, init=None):
        self._size = size
        self._item = [init] * self._size

    def __getitem__(self, index):
        return self._item[index]

    def __setitem__(self, index, value):
        self._item[index] = value

    def __len__(self):
        return self._size

    def clear(self):
        for i in range(len(self)):
            self[i] = None

    def __iter__(self):
        for item in self._item:
            yield item


class Slot:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashTable:
    UNUSED = None
    EMPTY = Slot(None, None)

    def __init__(self):
        self._table = Array(size=8, init=HashTable.UNUSED)
        self.length = 0

    def _hash(self, key):
        return abs(hash(key)) % len(self._table)

    def __len__(self):
        return self.length

    def __contains__(self, key):
        index = self._find_key(key)
        return index is not None

    @property
    def _load_factor(self):
        return self.length / float(len(self._table))

    def _find_key(self, key):
        index = self._hash(key)
        while self._table[index] is not HashTable.UNUSED:
            if self._table[index] is HashTable.EMPTY:
                index = (index * 5 + 1) % len(self._table)
                continue
            elif self._table[index].key == key:
                return index
            else:
                index = (index * 5 + 1) % len(self._table)
        return None

    def _slot_can_insert(self, index):
        return (
            self._table[index] is HashTable.UNUSED
            or self._table[index] is HashTable.EMPTY
        )

    def _find_slot_for_insert(self, key):
        index = self._hash(key)
        while not self._slot_can_insert(index):
            index = (index * 5 + 1) % len(self._table)
        return index

    def _rehash(self):
        old_table = self._table
        new_table_size = len(old_table) * 2
        self._table = Array(new_table_size, HashTable.UNUSED)
        self.length = 0
        for slot in old_table:
            if slot is not HashTable.UNUSED and slot is not HashTable.EMPTY:
                self.set(slot.key, slot.value)
                self.length += 1

    def set(self, key, value):
        if key in self:
            index = self._find_key(key)
            self._table[index].value = value
            return "modify"
        else:
            index = self._find_slot_for_insert(key)
            self._table[index] = Slot(key, value)
            self.length += 1
            if self._load_factor > 0.8:
                self._rehash()
            return "add"

    def get(self, key, default=None):
        if key in self:
            index = self._find_key(key)
            return self._table[index].value
        else:
            return default

    def remove(self, key):
        if key in self:
            index = self._find_key(key)
            self._table[index] = HashTable.EMPTY
            self.length -= 1
            return True
        else:
            return False

    def __iter__(self):
        for slot in self._table:
            if slot not in (HashTable.EMPTY, HashTable.UNUSED):
                yield slot.key


def test_hash_table():
    h = HashTable()
    h.set("a", 0)
    h.set("b", 1)
    h.set("c", 2)
    assert len(h) == 3
    assert h.get("a") == 0
    assert h.get("b") == 1
    assert h.get("hehe") is None

    h.remove("a")
    assert h.get("a") is None
    print(list(h))
    assert sorted(list(h)) == ["b", "c"]

    n = 50
    for i in range(n):
        h.set(i, i)

    for i in range(n):
        assert h.get(i) == i
