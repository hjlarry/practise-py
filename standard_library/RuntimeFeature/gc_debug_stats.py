import gc

gc.set_debug(gc.DEBUG_STATS)

gc.collect()
# 输出显示有两次单独的运行，一次是我们手动运行，一次是解释器退出时自动执行
print('exiting')