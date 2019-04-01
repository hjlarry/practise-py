import array
import binascii
import tempfile

s = b"This is the array"
a = array.array("b", s)

print("As byte string:", s)
print("As array:", a)
print("As hex:", binascii.hexlify(a))
print()

a = array.array("i", range(3))
print("Initial:", a)
a.extend(range(3))
print("Extended:", a)
print("Slice:", a[2:5])
print("Iterator:", list(enumerate(a)))
print()

print("A1:", a)
output = tempfile.NamedTemporaryFile()
# 数组写入临时文件
a.tofile(output.file)
output.flush()
with open(output.name, "rb") as input:
    raw_data = input.read()
    print("Raw Contents:", binascii.hexlify(raw_data))
    input.seek(0)
    a2 = array.array("i")
    a2.fromfile(input, len(a))
    print("A2:", a2)
    print(a == a2)
    print(a is a2)
print()

print("A1:", a)
as_bytes = a.tobytes()
print("Bytes:", binascii.hexlify(as_bytes))
a2 = array.array("i")
a2.frombytes(as_bytes)
print("A2:", a2)
print()


def to_hex(a):
    chars_per_item = a.itemsize * 2  # 两个16进制数字
    hex_version = binascii.hexlify(a)
    num_chunks = len(hex_version) // chars_per_item
    for i in range(num_chunks):
        start = i * chars_per_item
        end = start + chars_per_item
        yield hex_version[start:end]


start = int("0x12345678", 16)
end = start + 5
a1 = array.array("i", range(start, end))
a2 = array.array("i", range(start, end))
a2.byteswap()
fmt = "{!r:12} {:12} {!r:12} {:12}"
print(fmt.format("a1 hex", "a1", "a2 hex", "a2"))
print("-" * 51)
for values in zip(to_hex(a1), a1, to_hex(a2), a2):
    print(fmt.format(*values))
