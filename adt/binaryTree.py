class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


class BinTree:
    def __init__(self, root=None):
        self.root = root

    @classmethod
    def build_from_list(cls, arr):
        node_dict = {}
        for item in arr:
            data = item['data']
            node_dict[data] = Node(data)
        for item in arr:
            data = item['data']
            node = node_dict[data]
            if item['is_root']:
                root = node
            node.left = node_dict.get(item['left'])
            node.right = node_dict.get(item['right'])
        return cls(root)

    # 先序遍历
    def iter_tree_preorder(self, subtree, callback=print):
        if subtree is not None:
            callback(subtree.data)
            self.iter_tree_preorder(subtree.left, callback)
            self.iter_tree_preorder(subtree.right, callback)

    # 中序遍历
    def iter_tree_midorder(self, subtree):
        if subtree is not None:
            self.iter_tree_midorder(subtree.left)
            print(subtree.data)
            self.iter_tree_midorder(subtree.right)

    # 后序遍历
    def iter_tree_afterorder(self, subtree):
        if subtree is not None:
            self.iter_tree_afterorder(subtree.left)
            self.iter_tree_afterorder(subtree.right)
            print(subtree.data)

    # 翻转二叉树
    def reverse(self, subtree):
        if subtree is not None:
            subtree.left, subtree.right = subtree.right, subtree.left
            self.reverse(subtree.left)
            self.reverse(subtree.right)


def test_btree():
    node_list = [
        {'data': 'A', 'left': 'B', 'right': 'C', 'is_root': True},
        {'data': 'B', 'left': 'D', 'right': 'E', 'is_root': False},
        {'data': 'D', 'left': None, 'right': None, 'is_root': False},
        {'data': 'E', 'left': 'H', 'right': None, 'is_root': False},
        {'data': 'H', 'left': None, 'right': None, 'is_root': False},
        {'data': 'C', 'left': 'F', 'right': 'G', 'is_root': False},
        {'data': 'F', 'left': None, 'right': None, 'is_root': False},
        {'data': 'G', 'left': 'I', 'right': 'J', 'is_root': False},
        {'data': 'I', 'left': None, 'right': None, 'is_root': False},
        {'data': 'J', 'left': None, 'right': None, 'is_root': False},
    ]
    btree = BinTree.build_from_list(node_list)
    btree.iter_result = []
    btree.iter_tree_preorder(btree.root, btree.iter_result.append)
    assert btree.iter_result == ['A', 'B', 'D', 'E', 'H', 'C', 'F', 'G', 'I', 'J']

    btree.reverse_res = []
    btree.reverse(btree.root)
    btree.iter_tree_preorder(btree.root, btree.reverse_res.append)
    assert btree.reverse_res == ['A', 'C', 'G', 'J', 'I', 'F', 'B', 'E', 'H', 'D']
