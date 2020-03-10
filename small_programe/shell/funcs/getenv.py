import os

from .constants import SHELL_STATUS_RUN


def getenv(args):
    if len(args) > 0:
        print(os.getenv(args[0]))
    else:
        print(os.environ)
    return SHELL_STATUS_RUN
