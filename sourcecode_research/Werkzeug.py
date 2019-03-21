from werkzeug.local import LocalStack, LocalProxy
test_stack = LocalStack()
test_stack.push({'abc': '123'})
test_stack.push({'abc': '1234'})

def get_item():
    return test_stack.pop()

# LocalProxy 需要初始化callable的对象，然后每次调用proxy时  内部会去call一次这个初始化对象。
item = LocalProxy(get_item)



print(item['abc'])
print(item['abc'])