import logging
import os
import socketserver
import threading
import socket
import time

logging.basicConfig(level=logging.DEBUG, format="%(name)s : %(message)s")

print("一、 默认的TCPServer")


class EchoRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger("EchoRequestHandler")
        self.logger.debug("__init__")
        super().__init__(request, client_address, server)

    def setup(self):
        self.logger.debug("setup")
        super().setup()

    def handle(self):
        self.logger.debug("handle")
        data = self.request.recv(1024)
        self.logger.debug("receive --> %s", data)
        self.request.send(data)

    def finish(self):
        self.logger.debug("finish")
        return super().finish()


class EchoServer(socketserver.TCPServer):
    def __init__(self, server_address, handler_class=EchoRequestHandler):
        self.logger = logging.getLogger("EchoServer")
        self.logger.debug("__init__")
        super().__init__(server_address, handler_class)

    def server_activate(self):
        self.logger.debug("server_activate")
        super().server_activate()

    def serve_forever(self, poll_interval=0.5):
        self.logger.debug("server_forever, waiting for request")
        self.logger.info("Handing requests, press <ctrl-c> to quit")
        super().serve_forever(poll_interval)

    def handle_request(self):
        self.logger.debug("handle_request")
        return super().handle_request()

    def verify_request(self, request, client_address):
        self.logger.debug(f"verify_request({request} {client_address})")
        return super().verify_request(request, client_address)

    def process_request(self, request, client_address):
        self.logger.debug(f"process_request({request} {client_address})")
        return super().process_request(request, client_address)

    def server_close(self):
        self.logger.debug("server_close")
        return super().server_close()

    def finish_request(self, request, client_address):
        self.logger.debug(f"finish_request({request} {client_address})")
        return super().finish_request(request, client_address)

    def close_request(self, request_address):
        self.logger.debug(f"close_request({request_address})")
        return super().close_request(request_address)

    def shutdown(self):
        self.logger.debug("shutdown")
        return super().shutdown()


address = ("localhost", 0)  # let the kernel assign a port
server = EchoServer(address, EchoRequestHandler)
ip, port = server.server_address

# start the server in a thread
t = threading.Thread(target=server.serve_forever)
t.setDaemon(True)
t.start()

logger = logging.getLogger("client")
logger.info(f"Server on {ip} {port}")
logger.debug("creating socket")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

# sending data
message = "hello world ".encode()
logger.debug("sending data : %r", message)
len_sent = s.send(message)

# receive res
response = s.recv(len_sent)
logger.debug("response from server: %r", response)

server.shutdown()
s.close()
server.socket.close()


time.sleep(1)
print()
print("二、 添加了ThreadingMixIn")


class ThreadedEchoRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # echo the back to the client
        data = self.request.recv(1024)
        cur_thread = threading.currentThread()
        res = b"%s:%s" % (cur_thread.getName().encode(), data)
        self.request.send(res)


# same as socketserver.ThreadingTCPServer
class ThreadedEchoServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


address = ("localhost", 0)  # let the kernel assign a port
server = socketserver.ThreadingTCPServer(address, ThreadedEchoRequestHandler)
ip, port = server.server_address

# start the server in a thread
t = threading.Thread(target=server.serve_forever)
t.setDaemon(True)
t.start()
print("server runing on ", t.getName())


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

# sending data
message = "hello world ".encode()
print("sending data : ", message)
len_sent = s.send(message)
print("length:", len_sent)
# receive res
response = s.recv(1024)
print("response from server: ", response)

server.shutdown()
s.close()
server.socket.close()

print()
print("三、 添加了ForkingMixIn")


class ForkingEchoRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # echo the back to the client
        data = self.request.recv(1024)
        cur_pid = os.getpid()
        res = b"%d:%s" % (cur_pid, data)
        self.request.send(res)


# same as socketserver.ForkingTCPServer
class ForkingEchoServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


address = ("localhost", 0)  # let the kernel assign a port
server = ForkingEchoServer(address, ForkingEchoRequestHandler)
ip, port = server.server_address

# start the server in a thread
t = threading.Thread(target=server.serve_forever)
t.setDaemon(True)
t.start()
print("server runing on ", os.getpid())


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

# sending data
message = "hello world ".encode()
print("sending data : ", message)
len_sent = s.send(message)
print("length:", len_sent)
# receive res
response = s.recv(1024)
print("response from server: ", response)

server.shutdown()
s.close()
server.socket.close()


print()
print("四、 使用StreamRequestHandler")

# 比BaseRequestHandler更加灵活，能通过设置其他的类变量来支持一些新的特性
class EchoHandler(socketserver.StreamRequestHandler):
    # Optional settings (defaults shown)
    timeout = 5  # Timeout on all socket operations
    rbufsize = -1  # Read buffer size
    wbufsize = 0  # Write buffer size
    disable_nagle_algorithm = False  # Sets TCP_NODELAY socket option

    def handle(self):
        print("Got connection from", self.client_address)
        try:
            for line in self.rfile:
                # self.wfile is a file-like object for writing
                self.wfile.write(line)
        except socket.timeout:
            print("Timed out!")


address = ("localhost", 0)  # let the kernel assign a port
server = socketserver.ThreadingTCPServer(address, EchoHandler)
ip, port = server.server_address

# start the server in a thread
t = threading.Thread(target=server.serve_forever)
t.setDaemon(True)
t.start()
print("server runing on ", t.getName())


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

# sending data
message = "hello world ".encode()
print("sending data : ", message)
len_sent = s.send(message)
print("length:", len_sent)
# receive res
response = s.recv(1024)
print("response from server: ", response)

server.shutdown()
s.close()
server.socket.close()
