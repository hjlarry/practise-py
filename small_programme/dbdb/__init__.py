"""
- 教程：http://aosabook.org/en/500L/pages/dbdb-dog-bed-database.html
- 中文教程：https://github.com/HT524/500LineorLess_CN/blob/master/DBDB_Dog%20Bed%20Database/DBDB_%E9%9D%9E%E5%85%B3%E7%B3%BB%E5%9E%8B%E6%95%B0%E6%8D%AE%E5%BA%93.md
- 作者源码：https://github.com/aosabook/500lines/blob/master/data-store/README.rst?1533538157736


这个数据库的特点:
1. 接口、逻辑层、物理层的分开实现和设计
2. 不可变二叉树，插入和更新时总是返回一个新的树，新树老树共享数据不变的部分
3. 访问子节点时是通过NodeRef.get()获取真正的数据，以节省加载到内存中的数据量

待练习:
1. 替换BinaryTree为B+树等
2. 编写其他的序列化保存的例子，替换BinaryNodeRef
3. 压缩数据库，当前是会无限增大的
4. 如果需要总是读到最新的数据怎么办（即不允许脏读）

使用方法:
python3 -m dbdb.tool DBNAME set 123 4567
python3 -m dbdb.tool DBNAME get 123
python3 -m dbdb.tool DBNAME delete 123
"""

import os
from .interface import DBDB


def connect(dbname):
    try:
        f = open(dbname, "r+b")
    except IOError:
        fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, "r+b")
    return DBDB(f)
