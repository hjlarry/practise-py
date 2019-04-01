import pickle
from logical import LogicalBase, ValueRef


class BinaryNode:
    def store_refs(self, storage):
        # 递归，在任何有未写入的数据更新时一直循环
        self.value_ref.store(storage)
        self.left_ref.store(storage)
        self.right_ref.store(storage)


class BinaryTree(LogicalBase):
    def _get(self, node, key):
        # 执行搜索时，无需担心树的内容发生变化
        while node is not None:
            if key < node.key:
                node = self._follow(node.left_ref)
            elif node.key < key:
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)
        raise KeyError

    def _insert(self, node, key, value_ref):
        # 总返回一个新建的节点，它与旧节点共享未改变的部分，而非更新旧节点上的数据，使得二叉树不可变
        if node is None:
            new_node = BinaryNode(
                self.node_ref_class(), key, value_ref, self.node_ref_class(), 1
            )
        elif key < node.key:
            new_node = BinaryNode.from_node(
                node, left_ref=self._insert(self._follow(node.left_ref), key, value_ref)
            )
        elif key > node.key:
            new_node = BinaryNode.from_node(
                node,
                right_ref=self._insert(self._follow(node.right_ref), key, value_ref),
            )
        else:
            new_node = BinaryNode.from_node(node, value_ref=value_ref)
        return self.node_ref_class(referent=new_node)


class BinaryNodeRef(ValueRef):
    def prepare_to_store(self, storage):
        if self._referent:
            self._referent.store_refs(storage)

    @staticmethod
    def referent_to_string(referent):
        return pickle.dumps(
            {
                "left": referent.left_ref.address,
                "key": referent.key,
                "value": referent.value_ref.address,
                "right": referent.right_ref.address,
                "length": referent.length,
            }
        )
