import time
import redis
import flask

r = redis.StrictRedis()
app = flask.Flask(__name__)


def time_to_key(current_time):
    # 将当前时间转化为keyname用于存储
    return "active.users:" + time.strftime("%M", time.localtime(current_time))


def keys_in_last_10_minutes():
    # 返回过去10分钟的keyname
    now = time.time()
    result = []
    for i in range(10):
        result.append(time_to_key(now - i * 60))
    return result


@app.route("/")
def visit():
    # 模拟用户访问，将UA做为用户ID存入当前时间的键中
    user_id = flask.request.headers.get("User-Agent")
    current_key = time_to_key(time.time())
    pipe = r.pipeline()
    pipe.sadd(current_key, user_id)
    pipe.expire(current_key, 10 * 60)
    pipe.execute()
    return f"User:\t {user_id} <br> Key:\t {current_key}"


@app.route("/online")
def online():
    # 查看当前的用户列表
    online_users = r.sunion(keys_in_last_10_minutes())
    return b"<br>".join(online_users)


if __name__ == "__main__":
    app.run(debug=True)
