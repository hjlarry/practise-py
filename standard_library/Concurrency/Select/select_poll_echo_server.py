import select
import socket
import sys
import queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server_addr = ("localhost", 10000)
server.bind(server_addr)
server.listen(5)

messages_queues = {}

TIMEOUT = 1000

READ_ONLY = select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
READ_WRITE = READ_ONLY | select.POLLOUT
poller = select.poll()
# 注册server套接字，这样所有要连接的客户端或发送的数据都会触发一个事件
poller.register(server, READ_ONLY)

# 因为poll()的返回是一个文件描述符和事件标识的元组列表，为了后续能找到对应的套接字，我们存一个字典
fd_to_socket = {server.fileno(): server}

# 不断调用poll()，之后根据返回的事件做进一步处理
while True:
    print("waiting for the next event", file=sys.stderr)
    events = poller.poll(TIMEOUT)
    for fd, flag in events:
        # 通过文件描述符找对应的套接字
        s = fd_to_socket[fd]
        # 相当于inputs
        if flag & (select.POLLIN | select.POLLPRI):
            # 新连接的情况
            if s is server:
                conn, client_addr = s.accept()
                print("conn from ", client_addr, file=sys.stderr)
                conn.setblocking(False)
                # 存客户端文件描述符和套接字的映射，注册该套接字，并将其放到消息队列中去
                fd_to_socket[conn.fileno()] = conn
                poller.register(conn, READ_ONLY)
                messages_queues[conn] = queue.Queue()
            # 新数据的情况
            else:
                data = s.recv(1024)
                if data:
                    print(f"received {data} from {s.getpeername()}", file=sys.stderr)
                    # 确定要返回什么数据
                    messages_queues[s].put(data + b" by server")
                    # 修改套接字标识，相当于添加到outputs
                    poller.modify(s, READ_WRITE)
                # 客户端断开连接的情况
                else:
                    print("closing ", s.getpeername(), file=sys.stderr)
                    poller.unregister(s)
                    s.close()
                    del messages_queues[s]
        # POLLHUP 标识表示某客户端处于挂起状态，没有正确的关闭，服务器应停止轮询该客户端
        elif flag & select.POLLHUP:
            print(" closing", s.getpeername(), "(HUP)", file=sys.stderr)
            poller.unregister(s)
            s.close()
        # 套接字准备好发送数据
        elif flag & select.POLLOUT:
            try:
                next_msg = messages_queues[s].get_nowait()
            except queue.Empty:
                print(f"{s.getpeername()} queue empty")
                # 无消息要发送时，应改回 READ_ONLY
                poller.modify(s, READ_ONLY)
            else:
                print(f"sending {next_msg} to {s.getpeername()}")
                s.send(next_msg)
        # 处理异常，这里直接做了关闭处理
        elif flag & select.POLLERR:
            print(f"exception condition on {s.getpeername()}", file=sys.stderr)
            poller.unregister(s)
            s.close()
            del messages_queues[s]
