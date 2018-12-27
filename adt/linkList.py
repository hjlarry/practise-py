class Node:
    def __init__(self, value=None, next_ref=None, prev_ref=None):
        self.value = value
        self.next_ref = next_ref
        self.prev_ref = prev_ref


# 单链表
class SingleLinkList:
    def __init__(self):
        self.root = Node()  # 哨兵节点
        self.head_node = self.root
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
        self.tail_node.next_ref = new_node
        self.tail_node = new_node
        self.length += 1

    def appendleft(self, value):
        tmp_node = self.root.next_ref
        new_node = Node(value, tmp_node)
        self.root.next_ref = new_node
        self.length += 1

    def insert(self, k, value):
        # 在第K个位置后插入节点
        if k == 0:
            self.appendleft(value)
            return True
        if k == self.length:
            self.append(value)
            return True
        for i, cur_node in enumerate(self.iter_node()):
            if i == k:
                tmp_node = cur_node.next_ref
                new_node = Node(value, tmp_node)
                cur_node.next_ref = new_node
                self.length += 1
                return True
        return False

    def find(self, value):
        index = 0
        for node in self.iter_node():
            if value == node.value:
                return index
            index += 1
        return False

    def remove(self, value):
        prevnode = self.root
        for curnode in self.iter_node():
            if curnode.value == value:
                prevnode.next_ref = curnode.next_ref
                if curnode is self.tail_node:
                    self.tail_node = prevnode
                del curnode
                self.length -= 1
                return True
            else:
                prevnode = curnode
        return False


# 循环链表
class CircleLinkList:
    def __init__(self):
        self.root = Node(next_ref=self)
        self.head_node = self.root
        self.tail_node = self.root
        self.length = 0

    def __len__(self):
        return self.length

    def iter_node(self):
        cur_node = self.root.next_ref
        length = self.length
        while length:  # 和单链表不同
            yield cur_node
            cur_node = cur_node.next_ref
            length -= 1

    def __iter__(self):
        for node in self.iter_node():
            yield node.value

    def append(self, value):
        tmp_node = self.tail_node.next_ref  # 和单链表不同
        new_node = Node(value, tmp_node)
        self.tail_node.next_ref = new_node
        self.tail_node = new_node
        self.length += 1

    def appendleft(self, value):
        tmp_node = self.root.next_ref
        new_node = Node(value, tmp_node)
        self.root.next_ref = new_node
        self.length += 1

    def insert(self, k, value):
        if k == 0:
            self.appendleft(value)
            return True
        if k == self.length:
            self.append(value)
            return True
        for i, cur_node in enumerate(self.iter_node()):
            if i == k:
                tmp_node = cur_node.next_ref
                new_node = Node(value, tmp_node)
                cur_node.next_ref = new_node
                self.length += 1
                return True
        return False

    def find(self, value):
        index = 0
        for node in self.iter_node():
            if value == node.value:
                return index
            index += 1
        return False

    def remove(self, value):
        prevnode = self.root
        for curnode in self.iter_node():
            if curnode.value == value:
                prevnode.next_ref = curnode.next_ref
                if curnode is self.tail_node:
                    self.tail_node = prevnode
                del curnode
                self.length -= 1
                return True
            else:
                prevnode = curnode
        return False


# 双向链表
class DoubleLinkList:
    def __init__(self):
        self.root = Node()
        self.head_node = self.root
        self.tail_node = self.root
        self.length = 0

    def __len__(self):
        return self.length

    def iter_node(self):
        cur_node = self.root.next_ref
        while cur_node:
            yield cur_node
            cur_node = cur_node.next_ref

    def __iter__(self):
        for node in self.iter_node():
            yield node.value

    def append(self, value):
        new_node = Node(value, prev_ref=self.tail_node)
        self.tail_node.next_ref = new_node
        self.tail_node = new_node
        self.length += 1

    def appendleft(self, value):
        tmp_node = self.root.next_ref
        new_node = Node(value, next_ref=tmp_node, prev_ref=self.root)
        tmp_node.prev_ref = new_node
        self.root.next_ref = new_node
        self.length += 1

    def insert(self, k, value):
        if k == 0:
            self.appendleft(value)
            return True
        if k == self.length:
            self.append(value)
            return True
        for i, cur_node in enumerate(self.iter_node()):
            if i == k:
                tmp_node = cur_node.next_ref
                new_node = Node(value, next_ref=tmp_node, prev_ref=cur_node)
                tmp_node.prev_ref = new_node
                cur_node.next_ref = new_node
                self.length += 1
                return True
        return False

    def find(self, value):
        index = 0
        for node in self.iter_node():
            if value == node.value:
                return index
            index += 1
        return False

    def remove(self, value):
        for curnode in self.iter_node():
            if curnode.value == value:
                self.remove_node(curnode)
                return True
        return False

    def remove_node(self, node):
        # 已知晓节点，可以做到 O(1) 的删除
        prev_node = node.prev_ref
        next_node = node.next_ref
        prev_node.next_ref = next_node
        next_node.prev_ref = prev_node
        del node
        self.length -= 1
        return True


def test_linked_list(ll):
    ll.append(0)
    ll.append(1)
    ll.append(2)

    assert len(ll) == 3
    assert ll.find(2) == 2
    assert ll.find(3) is False

    assert ll.remove(0) is True
    assert ll.remove(3) is False
    assert len(ll) == 2
    assert ll.find(0) is False

    assert list(ll) == [1, 2]

    ll.appendleft(0)
    assert list(ll) == [0, 1, 2]
    assert len(ll) == 3

    ll.insert(0, 5)
    assert ll.find(5) == 0
    ll.insert(4, 6)
    assert ll.find(6) == 4
    ll.insert(1, 7)
    print(list(ll))


if __name__ == "__main__":
    l1 = SingleLinkList()
    l2 = DoubleLinkList()
    l3 = CircleLinkList()
    test_linked_list(l1)
    test_linked_list(l2)
    test_linked_list(l3)
