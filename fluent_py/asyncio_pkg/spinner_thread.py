import itertools
import time
from threading import Thread, Event
from primes import is_prime


def spin(msg: str, done: Event) -> None:
    for char in itertools.cycle("|/-\\"):
        status = f"\r{char} {msg}"
        print(status, end="", flush=True)
        if done.wait(0.1):
            break
    blanks = " " * len(status)
    print(f"\r{blanks}\r", end="")


def slow_function() -> int:
    # 假装io等待,模拟IO密集型场景
    # time.sleep(3)
    # 计算型任务，模拟CPU密集场景
    # 也许我们会想当然的认为由于GIL的存在，导致CPU密集场景，子线程spin不会被运行
    # 但实际上spin会运行，因为GIL的机制是每5ms释放一下，让其他线程也有机会运行
    # 而在async版本中，spin不会运行，解决的办法就是is_prime_nap版本
    is_prime(5_000_111_000_222_021)
    return 42


def supervisor():
    done = Event()
    spinner = Thread(target=spin, args=("thinking", done))
    print(f"spinner obj: {spinner}")
    spinner.start()
    result = slow_function()
    done.set()
    spinner.join()
    return result


def main():
    result = supervisor()
    print(f"Answer: {result}")


if __name__ == "__main__":
    main()
