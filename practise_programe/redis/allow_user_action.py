import time
import redis

client = redis.StrictRedis()


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
