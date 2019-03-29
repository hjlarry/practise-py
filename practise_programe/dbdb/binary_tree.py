from logical import LogicalBase


class BinaryNode:
    pass


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
        if node is None:
            new_node = BinaryNode()
