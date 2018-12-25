from array_ import Array


class ArrayStack:
    def __init__(self, n=32):
        self.n = n
        self.count = 0
        self.items = Array(n)

    def push(self, item):
        if self.count == self.n:
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


def test_stack():
    st = ArrayStack()
    st.push("aa")
    st.push("bb")
    st.push("cc")
    assert "cc" == st.pop()
    assert "bb" == st.pop()
    assert "aa" == st.pop()
    assert st.pop() is None
