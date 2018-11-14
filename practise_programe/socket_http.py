import socket

print("start")
client = socket.socket()
client.connect(("www.baidu.com", 80))
msg = "GET / HTTP/1.1\r\n\r\n"

client.send(msg.encode("utf-8"))
data = b""
while True:
    d = client.recv(1024)
    if d:
        data += d
    else:
        break
print(data.decode("utf-8"))
client.close()
