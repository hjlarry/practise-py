import cgitb
import os

LOGDIR = os.path.join(os.path.dirname(__file__), "LOGS")

if not os.path.exists(LOGDIR):
    os.makedirs(LOGDIR)

cgitb.enable(logdir=LOGDIR, display=False, format="text")


class MyException(Exception):
    """
    为自定义异常python添加一个额外的属性。
    """

    def __init__(self, message, bad_value):
        self.bad_value = bad_value
        Exception.__init__(self, message)
        return


raise MyException("Normal message", bad_value=99)
