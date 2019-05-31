from adt import ArrayStack

print("示例一、 十进制转二进制")


def divide_by2(num):
    remstack = ArrayStack()

    while num > 0:
        rem = num % 2
        remstack.push(rem)
        num = num // 2

    bin_str = ""
    while not remstack.is_empty():
        bin_str = bin_str + str(remstack.pop())

    return bin_str


print("42:", divide_by2(42))
print()


print("示例二、 通用十进制转化器")


def base_converter(num, base):
    digits = "0123456789ABCDEF"

    remstack = ArrayStack(max_size=1024)

    while num > 0:
        rem = num % base
        remstack.push(rem)
        num = num // base
    new_str = ""
    while not remstack.is_empty():
        new_str = new_str + digits[remstack.pop()]

    return new_str


print("25转二进制:", base_converter(25, 2))
print("960转十六进制:", base_converter(960, 16))

