# 要求

假设我们想访问 http://httpbin.org/get 这样的链接，但是由于某些原因不能直接访问，可以做一个端口转发，从一个中间服务里面转发流量。



这个还可以用在跳板机上，假如线上服务器为了访问安全，通常不可直接登录，需要跳板机登录。如果本地想访问服务器的如MySQL服务怎么办呢？可以在跳板机上做一个端口转发，也就是访问跳板机的XX端口，其实就是访问线上服务器的3308端口，这样就可以巧妙的实现访问了。



我们将写这样的一个程序：



```

python portforwarder.py -s httpbin.org  -l 8888 -p 80

```



这样访问 http://localhost:8888/get 就相当于访问 http://httpbin.org:8888/get. 另外这个脚本支持命令行解析：



```

python portforwarder.py -h

usage: portforwarder.py [-h] [-l LOCAL_PORT] [-s SOURCE] [-p PORT]



A port forward command tool using asyncio



optional arguments:

  -h, --help     show this help message and exit

  -l LOCAL_PORT  The port to bind to.

  -s SOURCE      Forward source-address

  -p PORT        Forward source-port

```