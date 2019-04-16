import threading
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy

# 由于 XML-RPC 将所有数据都序列化为XML格式，所以它会比其他的方式运行的慢一些。
# 但是它也有优点，这种方式的编码可以被绝大部分其他编程语言支持。
class KeyValueServer:
    _rpc_methods_ = ["get", "set", "delete", "exists", "keys"]

    def __init__(self, address):
        self._data = {}
        self._serv = SimpleXMLRPCServer(address, allow_none=True)
        for name in self._rpc_methods_:
            self._serv.register_function(getattr(self, name))

    def get(self, name):
        return self._data[name]

    def set(self, name, value):
        self._data[name] = value

    def delete(self, name):
        del self._data[name]

    def exists(self, name):
        return name in self._data

    def keys(self):
        return list(self._data)

    def serve_forever(self):
        self._serv.serve_forever()


kvserv = KeyValueServer(("", 15000))
t = threading.Thread(target=kvserv.serve_forever)
t.setDaemon(True)
t.start()


s = ServerProxy("http://localhost:15000", allow_none=True)
s.set("foo", "bar")
s.set("spam", [1, 2, 3])
print(s.keys())
print(s.get("foo"))
print(s.get("spam"))
print(s.delete("spam"))
print(s.exists("spam"))
