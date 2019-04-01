import traceback
import sys
import os
from traceback_example import call_function, produce_exception


def f():
    summary = traceback.StackSummary.extract(traceback.walk_stack(None))
    # print(''.join(summary.format()))
    # StackSummary 是一个包含 FrameSummary 实例的可迭代的容器
    for fs in summary:
        print("{fs.filename:<26}:{fs.lineno}:{fs.name}:{fs.line}".format(fs=fs))


print("Calling f() directly:")
f()
print()
print("Calling f() from 3 levels deep:")
call_function(f)


print("with no exception:")
exc_type, exc_value, exc_tb = sys.exc_info()
tbe = traceback.TracebackException(exc_type, exc_value, exc_tb)
print("".join(tbe.format()))

print("with exception:")
try:
    produce_exception()
except Exception as err:
    exc_type, exc_value, exc_tb = sys.exc_info()
    tbe = traceback.TracebackException(exc_type, exc_value, exc_tb)
    print("".join(tbe.format()))
    print("\n exception only:")
    print("".join(tbe.format_exception_only()))

print("print_exc() with no exception:")
traceback.print_exc(file=sys.stdout)
print()

try:
    produce_exception()
except Exception as err:
    print("print_exc():")
    traceback.print_exc(file=sys.stdout)
    print()
    print("print_exc(1):")
    traceback.print_exc(limit=1, file=sys.stdout)
print()
try:
    produce_exception()
except Exception as err:
    print("format_exception():")
    exc_type, exc_value, exc_tb = sys.exc_info()
    for tb_info in traceback.extract_tb(exc_tb):
        filename, linenum, funcname, source = tb_info
        if funcname != "<module>":
            funcname = funcname + "()"
        print(
            "{filename:<23}:{linenum}:{funcname}:\n    {source}".format(
                filename=os.path.basename(filename),
                linenum=linenum,
                source=source,
                funcname=funcname,
            )
        )
