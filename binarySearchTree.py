class Node:
    def __init__(self, key, value=None, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right


class BST:
    size = 0

    def __init__(self, root=None):
        self.root = root

    @classmethod
    def build_from_list(cls, arr):
        node_dict = {}
        for item in arr:
            data = item['key']
            node_dict[data] = Node(data, value=data * 2)
        for item in arr:
            data = item['key']
            node = node_dict[data]
            if item['is_root']:
                root = node
            node.left = node_dict.get(item['left'])
            node.right = node_dict.get(item['right'])
            cls.size += 1
        return cls(root)

    def _bst_search(self, subtree, key):
        if subtree is None:
            return None
        if key == subtree.key:
            return subtree
        elif key < subtree.key:
            return self._bst_search(subtree.left, key)
        elif key > subtree.key:
            return self._bst_search(subtree.right, key)

    def get(self, key, default=None):
        node = self._bst_search(self.root, key)
        if node:
            return node.value
        else:
            return default

    def _bst_min_key(self, subtree):
        if subtree.left is None:
            return subtree
        else:
            return self._bst_min_key(subtree.left)

    def get_min_key(self):
        return self._bst_min_key(self.root).key

    def _insert_node(self, subtree, key, value):
        if subtree is None:
            subtree = Node(key, value)
        elif key < subtree.key:
            subtree.left = self._insert_node(subtree.left, key, value)
        elif key > subtree.key:
            subtree.right = self._insert_node(subtree.right, key, value)
        return subtree

    def add(self, key, value):
        node = self._bst_search(self.root, key)
        if node:
            node.value = value
            return 'modify'
        else:
            self._insert_node(self.root, key, value)
            self.size += 1
            return 'add'

    def _bst_remove(self, subtree, key):
        if subtree is None:
            return None
        elif key < subtree.key:
            subtree.left = self._bst_remove(subtree.left, key)
            return subtree
        elif key > subtree.key:
            subtree.right = self._bst_remove(subtree.right, key)
            return subtree
        else:
            if subtree.left is None and subtree.right is None:
                return None
            elif subtree.left is None or subtree.right is None:
                if subtree.left is not None:
                    return subtree.left
                else:
                    return subtree.right
            else:
                successor_node = self._bst_min_key(subtree.right)
                subtree.key, subtree.value = successor_node.key, successor_node.value
                self._bst_remove(subtree.right, successor_node.key)
                return subtree

    def remove(self, key):
        node = self._bst_remove(self.root, key)
        if node:
            self.size -= 1
        return node

    def iter_tree_preorder(self, subtree, callback=print):
        if subtree is not None:
            callback(subtree.key)
            self.iter_tree_preorder(subtree.left, callback)
            self.iter_tree_preorder(subtree.right, callback)


NODE_LIST = [
    {'key': 60, 'left': 12, 'right': 90, 'is_root': True},
    {'key': 12, 'left': 4, 'right': 41, 'is_root': False},
    {'key': 4, 'left': 1, 'right': None, 'is_root': False},
    {'key': 1, 'left': None, 'right': None, 'is_root': False},
    {'key': 41, 'left': 29, 'right': None, 'is_root': False},
    {'key': 29, 'left': 23, 'right': 37, 'is_root': False},
    {'key': 23, 'left': None, 'right': None, 'is_root': False},
    {'key': 37, 'left': None, 'right': None, 'is_root': False},
    {'key': 90, 'left': 71, 'right': 100, 'is_root': False},
    {'key': 71, 'left': None, 'right': 84, 'is_root': False},
    {'key': 100, 'left': None, 'right': None, 'is_root': False},
    {'key': 84, 'left': None, 'right': None, 'is_root': False},
]


def test_bst_tree():
    bst = BST.build_from_list(NODE_LIST)
    for node_dict in NODE_LIST:
        key = node_dict['key']
        assert bst.get(key) == key * 2
    assert bst.size == len(NODE_LIST)
    assert bst.get(-1) is None  # 单例的 None 我们用 is 来比较

    assert bst.get_min_key() == 1

    bst.add(0, 0)
    bst.iter_tree_preorder(bst.root)
    assert bst.get_min_key() == 0

    bst.remove(12)
    assert bst.get(12) is None

    bst.remove(1)
    assert bst.get(1) is None

    bst.remove(29)
    assert bst.get(29) is None
