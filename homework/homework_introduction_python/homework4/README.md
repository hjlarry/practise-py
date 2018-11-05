1\. 使用多线程请求一定数量HTTPBIN网站页面并存储结果

要求:
- 地址格式 http://httpbin.org/get?a=X X为不同的数字
- 线程数为5
- 控制并发数量为3，使用线程池或者信号量都可以
- 使用队列1提交全部任务10个
- 使用队列2存储不同线程执行的结果
- 为了让结果随机，可以随机sleep一点点时间

```
❯ python 1.py  # 你执行的结果可能不一样
Thread1 ['1', '5', '8']
Thread0 ['0', '4', '7']
Thread2 ['2', '3', '6', '9']
```

提示：用Session提高性能

2\. 使用多进程实现生产者/消费者模型，而且可以通过生产者控制消费者是否接收新的任务

启动2个消费者
前5个任务由其中一个消费者接收执行，剩下的由另外的消费者单独接收执行。
```
❯ python 2.py
Produce: 76
Consumer0: 76
Produce: 12
Consumer0: 12
Produce: 92
Consumer0: 92
Produce: 53
Consumer0: 53
Consumer0: 96
Produce: 96
Produce: 84
Consumer1: 84
Produce: 18
Consumer1: 18
Produce: 72
Consumer1: 72
Consumer1: 93
Produce: 93
Consumer1: 19
Produce: 19
```

提示：使用Event

3\. 使用标准库内置模块写一个最简单的MAPREDUCE例子
分析一下金庸小说中，金庸最喜欢用的短句是那些？

要求：

金庸小说可以网上去找
使用停用词， https://github.com/chdd/weibo/blob/master/stopwords/中文停用词库.txt
```
❯ python 3.py
ForkPoolWorker-1 reading novels/3.txt
ForkPoolWorker-3 reading novels/2.txt
ForkPoolWorker-2 reading novels/1.txt


金庸最爱说：😉

过了一会  : count:72
拍的一声  : count:69
站起身来  : count:59
砰的一声  : count:52
韦小宝大喜 : count:50
心中大喜  : count:46
否则的话  : count:44
是了    : count:41
过不多时  : count:40
突然之间  : count:38
```

提示：codecs.open处理文件编码、multiprocessing.Pool的map方法、之前的延伸阅读链接

4\. 使用多进程模块写一个使用优先级队列的例子
```
❯ python 4.py
put :7
put :36
put :91
put :10
put :73
put :23
[PRI:7] 7 * 2 = 14
[PRI:10] 10 * 2 = 20
[PRI:23] 23 * 2 = 46
[PRI:36] 36 * 2 = 72
[PRI:73] 73 * 2 = 146
[PRI:91] 91 * 2 = 182
```
提示：用BaseManager共享queue.PriorityQueue

5\. 使用THREADPOOLEXECUTOR和多线程搭配

要求：
- 用一个线程监视当然已完成的进度
- 用ThreadPoolExecutor创建3个线程执行fib函数
- 用另外一个线程作为生产者
```
❯ python 5.py
fib(26) = 121393
fib(28) = 317811
fib(27) = 196418
fib(29) = 514229
fib(31) = 1346269
fib(30) = 832040
```

提示：使用submit方法提交新的任务

### 参考答案
https://talk.pycourses.com/topic/39/python%E5%85%A5%E9%97%A8-%E4%BD%9C%E4%B8%9A-%E5%9B%9B-%E7%AD%94%E6%A1%88