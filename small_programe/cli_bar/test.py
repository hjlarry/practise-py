import time
import sys


sys.path.insert(0, "..")

import cli_bar

n = 50
flag = input("1~4: ")
if "1" in flag:
    print("=" * 79)
    bar = cli_bar.ProgBar(n, monitor=True)
    for i in range(n):
        time.sleep(0.1)
        bar.update()
    print(bar)

if "2" in flag:
    print("=" * 79)
    for i in cli_bar.prog_bar(range(n)):
        time.sleep(0.1)

if "3" in flag:
    print("=" * 79)
    bar = cli_bar.ProgPercent(n, monitor=True)
    for i in range(n):
        time.sleep(0.1)
        bar.update()
    print(bar)

if "4" in flag:
    print("=" * 79)
    for i in cli_bar.prog_percent(range(n)):
        time.sleep(0.1)
