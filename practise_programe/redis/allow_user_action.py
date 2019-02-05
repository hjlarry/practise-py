import time
import redis

client = redis.StrictRedis()

## 简单限流方案
def is_action_allowed(user_id, action_key, period, max_count):
    # 指定用户某个action在一个时间周期period秒内最大的行为数量max_count
    key = f"hist:{user_id}:{action_key}"
    now_ts = int(time.time() * 1000)  # 毫秒时间戳
    with client.pipeline() as pipe:
        pipe.zadd(key, now_ts, now_ts)  # score 和 value都使用毫秒时间戳
        # 移除时间窗口之前的行为记录，剩下的都是时间窗口内的
        pipe.zremrangebyscore(key, 0, now_ts - period * 1000)
        # 获取时间窗口内的行为数量
        pipe.zcard(key)
        # 设置过期时间，避免冷用户持续占用内存
        # 过期时间应为时间窗口的过期时间再宽限一秒
        pipe.expire(key, period + 1)
        _, _, current_count, _ = pipe.execute()
    return current_count <= max_count


# 调用这个接口 , 一分钟内只允许最多回复 5 个帖子
can_reply = is_action_allowed("laoqian", "reply", 60, 5)
if can_reply:
    # do_reply()
    pass
else:
    raise Exception()


## 单机漏斗限流方案
class Funnel:
    def __init__(self, capacity, leaking_rate):
        self.capacity = capacity  # 漏斗容量
        self.leaking_rate = leaking_rate  # 漏斗流速
        self.left_quota = capacity  # 漏斗剩余空间
        self.leaking_ts = time.time()  # 上次漏水时间

    def make_space(self):
        now_ts = time.time()
        delta_ts = now_ts - self.leaking_ts  # 距离上次漏水时间
        delta_quota = delta_ts * self.leaking_rate  # 腾出多少漏斗空间
        if delta_quota < 1:  # 腾的空间太少，等下次
            return
        self.left_quota += delta_quota
        self.leaking_ts = now_ts
        if self.left_quota > self.capacity:  # 剩余空间不会多余漏斗容量
            self.left_quota = self.capacity

    def watering(self, quota):
        self.make_space()
        if self.left_quota >= quota:  # 判断剩余空间是否足够
            self.left_quota -= quota
            return True
        return False


funnels = {}


def is_action_allowed2(user_id, action_key, capacity, leaking_rate):
    key = f"{user_id}:{action_key}"
    funnel = funnels.get(key)
    if not funnel:
        funnel = Funnel(capacity, leaking_rate)
        funnels[key] = funnel
    return funnel.watering(1)


for i in range(20):
    print(is_action_allowed("laoqian", "reply", 15, 0.5))

#  redis-cell限流模块提供了以上思路的分布式解决方案
# 指令 cl.throttle laoqian:reply 15 30 60 1
