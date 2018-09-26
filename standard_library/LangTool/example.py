# 此注释首先出现
# 并跨越 2 行。

# 此注释不会出现在 getcomments() 的输出中。

"""示例文件用作 inspect 示例的基础。
"""

def module_level_function(arg1, arg2='default', *args, **kwargs):
    """该函数在模块中声明"""
    local_variable = arg1 * 2
    return local_variable

class A(object):
    """The A class."""

    def __init__(self, name):
        self.name = name

    def get_name(self):
        "Returns the name of the instance."
        return self.name

instance_of_a = A('sample_instance')

class B(A):
    """This is the B class.
        test It is derived from A.
    """

    # 此方法不是 A 的一部分。
    def do_something(self):
        """Does some work"""

    def get_name(self):
        "Overrides version from A"
        return 'B(' + self.name + ')'