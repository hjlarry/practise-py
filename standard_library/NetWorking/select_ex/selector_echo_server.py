import selectors
import socket

mysel = selectors.DefaultSelector()
keep_running = True


def read(conn, mask):
    "callback for read events"
    global keep_running

    client_addr = conn.getpeername()
    print(f"read({client_addr})")
    data = conn.recv(1024)
    if data:
        # A readable client socket has data
        print("received ", data)
        conn.sendall(data)
    else:
        # interpret empty result as closed conn
        print("closing")
        mysel.unregister(conn)
        conn.close()
        # Tell the main loop to stop
        keep_running = False


def accept(sock, mask):
    "Call back for new conn"
    new_conn, addr = sock.accept()
    print("accept ", addr)
    new_conn.setblocking(False)
    mysel.register(new_conn, selectors.EVENT_READ, read)


server_addr = ("localhost", 10000)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server.bind(server_addr)
server.listen(5)

mysel.register(server, selectors.EVENT_READ, accept)

while keep_running:
    print("waiting for i/o")
    for key, mask in mysel.select(timeout=1):
        callback = key.data
        callback(key.fileobj, mask)

print("shuting down")
mysel.close()
