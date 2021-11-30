import sys
from time import perf_counter
from typing import NamedTuple
from multiprocessing import Process, SimpleQueue, cpu_count
from multiprocessing import queues

from primes import is_prime, NUMBERS


class PrimeResult(NamedTuple):
    n: int
    prime: bool
    elapsed: float


JobQueue = queues.SimpleQueue[int]
ResultQueue = queues.SimpleQueue[PrimeResult]


def check(n: int) -> PrimeResult:
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n, res, perf_counter() - t0)


def worker(jobs: JobQueue, results: ResultQueue):
    while n := jobs.get():
        results.put(check(n))


def main() -> None:
    if len(sys.argv) < 2:
        workers = cpu_count()
    else:
        workers = int(sys.argv[1])
    print(f"Checking {len(NUMBERS)} numbers sequential:")
    jobs: JobQueue = SimpleQueue()
    results: ResultQueue = SimpleQueue()
    t0 = perf_counter()
    for n in NUMBERS:
        jobs.put(n)
    for _ in range(workers):
        proc = Process(target=worker, args=(jobs, results))
        proc.start()
        jobs.put(0)
    while True:
        n, prime, elapsed = results.get()
        label = "P" if prime else " "
        print(f"{n:16} {label} {elapsed:9.6f}s")
        if jobs.empty():
            break
    elapsed = perf_counter() - t0
    print(f"Total time: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
