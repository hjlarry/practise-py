"""
- 教程：http://aosabook.org/en/500L/pages/dbdb-dog-bed-database.html
- 中文教程：https://github.com/HT524/500LineorLess_CN/blob/master/DBDB_Dog%20Bed%20Database/DBDB_%E9%9D%9E%E5%85%B3%E7%B3%BB%E5%9E%8B%E6%95%B0%E6%8D%AE%E5%BA%93.md
- 作者源码：https://github.com/aosabook/500lines/blob/master/data-store/README.rst?1533538157736
"""

import os
from interface import dbdb


def connect(dbname):
    try:
        f = open(dbname, "r+b")
    except IOError:
        fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, "r+b")
    return dbdb(f)
