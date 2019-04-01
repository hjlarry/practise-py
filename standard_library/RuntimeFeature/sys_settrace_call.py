import sys


def trace_calls(frame, event, arg):
    if event != "call":
        return
    co = frame.f_code
    func_name = co.co_name
    if func_name == "write":
        # ignore write() calls from printing
        return
    func_line_no = frame.f_lineno
    func_filename = co.co_filename
    if not func_filename.endswith("sys_settrace_call.py"):
        # ignore calls not in this module
        return
    caller = frame.f_back
    caller_line_no = caller.f_lineno
    caller_filename = caller.f_code.co_filename
    print("* call to", func_name)
    print(f"* on line {func_line_no} of {func_filename}")
    print(f"* from line {caller_line_no} of {func_filename}")


def b():
    print("inside b() \n")


def a():
    print("inside a() \n")
    b()


sys.settrace(trace_calls)
a()
