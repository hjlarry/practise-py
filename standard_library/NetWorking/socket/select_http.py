import socket
import selectors
from urllib.parse import urlparse
import time

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
        self.client.send(msg.encode("utf-8"))
        selector.register(self.client.fileno(), selectors.EVENT_READ, self.readable)

    def readable(self, key):
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
        selector.register(self.client.fileno(), selectors.EVENT_WRITE, self.connected)


def loop():
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
    loop()
    print(time.time() - start_time)
