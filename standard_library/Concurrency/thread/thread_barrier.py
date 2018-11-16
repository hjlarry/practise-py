# 屏障（Barrier）是另一种线程同步的机制。每个 Barrier 会建立起一个控制点，所有处在其中的线程都会被阻塞，直到所有的线程都到达这个控制点。它会让所有的线程单独启动，然后在它们全都准备好执行下一步前先阻塞住。
import time
import threading
import logging


def worker(barrier):
    print(
        threading.current_thread().name,
        f"wait for barrier with {barrier.n_waiting} others",
    )
    worker_id = barrier.wait()
    print(f"{threading.current_thread().name} after barrier  {worker_id}")


NUM_T = 3
barrier = threading.Barrier(NUM_T)
threads = [
    threading.Thread(name=f"worker-{i}", target=worker, args=(barrier,))
    for i in range(NUM_T)
]
for t in threads:
    print(t.name, "starting")
    t.start()
    time.sleep(0.1)

for t in threads:
    t.join()

# Barrier 的 abort() 方法会导致所有等待中的线程接收到一个 BrokenBarrierError。 我们可以使用此方法来告知那些被阻塞住的线程该结束了。这次我们将 Barrier 设置成比实际开始的线程多一个，这样所有的线程就会被阻塞住，我们调用 abort() 就可以引起 BrokenBarrierError 了。
def worker2(barrier):
    print(
        threading.current_thread().name,
        f"wait for barrier with {barrier.n_waiting} others",
    )
    try:
        worker_id = barrier.wait()
    except threading.BrokenBarrierError:
        print(f"{threading.current_thread().name} aborting")
    else:
        print(f"{threading.current_thread().name} after barrier  {worker_id}")


NUM_T = 3
barrier = threading.Barrier(NUM_T + 1)
threads = [
    threading.Thread(name=f"worker-{i}", target=worker2, args=(barrier,))
    for i in range(NUM_T)
]
for t in threads:
    print(t.name, "starting")
    t.start()
    time.sleep(0.1)
barrier.abort()
for t in threads:
    t.join()

