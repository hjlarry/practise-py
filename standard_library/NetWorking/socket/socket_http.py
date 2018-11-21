import socket
import time

# 默认阻塞式IO, connect运行得到结果了才会运行send
def block_io():
    print("start")
    client = socket.socket()
    client.connect(("www.baidu.com", 80))
    msg = "GET / HTTP/1.1\r\n\r\n"
    client.send(msg.encode("utf-8"))
    data = b""
    while True:
        d = client.recv(1024)
        if d:
            data += d
        else:
            break
    print(data.decode("utf-8"))
    client.close()


# 非阻塞式IO，在connect后需要不断轮询检查状态是否已连接才能去调用send，否则会BlockingIOError。
# 这种轮询相对于阻塞式IO是消耗CPU资源的，但在做其他计算型任务或发起其他的连接需求时是有意义的
def non_block_io():
    print("start")
    client = socket.socket()
    client.setblocking(False)
    try:
        client.connect(("www.baidu.com", 80))
    except BlockingIOError as e:
        pass
    while True:
        try:
            msg = "GET / HTTP/1.1\r\nHost: www.baidu.com\r\nConnection:close\r\n\r\n"
            client.send(msg.encode("utf-8"))
            break
        except OSError as e:
            pass

    data = b""
    while True:
        try:
            d = client.recv(1024)
        except BlockingIOError as e:
            continue
        if d:
            data += d
        else:
            break
    print(data.decode("utf-8"))
    client.close()


non_block_io()
