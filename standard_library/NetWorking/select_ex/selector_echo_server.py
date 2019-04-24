import selectors
import socket

# 该server 也可以搭配select_echo_slow_client.py一起测试

server_addr = ("localhost", 10000)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server.bind(server_addr)
server.listen(5)

mysel = selectors.DefaultSelector()
keep_running = True


# 读事件的回调函数
def read(conn, mask):
    global keep_running

    client_addr = conn.getpeername()
    print(f"read({client_addr})")
    data = conn.recv(1024)
    if data:
        print("received ", data)
        # 返回消息
        conn.sendall(data + b" by server")
    else:
        # 未接受到数据说明客户端断开了连接
        print("closing")
        mysel.unregister(conn)
        conn.close()
        # 可以在这里关掉主进程
        # keep_running = False


# 接受新连接时的回调函数
def accept(sock, mask):
    new_conn, addr = sock.accept()
    print("accept ", addr)
    new_conn.setblocking(False)
    # 注册new_conn套接字可读时，调用read回调
    mysel.register(new_conn, selectors.EVENT_READ, read)


# 注册server套接字可读时，调用accept回调
mysel.register(server, selectors.EVENT_READ, accept)

while keep_running:
    print("waiting for i/o")
    for key, mask in mysel.select(timeout=1):
        callback = key.data
        callback(key.fileobj, mask)

print("shuting down")
mysel.close()
