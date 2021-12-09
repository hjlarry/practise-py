# 与flags2_asyncio.py区别是每次下载国旗时发起多次请求
from collections import Counter
import asyncio
from http import HTTPStatus

import httpx
import tqdm

from flags2_common import main, DownloadStatus, Result, save_flag


DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000


class FetchError(Exception):
    def __init__(self, country_code):
        self.country_code = country_code


async def get_country(client: httpx.AsyncClient, base_url: str, cc: str) -> str:
    url = f"{base_url}/{cc}/metadata.json"
    resp = await client.get(url, timeout=3.1, follow_redirects=True)
    resp.raise_for_status()
    metadata = resp.json()
    return metadata["country"]


async def get_flag(client: httpx.AsyncClient, base_url: str, cc: str) -> bytes:
    url = f"{base_url}/{cc}/{cc}.gif".lower()
    resp = await client.get(url, timeout=6.1, follow_redirects=True)
    resp.raise_for_status()
    return resp.read()


async def download_one(
    client: httpx.AsyncClient,
    cc: str,
    base_url: str,
    semaphore: asyncio.Semaphore,
    verbose: bool,
):
    try:
        async with semaphore:
            image = await get_flag(client, base_url, cc)
        async with semaphore:
            country = await get_country(client, base_url, cc)
    except httpx.HTTPStatusError as exc:
        res = exc.response
        if res.status_code == HTTPStatus.NOT_FOUND:
            status = DownloadStatus.not_found
            msg = f"not found {res.url}"
        else:
            raise
    else:
        filename = country.replace(" ", "_")
        await asyncio.to_thread(save_flag, image, f"{filename}.gif")
        status = DownloadStatus.ok
        msg = "OK"

    if verbose and msg:
        print(cc, msg)
    return Result(status, cc)


async def supervisor(cc_list: list[str], base_url: str, verbose: bool, concur_req: int):
    counter: Counter[DownloadStatus] = Counter()
    semaphore = asyncio.Semaphore(concur_req)
    async with httpx.AsyncClient() as client:
        to_do = [
            download_one(client, cc, base_url, semaphore, verbose)
            for cc in sorted(cc_list)
        ]
        to_do_iter = asyncio.as_completed(to_do)
        if not verbose:
            to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))
        for coro in to_do_iter:
            try:
                res = await coro
            except FetchError as exc:
                country_code = exc.country_code
                try:
                    error_msg = exc.__cause__.message  # type:ignore
                except AttributeError:
                    error_msg = "Unknown Cause"
                if verbose and error_msg:
                    print(f"*** Error for {country_code}: {error_msg}")
                status = DownloadStatus.error
            else:
                status = res.status
            counter[status] += 1
    return counter


def download_many(cc_list: list[str], base_url: str, verbose: bool, concur_req: int):
    coro = supervisor(cc_list, base_url, verbose, concur_req)
    counts = asyncio.run(coro)
    return counts


if __name__ == "__main__":
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
