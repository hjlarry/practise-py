import trace
from recurse import rescurse

"""
count
布尔类型。是否打开行计数。默认为 True。

countfuncs
布尔类型。是否统计函数的调用列表。默认 False。

countcallers
布尔类型。是否追踪调用者和被调用者。默认 False 。

ignoremods
序列。追踪覆盖时忽略的模块或包。默认是空元组。

ignoredirs
序列。要忽略的模块和包的目录。默认是空元组。

infile
包含已经抓取的计数值的文件的名称。默认是 None.

outfile
用于存储计数值的文件名。默认是 None，也就是不存储。
"""

tracer = trace.Trace(count=True, trace=True)
tracer.run("rescurse(2)")

results = tracer.results()
results.write_results()
