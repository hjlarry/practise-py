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

    def commit(self):
        # 把所有脏状态写入内存中，然后保存磁盘地址为树的新的根节点
        self._tree_ref.store(self._storage)
        self._storage.commit_root_address(self._tree_ref.address)


class ValueRef:
    def store(self, storage):
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            # 序列化这个节点，然后保存它的存储地址.
            # 实际上更新地址是改变了ValueRef, 但它对用户可见的值没有影响，我们仍可认为它是不可变的
            self._address = storage.write(self.referent_to_string(self._referent))

