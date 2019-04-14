import glob

# glob模块使用的模式匹配规则并不同于re模块的正则，其用Unix路径扩展规则。
print("test_files/*:")
for name in sorted(glob.glob("test_files/*")):
    print(name)
print()
print("test_files/*/*:")
for name in sorted(glob.glob("test_files/*/*")):
    print(name)
print()
print("test_files/fi?o:")
for name in sorted(glob.glob("test_files/fi?o")):
    print(name)
print()
print("test_files/fi??:")
for name in sorted(glob.glob("test_files/fi??")):
    print(name)
print()
print("test_files/fi[a-z]e:")
for name in sorted(glob.glob("test_files/fi[a-z]e")):
    print(name)
