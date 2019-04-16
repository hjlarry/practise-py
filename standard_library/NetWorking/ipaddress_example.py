import binascii
import ipaddress

print("一、 ip_address()")
ADDRESSES = ["10.9.0.6", "fdfd:87b5:b475:5e3e:b1bc:e121:a8eb:14aa"]

for ip in ADDRESSES:
    addr = ipaddress.ip_address(ip)
    print(f"{addr !r}")
    print("ip version", addr.version)
    print("is private", addr.is_private)
    print("packed from", binascii.hexlify(addr.packed))
    print("integer", int(addr))
print()
print("二、 ip_network()")
NETWORKS = ["10.9.0.0/24", "fdfd:87b5:b475:5e3e::/64"]

for n in NETWORKS:
    net = ipaddress.ip_network(n)
    print(f"{net !r}")
    print("is private", net.is_private)
    print("broadcast", net.broadcast_address)
    print("compressed", net.compressed)
    print("with netmask", net.with_netmask)
    print("with hostmask", net.with_hostmask)
    print("num addr", net.num_addresses)

for n in NETWORKS:
    net = ipaddress.ip_network(n)
    print(f"{net !r}")
    item = iter(net)
    print(next(item), next(item), next(item))
    host = iter(net.hosts())
    # net从0开始， host从1开始
    print(next(host), next(host), next(host))

print()
print("三、 判断ip in network")
NETWORKS = [
    ipaddress.ip_network("10.9.0.0/24"),
    ipaddress.ip_network("fdfd:87b5:b475:5e3e::/64"),
]

ADDRESSES = [
    ipaddress.ip_address("10.9.0.6"),
    ipaddress.ip_address("10.7.0.31"),
    ipaddress.ip_address("fdfd:87b5:b475:5e3e:b1bc:e121:a8eb:14aa"),
    ipaddress.ip_address("fe80::3840:c439:b25e:63b0"),
]

for ip in ADDRESSES:
    for net in NETWORKS:
        if ip in net:
            print(f"{ip} is in {net}")
            break
    else:
        print(f"{ip} is not a known network")

print()
print("四、 ip_interface()")
ADDRESSES = ["10.9.0.6/24", "fdfd:87b5:b475:5e3e:b1bc:e121:a8eb:14aa/64"]

for ip in ADDRESSES:
    iface = ipaddress.ip_interface(ip)
    print(f"{iface !r}")
    print("network", iface.network)
    print("ip", iface.ip)
    print("ip with prefixlen", iface.with_prefixlen)
    print("netmask", iface.netmask)
    print("hostmask", iface.hostmask)
