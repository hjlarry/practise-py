from concurrent import futures
from flags_threadpool import download_one, main


def download_many(cc_list: list[str]) -> int:
    cc_list = cc_list[:5]
    with futures.ThreadPoolExecutor(max_workers=3) as ex:
        to_do: list[futures.Future] = []
        for cc in sorted(cc_list):
            future = ex.submit(download_one, cc)
            to_do.append(future)
            print(f"Scheduled for {cc}:{future}")

        for count, future in enumerate(futures.as_completed(to_do), 1):
            res: str = future.result()
            print(f"{future} result:{res!r}")

    return count


if __name__ == "__main__":
    main(download_many)
