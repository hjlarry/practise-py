# 工厂方法模式
# 源自 celery/kombu
TRANSPORT_ALIASES = {
    "amqp": "kombu.transport.pyamqp:Transport",
    "memory": "kombu.transport.memory:Transport",
    "redis": "kombu.transport.redis:Transport",
    "mongodb": "kombu.transport.mongodb:Transport",
}
_transport_cache = {}


def symbol_by_name(transport):
    pass


def resolve_transport(transport=None):  # 原函数更复杂
    transport = TRANSPORT_ALIASES[transport]
    return symbol_by_name(transport)  # 把字符串转化为对象


def get_transport_cls(transport=None):
    if transport not in _transport_cache:
        _transport_cache[transport] = resolve_transport(transport)
    return _transport_cache[transport]


"""
In : from kombu.transport import get_transport_cls
In : get_transport_cls('redis')
Out: kombu.transport.redis.Transport
In : get_transport_cls('amqp')
Out: kombu.transport.pyamqp.Transport
"""
