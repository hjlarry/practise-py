from adt import ArrayStack

print("示例一、 括号匹配")


def par_checker(symbol_str):
    s = ArrayStack()
    balanced = True
    index = 0
    while index < len(symbol_str) and balanced:
        symbol = symbol_str[index]
        if symbol == "(":
            s.push(symbol)
        else:
            if s.is_empty():
                balanced = False
            else:
                s.pop()

        index = index + 1

    if balanced and s.is_empty():
        return True
    else:
        return False


print(par_checker("((()))"))
print(par_checker("(()"))
print()


print("示例二、 符号匹配")


def par_checker2(symbol_str):
    s = ArrayStack()
    balanced = True
    index = 0
    while index < len(symbol_str) and balanced:
        symbol = symbol_str[index]
        if symbol in "([{":
            s.push(symbol)
        else:
            if s.is_empty():
                balanced = False
            else:
                top = s.pop()
                if not matches(top, symbol):
                    balanced = False
        index = index + 1
    if balanced and s.is_empty():
        return True
    else:
        return False


def matches(open, close):
    opens = "([{"
    closers = ")]}"
    return opens.index(open) == closers.index(close)


print(par_checker2("{{([][])}()}"))
print(par_checker2("[{()]"))
