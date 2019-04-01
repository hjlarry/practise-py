"""
- 教程：http://aosabook.org/en/500L/pages/a-python-interpreter-written-in-python.html
- 中文教程：https://linux.cn/article-7753-1.html
- 作者源码：https://github.com/aosabook/500lines/blob/master/interpreter/interpreter.markdown?1533539557726
"""


import types
import inspect
import dis
import sys
import collections


class VirtualMachine:
    def __init__(self):
        self.frames = []
        self.frame = None
        self.return_value = None
        self.last_exception = None

    def run_code(self, code, global_names=None, local_names=None):
        frame = self.make_frame(
            code, global_names=global_names, local_names=local_names
        )
        self.run_frame(frame)

    def make_frame(self, code, call_args={}, global_names=None, local_names=None):
        if global_names is not None and local_names is not None:
            local_names = global_names
        elif self.frames:
            global_names = self.frame.global_names
            local_names = {}
        else:
            global_names = local_names = {
                "__builtins__": __builtins__,
                "__name__": "__main__",
                "__doc__": None,
                "__package__": None,
            }
        local_names.update(call_args)
        frame = Frame(code, global_names, local_names, self.frame)
        return frame

    def parse_byte_and_args(self):
        f = self.frame
        op_offset = f.last_instruction
        current_op = list(dis.get_instructions(f.code_obj))[op_offset]
        byte_code = current_op.opcode
        byte_name = current_op.opname
        f.last_instruction += 1
        if byte_code >= dis.HAVE_ARGUMENT:
            int_arg = current_op.arg

            if byte_code in dis.hasconst:
                arg = f.code_obj.co_consts[int_arg]
            elif byte_code in dis.hasname:
                arg = f.code_obj.co_names[int_arg]
            elif byte_code in dis.haslocal:
                arg = f.code_obj.co_varnames[int_arg]
            elif byte_code in dis.hasjrel:
                arg = f.last_instruction + int_arg // 2
            elif byte_code in dis.hasjabs:
                arg = int_arg // 2
            else:
                arg = int_arg
            argument = [arg]
        else:
            argument = []
        return byte_name, argument

    def dispatch(self, byte_name, argument):
        # print(byte_name, argument)
        try:
            bytecode_fn = getattr(self, "byte_{}".format(byte_name), None)
            print(bytecode_fn)
            if bytecode_fn is None:
                if byte_name.startswith("UNARY_"):
                    self.unaryOperator(byte_name[6:])
                elif byte_name.startswith("BINARY_"):
                    self.binaryOperator(byte_name[7:])
                else:
                    raise Exception("unsupported bytecode type {}".format(byte_name))
            why = bytecode_fn(*argument)
        except:
            self.last_exception = sys.exc_info()[:2] + (None,)
            why = "exception"
        return why

    def run_frame(self, frame):
        self.push_frames(frame)
        while True:
            # print(frame.block_stack)
            byte_name, arguments = self.parse_byte_and_args()
            why = self.dispatch(byte_name, arguments)
            while why and frame.block_stack:
                why = self.manage_block_stack(why)
            if why:
                break
        self.pop_frame()
        if why == "exception":
            exc, val, tb = self.last_exception
            e = exc(val)
            e.__trackback__ = tb
            raise e
        return self.return_value

    def manage_block_stack(self, why):
        assert why != "yield"
        block = self.frame.block_stack[-1]
        if block.type == "loop" and why == "continue":
            self.jump(self.return_value)
            why = None
            return why

        self.pop_block()
        self.unwind_block(block)

        if block.type == "loop" and why == "break":
            self.jump(block.handler)
            why = None
            return why

        if block.type in ["setup-except", "finally"] and why == "exception":
            self.push_block("except-handler")
            exctype, value, tb = self.last_exception
            self.push(tb, value, exctype)
            self.push(tb, value, exctype)
            why = None
            self.jump(block.handler)
            return why

        elif block.type == "finally":
            if why in ("return", "continue"):
                self.push(self.return_value)
            self.push(why)
            why = None
            self.jump(block.handler)
            return why
        return why

    def push_frames(self, frame):
        self.frames.append(frame)
        self.frame = frame

    def pop_frame(self):
        self.frames.pop()
        self.frame = self.frames[-1] if self.frames else None

    def top(self):
        return self.frame.stack[-1]

    def pop(self):
        # print(self.frame.stack)
        return self.frame.stack.pop()

    def push(self, *vals):
        self.frame.stack.extend(vals)

    def popn(self, n):
        if n:
            ret = self.frame.stack[-n:]
            self.frame.stack[-n:] = []
            return ret
        else:
            return []

    def jump(self, jump):
        self.frame.last_instruction = jump

    def push_block(self, b_type, handler=None, level=None):
        if level is None:
            level = len(self.frame.stack)
        self.frame.block_stack.append(Block(b_type, handler, level))

    def pop_block(self):
        return self.frame.block_stack.pop()

    def unwind_block(self, block):
        if block.type == "except-handler":
            offset = 3
        else:
            offset = 0
        while len(self.frame.stack) > block.stack_height + offset:
            self.pop()
        if block.type == "except-handler":
            trackback, value, exctype = self.popn(3)
            self.last_exception = exctype, value, trackback

    def byte_SETUP_LOOP(self, dest):
        self.push_block("loop", dest)

    def byte_SETUP_EXCEPT(self, dest):
        self.push_block("setup-except", dest)

    def byte_RAISE_VARARGS(self, argc):
        cause = exc = None
        if argc == 2:
            cause = self.pop()
            exc = self.pop()
        elif argc == 1:
            exc = self.pop()
        return self.do_raise(cause, exc)

    def do_raise(self, cause, exc):
        if exc is None:
            exc_type, val, tb = self.last_exception
            if exc_type is None:
                return "exception"
            else:
                return "reraise"
        elif type(exc) == type:
            exc_type = exc
            val = exc()
        elif isinstance(exc, BaseException):
            exc_type = type(exc)
            val = exc
        else:
            return "exception"

        if cause:
            if type(cause) == type:
                cause = cause()
            elif not isinstance(cause, BaseException):
                return "exception"
            val.__cause__ = cause

        self.last_exception = exc_type, val, val.__traceback__

    def byte_POP_TOP(self):
        self.pop()

    def byte_LOAD_NAME(self, name):

        frame = self.frame
        if name in frame.local_names:
            val = frame.local_names[name]
        elif name in frame.global_names:
            val = frame.global_names[name]
        elif name in frame.builtin_names:
            val = frame.builtin_names[name]
        else:
            raise NameError("name '%s' is not defined" % name)
        self.push(val)

    def byte_STORE_NAME(self, name):
        self.frame.local_names[name] = self.pop()

    def byte_LOAD_CONST(self, const):
        self.push(const)

    def byte_CALL_FUNCTION(self, arg):
        lenKw, lenPos = divmod(arg, 256)  # KWargs not supported here

        posargs = self.popn(lenPos)
        func = self.pop()
        retval = func(*posargs)

        self.push(retval)

    def byte_MAKE_FUNCTION(self, arg):
        name = self.pop()
        code = self.pop()
        globs = self.frame.global_names
        closure = self.pop() if (arg & 0x8) else None
        ann = self.pop() if (arg & 0x4) else None
        kwdefaults = self.pop() if (arg & 0x2) else None
        defaults = self.pop() if (arg & 0x1) else None
        fn = Function(name, code, globs, defaults, closure, self)
        self.push(fn)

    def byte_GET_ITER(self):
        self.push(iter(self.pop()))

    def byte_FOR_ITER(self, jump):
        iterobj = self.top()
        try:
            v = next(iterobj)
            self.push(v)
        except StopIteration:
            self.pop()
            self.jump(jump)

    def byte_JUMP_ABSOLUTE(self, jump):
        self.jump(jump)

    def byte_JUMP_FORWARD(self, jump):
        self.jump(jump)

    def byte_POP_BLOCK(self):
        self.pop_block()

    def byte_RETURN_VALUE(self):
        self.return_value = self.pop()
        return "return"


