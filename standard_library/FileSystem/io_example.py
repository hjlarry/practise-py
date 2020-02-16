import io

print("一、 字符串IO操作")
output = io.StringIO()
output.write("something to buffer. ")
# file:  a file-like object (stream); defaults to the current sys.stdout.
print("And so does this", file=output, end=" ")
print(output.getvalue())
output.close()  # discard buffer memory

input = io.StringIO("Intial value for read buffer")
print(input.read())  # readline() 和 readlines() seek()方法也是可用的
print()


print("二、 二进制字符IO操作")
output = io.BytesIO()
output.write("sth to buffer".encode("utf-8"))
output.write("ÁÇÊ".encode("utf-8"))
print(output.getvalue())
output.close()

input = io.BytesIO(b"Intial value for read buffer")
print(input.read())
print()

print("三、 TextIOWrapper")
output = io.BytesIO()
wrapper = io.TextIOWrapper(output, encoding="utf-8", write_through=True)
wrapper.write("something to buffer.")
wrapper.write("ÁÇÊ")

print(output.getvalue())
output.close()

input = io.BytesIO(b"Intial value for read buffer" + "ÁÇÊ".encode("utf-8"))
wrapper = io.TextIOWrapper(input, encoding="utf-8")
print(wrapper.read())

# I/O系统由一系列的层次构建而成
f = open("test_files/sth.txt", "w")
# io.TextIOWrapper 是一个编码和解码Unicode的文本处理层
print(f)
# io.BufferedWriter 是一个处理二进制数据的带缓冲的I/O层
print(f.buffer)
# io.FileIO 是一个表示操作系统底层文件描述符的原始文件
print(f.buffer.raw)
