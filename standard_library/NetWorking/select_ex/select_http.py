import socket
import selectors
from urllib.parse import urlparse
import time

# epoll并不一定比select好， 并发高、连接不活跃的情况下，epoll比select好；并发不高、连接活跃时，select比epoll好
selector = selectors.DefaultSelector()
urls = []
stop = False


class Fetcher:
    def __init__(self, url):
        self.spider_url = url
        url = urlparse(url)
        self.host, self.path = url.netloc, url.path
        self.data = b""
        self.path = "/" if not self.path else self.path
        self.client = socket.socket()

    def connected(self, key):
        selector.unregister(key.fd)
        msg = (
            f"GET {self.path} HTTP/1.1\r\nHost: {self.host}\r\nConnection:close\r\n\r\n"
        )
        # 和非阻塞IO形成对比，不在需要轮询尝试send，selector注册了事件调用了回调说明状态已经就绪了
        self.client.send(msg.encode("utf-8"))
        # 监听socket能不能读，能读则可接收数据
        selector.register(self.client.fileno(), selectors.EVENT_READ, self.readable)

    def readable(self, key):
        # 接收数据之后不需要再while去确保receive完整的数据，这一步应由selector去做
        d = self.client.recv(1024)
        if d:
            self.data += d
        else:
            selector.unregister(key.fd)
            data = self.data.decode("utf8")
            print(data)
            self.client.close()
            urls.remove(self.spider_url)
            if not urls:
                global stop
                stop = True

    def get_url(self):
        self.client.setblocking(False)
        try:
            self.client.connect((self.host, 80))
        except BlockingIOError as e:
            pass
        # 建立连接之后，使用socket的文件描述符注册监听其可写时，调用回调函数
        selector.register(self.client.fileno(), selectors.EVENT_WRITE, self.connected)

# selector的回调是需要程序员去监听并执行回调的，所以这里建立事件循环不断去找到ready状态的socket并处理其回调
def event_loop():
    while not stop:
        ready = selector.select()
        for key, mask in ready:
            callback = key.data
            callback(key)


if __name__ == "__main__":
    start_time = time.time()
    for url in range(20):
        url = f"http://shop.projectsedu.com/goods/{url}/"
        urls.append(url)
        fetch = Fetcher(url)
        fetch.get_url()
    event_loop()
    print(time.time() - start_time)
