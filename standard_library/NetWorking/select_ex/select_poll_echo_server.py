import select
import socket
import sys
import queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server_addr = ("localhost", 10000)
server.bind(server_addr)
server.listen(5)

messages_queues = {}

TIMEOUT = 1000

READ_ONLY = select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
READ_WRITE = READ_ONLY | select.POLLOUT
poller = select.poll()
poller.register(server, READ_ONLY)

# Map file descriptors to socket objects
fd_to_socket = {server.fileno(): server}

while True:
    print("waiting for the next event", file=sys.stderr)
    events = poller.poll(TIMEOUT)
    for fd, flag in events:
        # Retrieve the actual socket from its file descriptor
        s = fd_to_socket[fd]
        if flag & (select.POLLIN | select.POLLPRI):
            if s is server:
                conn, client_addr = s.accept()
                print("conn from ", client_addr, file=sys.stderr)
                conn.setblocking(0)
                fd_to_socket[conn.fileno()] = conn
                poller.register(conn, READ_ONLY)
                messages_queues[conn] = queue.Queue()
            else:
                data = s.recv(1024)
                if data:
                    print(f"received {data} from {s.getpeername()}", file=sys.stderr)
                    messages_queues[s].put(data)
                    poller.modify(s, READ_WRITE)
                else:
                    print("closing ", client_addr, file=sys.stderr)
                    poller.unregister(s)
                    s.close()
                    del messages_queues[s]
        # The POLLHUP flag indicates a client that “hung up” the connection without closing it cleanly.
        # The server stops polling clients that disappear.
        elif flag & select.POLLHUP:
            print(' closing', client_addr, '(HUP)', file=sys.stderr)
            poller.unregister(s)
            s.close()
        elif flag & select.POLLOUT:
            try:
                next_msg = messages_queues[s].get_nowait()
            except queue.Empty:
                print(f"{s.getpeername()} queue empty")
                poller.modify(s, READ_WRITE)
            else:
                print(f"sending {next_msg} to {s.getpeername()}")
                s.send(next_msg)
        elif flag & select.POLLERR:
            print(f"exception condition on {s.getpeername()}", file=sys.stderr)
            poller.unregister(s)
            s.close()
            del messages_queues[s]


