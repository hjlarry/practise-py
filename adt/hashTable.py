class Array:
    def __init__(self, size=32, init=None):
        self._size = size
        self._items = [init] * self._size

    def __getitem__(self, index):
        return self._items[index]

    def __setitem__(self, index, value):
        self._items[index] = value

    def __len__(self):
        return self._size

    def clear(self):
        for i in range(len(self)):
            self._items[i] = None

    def __iter__(self):
        for item in self._items:
            yield item


class Slot:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

    def __repr__(self):
        return f"<{self.key}>{self.value}[{self.next}]"


class HashTable:
    """使用开放寻址法的线性探测处理哈希冲突"""

    UNUSED = None
    EMPTY = Slot(None, None)  # 使用过但已删除

    def __init__(self, factor=0.8):
        self._table = Array(size=8, init=HashTable.UNUSED)
        self.length = 0
        self.factor = factor
        assert 0 < self.factor < 1

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
                self.add(slot.key, slot.value)
                self.length += 1

    def add(self, key, value):
        if key in self:
            index = self._find_key(key)
            self._table[index].value = value
            return False
        else:
            index = self._find_slot_for_insert(key)
            self._table[index] = Slot(key, value)
            self.length += 1
            if self._load_factor > self.factor:
                self._rehash()
            return True

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


class HashTableWithLinklist:
    def __init__(self, factor=0.8):
        self._table = Array(size=8)
        self.length = 0
        self.factor = factor

    def _hash(self, key):
        return abs(hash(key)) % len(self._table)

    def __len__(self):
        return self.length

    @property
    def _load_factor(self):
        return self.length / float(len(self._table))

    def _find_slot(self, key):
        index = self._hash(key)
        current = self._table[index]
        is_find = False
        if current is None:
            return None, is_find
        while not is_find:
            if current.key == key:
                is_find = True
            elif current.next is not None:
                current = current.next
            else:
                break
        return current, is_find

    def add(self, key, value):
        slot, is_find = self._find_slot(key)
        if is_find:
            slot.value = value
            return False
        new_slot = Slot(key, value)
        if slot is None:
            self._table[self._hash(key)] = new_slot
        else:
            new_slot.prev = slot
            slot.next = new_slot
        self.length += 1
        if self._load_factor > self.factor:
            self._rehash()
        return True

    def get(self, key, default=None):
        slot, is_find = self._find_slot(key)
        if is_find and slot:
            return slot.value
        return default

    def remove(self, key):
        slot, is_find = self._find_slot(key)
        if not is_find:
            raise KeyError()
        value = slot.value
        if slot.prev:
            slot.prev.next = slot.next
        else:
            self._table[self._hash(key)] = None
        self.length -= 1
        return value

    def _rehash(self):
        old_values = list(self)
        newsize = len(self._table) * 2
        self._table = Array(newsize, None)
        self.length = 0
        for slot in old_values:
            self.add(slot.key, slot.value)

    def __iter__(self):
        for slot in self._table:
            if slot:
                current = slot
                yield current
                while current.next:
                    current = current.next
                    yield current


def test_hash_table():
    h = HashTable()
    h.add("a", 0)
    h.add("b", 1)
    h.add("c", 2)
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
        h.add(i, i)

    for i in range(n):
        assert h.get(i) == i


def test_hash_table_ll():
    h = HashTableWithLinklist()
    h.add("a", 0)
    h.add("b", 1)
    h.add("c", 2)

    assert len(h) == 3
    assert h.get("a") == 0
    assert h.get("b") == 1
    assert h.get("hehe") is None

    h.remove("a")
    assert h.get("a") is None

    n = 50
    for i in range(n):
        h.add(i, i)

    for i in range(n):
        assert h.get(i) == i


if __name__ == "__main__":
    test_hash_table()
    test_hash_table_ll()
