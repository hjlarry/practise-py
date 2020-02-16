# 一、 整数
# import sys

# x = 1
# y = 1 << 1000
# # 同样是整数，占用的内存大小不同，其采用了变长结构
# print(sys.getsizeof(x))
# print(sys.getsizeof(y))

# print(12_345_6789)  # 可使用下划线分割使数字清晰
# print(0b11011)  # 二进制
# print(0o12)  # 八进制
# print(0x64)  # 十六进制
# # 转换为二进制、八进制、十六进制
# print(bin(100))
# print(oct(100))
# print(hex(100))
# print(int("0o144", 8))  # 字符串八进制转整数

# # 整数转换为字节数组，需要指定大小端
# z = 0x1234
# n = (z.bit_length() + 8 - 1) // 8  # 计算出按8位对齐所需的字节数
# b = z.to_bytes(n, sys.byteorder)
# print(b)
# print(b.hex())
# print(hex(int.from_bytes(b, sys.byteorder)))  # 转换回来

# 二、 字符串
# 1. 转换
# print(ord("汉"))  # 码点 code point
# print(hex(ord("汉")))
# print(chr(27721))
# print(chr(0x6C49))
# print("h\x69, \u6c49\U00005B57")  # 字面量支持转义或Unicode格式字符

# s = "汉字"
# print(s.encode("utf-16"))  # 编码后有BOM标志
# print(s.encode("utf-16").hex())
# import codecs

# print(codecs.BOM_UTF16_LE)  # 可通过codecs处理BOM
# print(codecs.encode(s, "utf-16be").hex())  # 可按指定bom转换

# 2. 池化
# import sys

# print("ashakklskl" is sys.intern("ashakklskl"))
# a = "helloworld!"
# b = "helloworld!"
# print(a is b)
# print(a is sys.intern(a))
# print(a is sys.intern("helloworld!"))

# 3. 通过内存视图修改数据
# e = bytearray(b"abcdefg")
# f = e[2:5]
# print(f)
# e[3] = 0x77  # 修改无效，因为切片是复制字节数据
# print(f)
# print(e)
# v = memoryview(e)
# x = v[2:5]
# x[0] = 0x77  # 修改生效，因为内存视图是对目标内存进行引用
# print(v)
# print(e)

# 4. 需要将一个字符串分割为多个字段，但是分隔符(还有周围的空格)并不是固定的
# import re

# line = "asdf fjdk; afed, fjek,asdf, foo"
# result = re.split(r"[;,\s]\s*", line)
# print(result)

# 5. 在Unicode中，某些字符能够用多个合法的编码表示，可使用unicodedata判断其是否相等
# s1 = "Spicy Jalape\u00f1o"
# s2 = "Spicy Jalapen\u0303o"
# print(s1)
# print(s2)
# print(s1 == s2)  # false
# print(len(s1), len(s2))

# import unicodedata

# t1 = unicodedata.normalize("NFC", s1)
# t2 = unicodedata.normalize("NFC", s2)
# print(t1)
# print(t2)
# print(t1 == t2)  # true


# 6. 字符串清理
# import sys
# import unicodedata

# s = "pýtĥöñ\fis\tawesome\r\n"
# print(s)
# remap = {ord("\t"): " ", ord("\f"): " ", ord("\r"): None}
# a = s.translate(remap)
# print(a)
# cmb_chrs = dict.fromkeys(
#     c for c in range(sys.maxunicode) if unicodedata.combining(chr(c))
# )
# b = unicodedata.normalize("NFD", a)
# c = b.translate(cmb_chrs)
# print(c)
# # 另一种方法
# d = b.encode("ascii", "ignore").decode("ascii")
# print(d)

# 7. 字符串对齐
# text = "Hello World"
# print(text.ljust(20))
# print(text.rjust(20, "*"))
# print(text.center(20))
# print(format(text, "=>20s"))
# print(format(text, "*^20s"))

# 8. 字符串中处理html
# import html

# s = 'Elements are written as "<tag>text</tag>".'
# print(s)
# print(html.escape(s))
# s2 = html.escape(s, quote=False)
# print(s2)
# print(html.unescape(s2))

# 三、 字典
# 1. 一些特殊的创建方式
# kvs = [["a", 1], ("b", 3)]
# c = dict(kvs)
# print(c)
# d = dict(c, e=9)
# print(d)
# x = dict.fromkeys(d, 0)
# print(x)
# y = dict.fromkeys(["h", "i"], 1)
# z = dict.fromkeys("j", 2)
# print(y, z)
# # 如果有a，返回a的值，否则设置a
# x.setdefault("a", 10)
# y.setdefault("a", 10)
# print(x, y)

# 2. 视图支持集合运算，弥补字典功能不足。
# kc = c.keys()
# ky = y.keys()
# print(kc & ky)  # 交集
# print(kc | ky)  # 并集
# print(kc - ky)  # 差集，仅属于a，不属于b
# print(kc ^ ky)  # 对称差集，仅属于a 加 仅属于b， 等于并集减交集
# ks = kc & ky
# c.update({k: y[k] for k in ks})  # 利用交集结果提取待更新内容
# print(c)

# 3. 根据值求最大、最小值、排序
# prices = {"ACME": 45.23, "AAPL": 612.78, "IBM": 205.55, "HPQ": 37.20, "FB": 10.75}
# min_price = min(zip(prices.values(), prices.keys()))
# print(min_price)
# price_sorted = sorted(zip(prices.values(), prices.keys()))
# print(price_sorted)

# 4. 根据字典中某一项的值排序
# rows = [
#     {"fname": "Brian", "lname": "Jones", "uid": 1003},
#     {"fname": "David", "lname": "Beazley", "uid": 1002},
#     {"fname": "John", "lname": "Cleese", "uid": 1001},
#     {"fname": "Big", "lname": "Jones", "uid": 1004},
# ]
# from operator import itemgetter

# row_by_uid = sorted(rows, key=itemgetter("uid"))
# print(row_by_uid)

# 5. 查找两字典的相同点
# a = {"x": 1, "y": 2, "z": 3}
# b = {"w": 10, "x": 11, "y": 2}
# c = {k: a[k] for k in a.keys() & b.keys()}
# print(c)

# 四、 集合
class User1:
    def __init__(self, uid):
        self.uid = uid


class User2:
    def __init__(self, uid):
        self.uid = uid

    def __hash__(self):
        return hash(self.uid)

    def __eq__(self, other):
        return self.uid == other.uid


# 自定义对象的哈希实现是返回随机值，__eq__仅比较自身，所以无法通过set去重
# 需要重载这两个方法。另外如果只重载eq方法，会发现对象是不可哈希的。
u1 = User1(1)
u2 = User1(1)
s1 = set((u1, u2))
print(s1)

u1 = User2(1)
u2 = User2(1)
s2 = set((u1, u2))
print(s2)
