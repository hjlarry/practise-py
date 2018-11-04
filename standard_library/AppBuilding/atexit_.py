import atexit
def all_done():
    print('alldone()')

print('Registering')
atexit.register(all_done)
print('registered')

def my_cleanup(name):
    print(f"my_cleanup({name})")

atexit.register(my_cleanup, 'first')
atexit.register(my_cleanup, 'second')
# 最后注册最先执行
atexit.register(my_cleanup, 'third')

@atexit.register
def all_done1():
    print('alldone1()')

#  取消回调，若取消未注册的回调也不会引发异常
atexit.unregister(my_cleanup)