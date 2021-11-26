import asyncio
import itertools
from primes import is_prime, is_prime_nap


async def spin(msg: str) -> None:
    for char in itertools.cycle("|/-\\"):
        status = f"\r{char} {msg}"
        print(status, end="", flush=True)
        try:
            await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            break
    blanks = " " * len(status)
    print(f"\r{blanks}\r", end="")


async def slow_function() -> int:
    # await asyncio.sleep(3)
    # is_prime(5_000_111_000_222_021)
    await is_prime_nap(5_000_111_000_222_021)
    return 42


async def supervisor() -> int:
    spinner = asyncio.create_task(spin("thinking"))
    print(f"spinner obj: {spinner}")
    result = await slow_function()
    spinner.cancel()
    return result


def main() -> None:
    result = asyncio.run(supervisor())
    print(f"Answer: {result}")


if __name__ == "__main__":
    main()
