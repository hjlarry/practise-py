class LogicalBase:
    def get(self, key):
        # 如果没有锁，则更新磁盘上数据树的视图，有锁则可能造成脏读
        if not self._storage.locked:
            self._refresh_tree_ref()
        return self._get(self._follow(self._tree_ref), key)

    def set(self, key, value):
        if self._storage.lock():
            self._refresh_tree_ref()
        # 返回新的树，新树老树共享数据不变的部分以节省内存和执行时间
        self._tree_ref = self._insert(
            self._follow(self._tree_ref), key, self.value_ref_class(value)
        )

    def _refresh_tree_ref(self):
        self._tree_ref = self.node_ref_class(address=self._storage.get_root_address())

