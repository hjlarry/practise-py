import selectors
import socket

mysel = selectors.DefaultSelector()
keep_running = True
out_going = [b"this is a message", b"it will be repeated"]
bytes_sent = 0
bytes_received = 0


server_addr = ("localhost", 10000)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_addr)
sock.setblocking(False)


mysel.register(sock, selectors.EVENT_READ | selectors.EVENT_WRITE)


while keep_running:
    print("waiting for i/o")
    for key, mask in mysel.select(timeout=1):
        conn = key.fileobj
        client_addr = conn.getpeername()
        print("client ", client_addr)

        if mask & selectors.EVENT_READ:
            print("ready to read")
            data = conn.recv(1024)
            if data:
                print("received", data)
                bytes_received += len(data)
            # Interpret empty result as closed conn, and also close when we have received a copy of all the data sent
            keep_running = not (
                data or (bytes_received and (bytes_received == bytes_sent))
            )

        if mask & selectors.EVENT_WRITE:
            print("ready to write")
            if not out_going:
                # we are out of msg, so we no longer need to write anything.
                # change our registration to let us keep reading response from server
                print("switching to read only")
                mysel.modify(sock, selectors.EVENT_READ)
            else:
                # send the next message
                next_msg = out_going.pop()
                print("sending ", next_msg)
                sock.sendall(next_msg)
                bytes_sent += len(next_msg)


print("shuting down")
mysel.unregister(conn)
conn.close()
mysel.close()
