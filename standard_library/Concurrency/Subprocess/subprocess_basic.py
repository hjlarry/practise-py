"""
subprocess 模块提供了了三个 API 处理进程:
1. Python 3.5 中添加的 run() 函数，是一个运行进程的 API，也可以收集其输出
2. call()，check_call() 以及 check_output() 是从 Python2 继承的较早的高级 API。
3. 类 Popen 是一个低级 API，用于构建其他的 API 以及用于更复杂的进程交互。Popen 构造函数接受参数设置新进程，以便父进程可以通过管道与它通信。
"""
import subprocess

print("一、 subprocess.run()")
completed = subprocess.run(["ls", "-l"])
print("return code:", completed.returncode)

# shell为True则subprocess创建一个新的中间shell进程运行命令。默认的行为是直接运行命令
completed = subprocess.run("echo $HOME", stdout=subprocess.PIPE, shell=True)

print("returncode:", completed.returncode)
print(completed.stdout)

print()
print("二、 是否验证错误")
try:
    subprocess.run(["false"], check=True)
except subprocess.CalledProcessError as err:
    print("ERROR:", err)

try:
    subprocess.run(["false"])
except subprocess.CalledProcessError as err:
    print("ERROR?:", err)
print()
print("三、 不同的stdout设置")
try:
    completed = subprocess.run(
        "echo to stdout; echo to stderr 1>&2; exit 1",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
except subprocess.CalledProcessError as err:
    print("ERROR:", err)
else:
    print("returncode:", completed.returncode)
    print("stdout is {!r}".format(completed.stdout))
    print("stderr is {!r}".format(completed.stderr))

# 某些情况下，输出不应该被展示和捕获，使用 DEVNULL 抑制输出流。
try:
    completed = subprocess.run(
        "echo to stdout; echo to stderr 1>&2; exit 1",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
except subprocess.CalledProcessError as err:
    print("ERROR:", err)
else:
    print("returncode:", completed.returncode)
    print("stdout is {!r}".format(completed.stdout))
    print("stderr is {!r}".format(completed.stderr))
