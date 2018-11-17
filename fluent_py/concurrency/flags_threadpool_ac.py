from concurrent import futures
from flags_threadpool import download_one, main


def download_many(cc_list):
    cc_list = cc_list[:5]
    with futures.ThreadPoolExecutor(max_workers=3) as ex:
        to_do = []
        for cc in sorted(cc_list):
            future = ex.submit(download_one, cc)
            to_do.append(future)
            print(f"Scheduled for {cc}:{future}")

        results = []
        for future in futures.as_completed(to_do):
            res = future.result()
            print(f"{future} result:{res}")
            results.append(res)

    return len(results)

if __name__ == "__main__":
    main(download_many)
