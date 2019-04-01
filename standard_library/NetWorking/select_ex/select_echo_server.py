import select
import socket
import sys
import queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server_addr = ("localhost", 10000)
server.bind(server_addr)

server.listen(5)

# select() 中的参数是三个包含向监听器通信渠道的列表。第一个列表中的对象用于检测即将读取的数据，第二个列表包含的对象会在缓存区有空间的时候接收传出的数据，第三个则是接收它们执行期间发生的错误（通常是输入和输出对象的结合）。
inputs = [server]
outputs = []
messages_queues = {}

while inputs:
    print("wait for the next event", file=sys.stderr)
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
    for s in readable:
        if s is server:
            # a readable socket is ready to accept a conn
            conn, client_addr = s.accept()
            print("conn from ", client_addr, file=sys.stderr)
            conn.setblocking(0)
            inputs.append(conn)
            # give the conn a queue for data we want to send
            messages_queues[conn] = queue.Queue()
        else:
            data = s.recv(1024)
            if data:
                print(f"received {data} from {s.getpeername()}", file=sys.stderr)
                messages_queues[s].put(data)
                # add output channel for response
                if s not in outputs:
                    outputs.append(s)
            else:
                print("closing ", client_addr, file=sys.stderr)
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del messages_queues[s]

    for s in writable:
        try:
            next_msg = messages_queues[s].get_nowait()
        except queue.Empty:
            print(f"{s.getpeername()} queue empty")
            outputs.remove(s)
        else:
            print(f"sending {next_msg} to {s.getpeername()}")
            s.send(next_msg)

    for s in exceptional:
        print(f"exception condition on {s.getpeername()}", file=sys.stderr)
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del messages_queues[s]
