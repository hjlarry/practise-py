import itertools
import time
from multiprocessing import Process, Event, synchronize


def spin(msg: str, done: synchronize.Event) -> None:
    for char in itertools.cycle("|/-\\"):
        status = f"\r{char} {msg}"
        print(status, end="", flush=True)
        if done.wait(0.1):
            break
    blanks = " " * len(status)
    print(f"\r{blanks}\r", end="")


def slow_function() -> int:
    # 假装io等待
    time.sleep(3)
    return 42


def supervisor():
    done = Event()
    spinner = Process(target=spin, args=("thinking", done))
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
