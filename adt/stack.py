import abc

from array_ import Array
from linkList import DoubleLinkList


class Stack(abc.ABC):
    """栈的API"""

    @abc.abstractmethod
    def push(self, item) -> bool:
        """入栈"""
        raise NotImplementedError

    @abc.abstractmethod
    def pop(self):
        """出栈"""
        raise NotImplementedError


class ArrayStack(Stack):
    def __init__(self, max_size=32):
        self.max_size = max_size
        self.count = 0
        self.items = Array(max_size)

    def push(self, item):
        if self.count == self.max_size:
            return False
        self.items[self.count] = item
        self.count += 1
        return True

    def pop(self):
        if self.count == 0:
            return None
        item = self.items[self.count - 1]
        self.count -= 1
        return item


class LinklistStack(Stack):
    def __init__(self, max_size=32):
        self.max_size = max_size
        self.count = 0
        self.items = DoubleLinkList()

    def push(self, item):
        if self.count == self.max_size:
            return False
        self.items.append(item)
        self.count += 1
        return True

    def pop(self):
        if self.count == 0:
            return None
        item = self.items.tail_node.value
        self.items.remove_node(self.items.tail_node)
        return item


def test_stack(st):
    st.push("aa")
    st.push("bb")
    st.push("cc")
    assert "cc" == st.pop()
    assert "bb" == st.pop()
    assert "aa" == st.pop()
    assert st.pop() is None


if __name__ == "__main__":
    st1 = ArrayStack()
    st2 = LinklistStack()
    test_stack(st1)
    test_stack(st2)
