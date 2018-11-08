import cProfile
import pstats
from profile_fib import fib1, fib_seq1

for i in range(5):
    filename = f"profile_stats_{i}.stats"
    cProfile.run(f"print({i}, fib_seq1(20))", filename)

# 用同一个对象读取全部的5个统计文件。
stats = pstats.Stats("profile_stats_0.stats")
for i in range(5):
    stats.add(f"profile_stats_{i}.stats")

# 清理报告文件
stats.strip_dirs()
# 以累积花费的时间进行排序
stats.sort_stats("cumulative")
stats.print_stats()
# 限制输出，只能是"(fib"的才能输出。
stats.print_stats(r"\(fib")


print('INCOMING CALLERS:')
stats.print_callers(r'\(fib')

print('OUTGOING CALLEES:')
stats.print_callees(r'\(fib')