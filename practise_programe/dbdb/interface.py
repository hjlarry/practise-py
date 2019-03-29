class DBDB:
    def __init__(self, f):
        # self._storage属性放在这里是为了可以assert_closed，否则直接通过tree对存储访问就行了
        self._storage = Storage(f)
        self._tree = BinaryTree(self._storage)

    def _assert_not_closed(self):
        if self._storage.closed:
            raise ValueError("Database closed")

    def __getitem__(self, key):
        self._assert_not_closed()
        return self._tree.get(key)

    def __setitem__(self, key, value):
        self._assert_not_closed()
        return self._tree.set(key, value)
