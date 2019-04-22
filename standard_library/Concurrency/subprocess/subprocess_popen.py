import subprocess
import io

print("一、 与进程单向通信")
print("read:")
proc = subprocess.Popen(["echo", "to stdout"], stdout=subprocess.PIPE)
# proc = subprocess.Popen(["ls", "-l"], stdout=subprocess.PIPE)
value = proc.communicate()
print(value)
stdout_value = value[0].decode("utf-8")
print(stdout_value)

print("write:")
proc = subprocess.Popen(["cat", "-"], stdin=subprocess.PIPE)
proc.communicate("stdin:sth".encode("utf-8"))

print()
print()
print("二、 与进程双向通信:")
proc = subprocess.Popen(
    'cat -; echo "to stderr" 1>&2',
    shell=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
msg = "through stdin to stdout".encode("utf-8")
stdout_value, stderr_value = proc.communicate(msg)
print(stdout_value)
print(stderr_value)

print()
print("三、 管道连接:")
# 相当于 $cat signal.ipynb | grep "def" | cut -b -30
cat = subprocess.Popen(["cat", "subprocess.ipynb"], stdout=subprocess.PIPE)
grep = subprocess.Popen(["grep", "def"], stdin=cat.stdout, stdout=subprocess.PIPE)
cut = subprocess.Popen(["cut", "-b", "-30"], stdin=grep.stdout, stdout=subprocess.PIPE)
for line in cut.stdout:
    print(line)

print()
print("四、 与另一个命令行去交互:")
print("one line at a time:")
proc = subprocess.Popen(
    "python3 repeater.py", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
)
stdin = io.TextIOWrapper(proc.stdin, encoding="utf-8", line_buffering=True)
stdout = io.TextIOWrapper(proc.stdout, encoding="utf-8")
for i in range(5):
    line = f"{i} \n"
    stdin.write(line)
    output = stdout.readline()
    print(output)

remainder = proc.communicate()[0].decode("utf-8")
print(remainder)

print()
print("All line at a time:")
proc = subprocess.Popen(
    "python3 repeater.py", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE
)
stdin = io.TextIOWrapper(proc.stdin, encoding="utf-8")
stdout = io.TextIOWrapper(proc.stdout, encoding="utf-8")
for i in range(5):
    line = f"{i} \n"
    stdin.write(line)
stdin.flush()

remainder = proc.communicate()[0].decode("utf-8")
print(remainder)
