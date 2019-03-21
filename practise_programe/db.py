"""
- 教程：http://aosabook.org/en/500L/pages/dbdb-dog-bed-database.html
- 中文教程：https://github.com/HT524/500LineorLess_CN/blob/master/DBDB_Dog%20Bed%20Database/DBDB_%E9%9D%9E%E5%85%B3%E7%B3%BB%E5%9E%8B%E6%95%B0%E6%8D%AE%E5%BA%93.md
- 作者源码：https://github.com/aosabook/500lines/blob/master/data-store/README.rst?1533538157736
"""


import os
import struct
import pickle

import portalocker


class DBDB:
    def __init__(self, f):
        self._storage = Storage(f)
        self._tree = BinaryTree(self._storage)

    def __getitem__(self, key):
        return self._tree.get(key)

    def __setitem__(self, key, value):
        return self._tree.set(key, value)


class Storage:
    SUPERBLOCK_SIZE = 4096
    INTEGER_LENGTH = 8
    INTEGER_FORMAT = "!Q"

    def __init__(self, f):
        self._f = f
        self.locked = False
        self._ensure_superblock()

    def _ensure_superblock(self):
        self.lock()
        self._seek_end()
        end_address = self._f.tell()
        if end_address < self.SUPERBLOCK_SIZE:
            self._f.write(b"\x00" * (self.SUPERBLOCK_SIZE - end_address))
        self.unlock()

    def lock(self):
        if not self.locked:
            portalocker.lock(self._f, portalocker.LOCK_EX)
            self.locked = True
            return True
        else:
            return False

    def unlock(self):
        if self.locked:
            self._f.flush()
            portalocker.unlock(self._f)
            self.locked = False

    def _seek_end(self):
        self._f.seek(0, os.SEEK_END)

    def get_root_address(self):
        self._f.seek(0)
        return self._read_integer()

    def _read_integer(self):
        return self._bytes_to_integer(self._f.read(self.INTEGER_LENGTH))

    def _bytes_to_integer(self, integer_bytes):
        return struct.unpack(self.INTEGER_FORMAT, integer_bytes)[0]

    def read(self, address):
        self._f.seek(address)
        length = self._read_integer()
        data = self._f.read(length)
        return data


class BinaryNodeRef:
    def __init__(self, referent=None, address=0):
        self._referent = referent
        self._address = address

    def get(self, storage):
        if self._referent is None and self._address:
            self._referent = self.string_to_referent(storage.read(self._address))
        return self._referent

    @staticmethod
    def string_to_referent(string):
        d = pickle.loads(string)
        print(d)
        return BinaryNode(
            BinaryNodeRef(address=d["left"]),
            d["key"],
            ValueRef(address=d["value"]),
            BinaryNodeRef(address=d["right"]),
            d["length"],
        )


class ValueRef(object):
    @staticmethod
    def string_to_referent(string):
        return string.decode("utf-8")

    def __init__(self, referent=None, address=0):
        self._referent = referent
        self._address = address

    def get(self, storage):
        if self._referent is None and self._address:
            self._referent = self.string_to_referent(storage.read(self._address))
        return self._referent


class BinaryNode(object):
    @classmethod
    def from_node(cls, node, **kwargs):
        length = node.length
        if "left_ref" in kwargs:
            length += kwargs["left_ref"].length - node.left_ref.length
        if "right_ref" in kwargs:
            length += kwargs["right_ref"].length - node.right_ref.length

        return cls(
            left_ref=kwargs.get("left_ref", node.left_ref),
            key=kwargs.get("key", node.key),
            value_ref=kwargs.get("value_ref", node.value_ref),
            right_ref=kwargs.get("right_ref", node.right_ref),
            length=length,
        )

    def __init__(self, left_ref, key, value_ref, right_ref, length):
        self.left_ref = left_ref
        self.key = key
        self.value_ref = value_ref
        self.right_ref = right_ref
        self.length = length

    def store_refs(self, storage):
        self.value_ref.store(storage)
        self.left_ref.store(storage)
        self.right_ref.store(storage)


class BinaryTree:
    node_ref_class = BinaryNodeRef

    def __init__(self, storage):
        self._storage = storage
        self._tree_ref = self.node_ref_class(address=self._storage.get_root_address())

    def get(self, key):
        node = self._follow(self._tree_ref)
        return self._get(node, key)

    def _get(self, node, key):
        while node is not None:
            if key < node.key:
                node = self._follow(node.left_ref)
            elif node.key < key:
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)
        raise KeyError

    def _follow(self, ref):
        return ref.get(self._storage)


dbname = "example.db"
try:
    f = open(dbname, "r+b")
except IOError:
    fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
    f = os.fdopen(fd, "r+b")
#
db = DBDB(f)
# db['foo'] = 'jsjjsj'
print(b"\x04Mk\x10X\x05\x00\x00\x00".decode())
