def rescurse(level):
    print(f"recurse({level})")
    if level:
        rescurse(level - 1)


def not_called():
    print("this func not called")
