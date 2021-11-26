import asyncio
import itertools


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
    # 假装io等待
    await asyncio.sleep(3)
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
