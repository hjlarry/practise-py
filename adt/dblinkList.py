class Node:
    def __init__(self, value=None, pre_ref=None, next_ref=None):
        self.value = value
        self.pre_ref = pre_ref
        self.next_ref = next_ref


class DoubleLinkList:
    def __init__(self):
        self.root = Node()
        self.tail_node = self.root
        self.length = 0

    def __len__(self):
        return self.length

    def iter_node(self):
        cur_node = self.root.next_ref
        while cur_node is not None:
            yield cur_node
            cur_node = cur_node.next_ref

    def __iter__(self):
        for node in self.iter_node():
            yield node.value

    def append(self, value):
        new_node = Node(value)
        new_node.pre_ref = self.tail_node
        self.tail_node.next_ref = new_node
        self.tail_node = new_node
        self.root.pre_ref = self.tail_node
        self.length += 1

    def appendleft(self, value):
        tem_node = self.root.next_ref
        new_node = Node(value, self.root, tem_node)
        tem_node.pre_ref = new_node
        self.root.next_ref = new_node
        self.length += 1

    def find(self, value):
        index = 0
        for node in self.iter_node():
            if value == node.value:
                return index
            index += 1
        return -1

    def remove(self, value):
        prevnode = self.root
        for curnode in self.iter_node():
            if curnode.value == value:
                prevnode.next_ref = curnode.next_ref
                del curnode
                self.length -= 1
                return 1  # 表明删除成功
        return -1  # 表明删除失败


def test_double_link_list():
    dll = DoubleLinkList()
    assert len(dll) == 0

    dll.append(0)
    dll.append(1)
    dll.append(2)

    assert list(dll) == [0, 1, 2]

    assert [node.value for node in dll.iter_node()] == [0, 1, 2]
