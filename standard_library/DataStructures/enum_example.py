import enum


class BugStatus(enum.Enum):
    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1

    # 若在类上添加装饰器 @enum.unique 则以下两行会抛出异常
    # 遍历时不会有下面两行，因为会把它们当作其他成员的别名
    by_design = 4
    closed = 1


print(BugStatus.wont_fix.name)
print(BugStatus.wont_fix.value)
for status in BugStatus:
    print(f"{status.name} = {status.value}")

print(BugStatus.closed is BugStatus.fix_released)
print(BugStatus.closed == BugStatus.fix_released)
print()

print("Order by value:")
try:
    print("\n".join(s.name for s in sorted(BugStatus)))
except TypeError as err:
    print(err)


class IntBugStatus(enum.IntEnum):
    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1
    closed = 1


# IntEnum可以比较大小，Enum 只能比较相等
print("\n".join(s.name for s in sorted(IntBugStatus)))
print()

BugStatus2 = enum.Enum(
    value="BugStatus1", names=("fix_released fix_commited wont_fix new")
)
print(BugStatus2.new)
for status in BugStatus2:
    print(f"{status.name} = {status.value}")
print()

BugStatus3 = enum.Enum(
    value="BugStatus3", names=[("fix_released", 3), ("fix_commited", 5), ("new", 1)]
)
for status in BugStatus3:
    print(f"{status.name} = {status.value}")
