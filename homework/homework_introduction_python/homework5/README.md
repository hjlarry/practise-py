1\. 写一个异步生成器

要求：
- 用到 async for
- 抓取10个 http://httpbin.org/get?a=X 这样的url (X为0-9这十个数字)，并打印a的值
2\. 写一个异步列表解析式

要求：把第一个题目中获得的a的值，最后用异步列表解析式搜集起来：
```
❯ python 2.py
['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
```

3\. 使用TASK 的写法
- 抓取10个 http://httpbin.org/get?a=X 这样的url (X为0-9这十个数字)
- 使用ensure_future+gather
- 最后用异步列表解析式搜集起来
```
❯ python 3.py
['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
```

4\. 写一个生产者/消费者例子

要求:

- 地址格式 http://httpbin.org/get?a=X X为不同的数字
- 消费时，如果请求超时(1秒)，把未完成的任务放回队列
- 一开始先生产5个任务，任务开始的1秒后再放入剩下的5个任务
- 程序可以自动结束

```
❯ python 4.py
producing 4
producing 24
producing 71
producing 21
producing 27
consuming 4...
consuming 24...
producing 82
producing 18
producing 99
producing 28
producing 74
Put back: 24
consuming 71...
consuming 21...
consuming 27...
Put back: 27
consuming 82...
consuming 18...
consuming 99...
Put back: 99
consuming 28...
consuming 74...
consuming 24...
consuming 27...
consuming 99...
['4', '71', '21', '82', '18', '28', '74', '24', '27', '99']
```

### 参考答案
https://talk.pycourses.com/topic/42/python%E5%85%A5%E9%97%A8-%E4%BD%9C%E4%B8%9A-%E4%BA%94-%E7%AD%94%E6%A1%88