import sys
import functools


def trace_lines(frame, event, arg):
    if event != "line":
        return
    co = frame.f_code
    func_name = co.co_name
    line_no = frame.f_lineno
    print(f"* {func_name} line {line_no}")


def trace_calls(frame, event, arg, to_be_traced):
    if event != "call":
        return
    co = frame.f_code
    func_name = co.co_name
    if func_name == "write":
        # ignore write() calls from printing
        return
    func_line_no = frame.f_lineno
    func_filename = co.co_filename
    if not func_filename.endswith("sys_settrace_line.py"):
        # ignore calls not in this module
        return
    print(f"*call to {func_name} on line {func_line_no} of {func_filename}")
    if func_name in to_be_traced:
        return trace_lines


def c(input):
    print("input=", input)
    print("leaving c()")


def b(arg):
    val = arg * 5
    c(val)
    print("leaving b() \n")


def a():
    b(2)
    print("leaving a() \n")


tracer = functools.partial(trace_calls, to_be_traced=["b"])

sys.settrace(tracer)
a()
