import sys


def trace_calls_and_returns(frame, event, arg):
    co = frame.f_code
    func_name = co.co_name
    if func_name == "write":
        # ignore write() calls from printing
        return
    func_line_no = frame.f_lineno
    func_filename = co.co_filename
    if not func_filename.endswith("sys_settrace_return.py"):
        # ignore calls not in this module
        return
    if event == "call":
        print(f"call to {func_name} on line {func_line_no} of {func_filename}")
        return trace_calls_and_returns
    elif event == "return":
        print(f"{func_name} => {arg}")


def b():
    print("inside b() \n")
    return "response from b"


def a():
    print("inside a() \n")
    val = b()
    return val * 2


sys.settrace(trace_calls_and_returns)
a()
