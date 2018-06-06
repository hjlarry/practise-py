class Node:
    def __init__(self, value=None, next_ref=None):
        self.value = value
        self.next_ref = next_ref


class LinkList:
    def __init__(self):
        self.root = Node()
        self.tail_node = self.root
        self.length = 0

    def __len__(self):
        return self.length

    # def __iter__(self):
    #     pos = 0
    #     node = self.root
    #     while pos < self.length:
    #         yield node.value
    #         pos += 1
    #         node = node.next_ref

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
        self.tail_node.next_ref = new_node
        self.tail_node = new_node
        self.length += 1

    def appendleft(self, value):
        tem_node = self.root.next_ref
        new_node = Node(value, tem_node)
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


def test_linked_list():
    ll = LinkList()

    ll.append(0)
    ll.append(1)
    ll.append(2)

    assert len(ll) == 3
    assert ll.find(2) == 2
    assert ll.find(3) == -1

    assert ll.remove(0) == 1
    assert ll.remove(3) == -1
    assert len(ll) == 2
    assert ll.find(0) == -1

    assert list(ll) == [1, 2]

    ll.appendleft(0)
    assert list(ll) == [0, 1, 2]
    assert len(ll) == 3