class Frame:
    def __init__(self, code_obj, global_names, local_names, prev_frame):
        self.code_obj = code_obj
        self.global_names = global_names
        self.local_names = local_names
        self.prev_frame = prev_frame
        self.stack = []
        if prev_frame:
            self.builtin_names = prev_frame.buildin_names
        else:
            self.builtin_names = local_names["__builtins__"]
            if hasattr(self.builtin_names, "__dict__"):
                self.builtin_names = self.builtin_names.__dict__

        self.last_instruction = 0
        self.block_stack = []


class Function:
    def __init__(self, name, code, globs, defaults, closure, vm):
        self._vm = vm
        self.func_code = code
        self.func_name = self.__name__ = name or code.co_name
        self.func_defaults = tuple(defaults)
        self.func_globals = globs
        self.func_locals = self._vm.frame.f_locals
        self.__dict__ = {}
        self.func_closure = closure
        self.__doc__ = code.co_consts[0] if code.co_consts else None

        kw = {"argdefs": self.func_defaults}

        self._func = types.FunctionType(code, globs, **kw)

    def __call__(self, *args, **kwargs):
        callargs = inspect.getcallargs(self._func, *args, **kwargs)
        frame = self._vm.make_frame(self.func_code, callargs, self.func_globals, {})
        return self._vm.run_frame(frame)


Block = collections.namedtuple("Block", "type, handler, stack_height")

code = compile(
    """
[i for i in range(10)]
    """,
    "",
    "exec",
)
vm = VirtualMachine()
vm.run_code(code)
