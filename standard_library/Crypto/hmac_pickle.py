import hashlib
import hmac
import io
import pickle
import pprint


def make_digest(msg):
    hash_value = hmac.new(b"secret-key", msg, hashlib.sha1)
    return hash_value.hexdigest().encode("utf-8")


class SimpleObj:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


out_s = io.BytesIO()
# 往流中写入一个有效的对象
o = SimpleObj("digest matches")
pickle_data = pickle.dumps(o)
digest = make_digest(pickle_data)
header = b"%s %d\n" % (digest, len(pickle_data))
print(f"WRITING: {header}")
out_s.write(header)
out_s.write(pickle_data)
# 往流中写入一个无效的对象
o = SimpleObj("digest does not match")
pickled_data = pickle.dumps(o)
digest = make_digest(b"not the pickled data at all")
header = b"%s %d\n" % (digest, len(pickled_data))
print("\nWRITING: {}".format(header))
out_s.write(header)
out_s.write(pickled_data)

out_s.flush()

in_s = io.BytesIO(out_s.getvalue())

while True:
    first_line = in_s.readline()
    if not first_line:
        break

    incoming_digest, incoming_length = first_line.split(b' ')
    incoming_length = int(incoming_length.decode('utf-8'))
    print('\n Read:', incoming_digest, incoming_length)

    incoming_pickled_data = in_s.read(incoming_length)
    actual_digest = make_digest(incoming_pickled_data)
    print('ACTUAL:', actual_digest)

    if hmac.compare_digest(actual_digest, incoming_digest):
        obj = pickle.loads(incoming_pickled_data)
        print('OK:', obj)
    else:
        print('Warning: data corruption')
