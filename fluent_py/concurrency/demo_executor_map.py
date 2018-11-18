import time
from concurrent import futures


def display(*args):
    print(time.strftime("[%H:%M:%S]"), end=" ")
    print(*args)


def loiter(n):
    msg = "{}lotier({}):doing nothing for {}s..."
    display(msg.format("\t" * n, n, n))
    time.sleep(n)
    msg = "{}lotier({}) done"
    display(msg.format("\t" * n, n))
    return n * 10

def main():
    display('Script starting')
    ex = futures.ThreadPoolExecutor(max_workers=3)
    results = ex.map(loiter, range(5))
    display('results:', results)
    display('Waiting for individual results:')
    for i, result in enumerate(results):
        display(f"result {i}: {result}")

if __name__ == "__main__":
    main()