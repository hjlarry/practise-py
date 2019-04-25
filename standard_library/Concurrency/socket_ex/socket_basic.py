import socket
import binascii
import os
from urllib.parse import urlparse

print("一、 socket.gethostname:")
print(socket.gethostname())

print()
print("二、 socket.gethostbyname:")
HOSTS = ["hejldeIMAC.local", "pymotw.com", "www.python.org", "nosuchname"]

for host in HOSTS:
    try:
        print(f"{host}: {socket.gethostbyname(host)}")
    except socket.error as msg:
        print(msg)

print()
print("三、 socket.gethostbyname_ex:")
for host in HOSTS:
    try:
        name, aliases, addresses = socket.gethostbyname_ex(host)
        print(f"{host}:")
        print(f"{name}")
        print(f"{aliases}")
        print(f"{addresses}")
        print()
    except socket.error as msg:
        print(msg)

print()
print("四、 socket.getfqdn:")
for host in HOSTS:
    try:
        print(f"{host}: {socket.getfqdn(host)}")
    except socket.error as msg:
        print(msg)

print()
print("五、 socket.gethostbyaddr:")
hostname, aliases, addresses = socket.gethostbyaddr("66.33.211.242")
print(hostname)
print(aliases)
print(addresses)

print()
print("六、 socket.getservbyname:")
URLS = [
    "http://www.python.org",
    "https://www.mybank.com",
    "ftp://prep.ai.mit.edu",
    "gopher://gopher.micro.umn.edu",
    "smtp://mail.example.com",
    "imap://mail.example.com",
    "imaps://mail.example.com",
    "pop3://pop.example.com",
    "pop3s://pop.example.com",
]
for url in URLS:
    parsed_url = urlparse(url)
    port = socket.getservbyname(parsed_url.scheme)
    print(f"{parsed_url.scheme} : {port}")

print()
print("七、 socket.getservbyport:")
for port in [80, 443, 21, 70, 25, 143, 993, 110, 995]:
    url = "{}://example.com/".format(socket.getservbyport(port))
    print(url)


print()
print("八、 socket.getaddrinfo:")


def get_constants(prefix):
    return {getattr(socket, n): n for n in dir(socket) if n.startswith(prefix)}


families = get_constants("AF_")
types = get_constants("SOCK_")
protocols = get_constants("IPPROTO_")

for res in socket.getaddrinfo("www.python.org", 80):
    family, socketype, proto, canonname, sockaddr = res
    print("Family:", families[family])
    print("Socketype:", types[socketype])
    print("Proto:", protocols[proto])
    print("Canonname:", canonname)
    print("Sockaddr:", sockaddr)
    print()

print()
print("九、 socket.inet_aton:")
for str_addr in ["192.168.1.1", "127.0.0.1"]:
    packed = socket.inet_aton(str_addr)
    print("Origin:", str_addr)
    print("Packed:", binascii.hexlify(packed))
    print("Packed:", packed)
    print("Unpacked:", socket.inet_ntoa(packed))

print()
print("十、 父子进程通信:")
parent, child = socket.socketpair()

pid = os.fork()
if pid:
    print("In parent, sending message")
    child.close()
    parent.sendall(b"ping")
    response = parent.recv(1024)
    print("response from child:", response)
    parent.close()
else:
    print("In child, waiting for message")
    parent.close()
    message = child.recv(1024)
    print("message from parent", message)
    child.sendall(b"pong")
    child.close()
