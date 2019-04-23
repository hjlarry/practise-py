import select
import socket
import sys
import queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server_addr = ("localhost", 10000)
server.bind(server_addr)

server.listen(5)


inputs = [server]
outputs = []
messages_queues = {}

while inputs:
    print("wait for the next event", file=sys.stderr)
    timeout = 1
    # 这里与select_echo_server.py不同，多设置了超时参数和超时的处理
    readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)
    if not (readable or writable or exceptional):
        print("timeout , do some other work here", file=sys.stderr)
        continue
    for s in readable:
        if s is server:
            conn, client_addr = s.accept()
            print("conn from ", client_addr, file=sys.stderr)
            conn.setblocking(False)
            inputs.append(conn)
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
                print("closing ", s.getpeername(), file=sys.stderr)
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
