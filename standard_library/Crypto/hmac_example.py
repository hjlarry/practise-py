import hmac
import base64
import hashlib

# new() 函数接受三个参数值，第一个是密钥，共享于两个通信的端点之间，所以两个端点都使用相同的值。
# 第二个参数是初始化消息值。如果需要认证的消息内容非常小，例如时间戳或者 HTTP POST，那么整个消息体可以传入 new() 而不用 update() 方法。
# 最后一个参数是要使用的摘要算法。默认的是  hashlib.md5
digest_maker = hmac.new(b"secret-shared-key")
with open("lorem.txt", "rb") as f:
    while True:
        block = f.read(1024)
        if not block:
            break
        digest_maker.update(block)

digest = digest_maker.hexdigest()
print(digest)
print()


with open("lorem.txt", "rb") as f:
    body = f.read()

hash_value = hmac.new(b"secret-shared-key", body, hashlib.sha1)
digest1 = hash_value.hexdigest()
print(digest1)
print(base64.encodestring(digest1.encode()))
