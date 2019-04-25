import select
import socket
import sys
import queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server_addr = ("localhost", 10000)
server.bind(server_addr)

server.listen(5)

# select() 中的参数是三个包含向监听器通信渠道的列表。
# 第一个列表中的对象用于检测即将读取的数据
# 第二个列表包含的对象会在缓存区有空间的时候接收传出的数据
# 第三个则是接收它们执行期间发生的错误
inputs = [server]
outputs = []
errors = []
messages_queues = {}

while inputs:
    print("wait for the next event", file=sys.stderr)
    readable, writable, exceptional = select.select(inputs, outputs, errors)

    # 针对可读套接字，有以下三种情况
    for s in readable:
        # 如果它是一个服务端套接字，而且可读，意味着它在准备好接受一个新的传入连接
        # 那么需要将对端套接字设置为非阻塞，并将其添加到inputs中去
        if s is server:
            conn, client_addr = s.accept()
            print("conn from ", client_addr, file=sys.stderr)
            conn.setblocking(False)
            inputs.append(conn)
            # 先给对端套接字一个空的队列
            messages_queues[conn] = queue.Queue()
        else:
            # 另一种情况是客户端套接字，我们先接收数据
            data = s.recv(1024)
            # 若接收到数据，我们把它放到output中，这样就可以之后通过该套接字返回数据给客户端
            if data:
                print(f"received {data} from {s.getpeername()}", file=sys.stderr)
                # 消息队列中放要返回给客户端的数据
                messages_queues[s].put(data + b"  by_server")
                if s not in outputs:
                    outputs.append(s)
            # 若未接收到数据，说明客户端已断开连接了
            else:
                print("closing ", s.getpeername(), file=sys.stderr)
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del messages_queues[s]

    # 针对可写套接字
    for s in writable:
        try:
            # 先从消息队列中拿，看是否有消息要返回给客户端
            next_msg = messages_queues[s].get_nowait()
        except queue.Empty:
            print(f"{s.getpeername()} queue empty")
            # 没有则把连接从输出列表中移除
            outputs.remove(s)
        else:
            print(f"sending {next_msg} to {s.getpeername()}")
            # 有则把消息发送给客户端
            s.send(next_msg)

    for s in exceptional:
        print(f"exception condition on {s.getpeername()}", file=sys.stderr)
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del messages_queues[s]
