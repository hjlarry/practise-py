import collections
import asyncio

import aiohttp
import tqdm

from flags2_common import main, HTTPStatus, Result, save_flag


DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000


class FetchError(Exception):
    def __init__(self, country_code):
        self.country_code = country_code


async def get_flag(base_url, cc):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{base_url}/{cc.lower()}/{cc.lower()}.gif") as resp:
            if resp.status == 200:
                image = await resp.read()
                return image
            elif resp.status == 404:
                raise aiohttp.web.HTTPNotFound()
            else:
                raise aiohttp.http.HttpProcessingError(
                    code=resp.code, message=resp.reason, headers=resp.headers
                )


async def download_one(cc, base_url, semaphore, verbose=False):
    try:
        with (await semaphore):
            image = await get_flag(base_url, cc)
    except aiohttp.web.HTTPNotFound:
        status = HTTPStatus.not_found
        msg = "not found"
    except Exception as exc:
        raise FetchError(cc) from exc
    else:
        # 与 flags2_asyncio 只有这里不同
        loop = asyncio.get_event_loop()
        # None则使用事件循环默认的 ThreadPoolExecutor实例
        loop.run_in_executor(None, save_flag, image, cc.lower() + ".gif")
        status = HTTPStatus.ok
        msg = "OK"

    if verbose and msg:
        print(cc, msg)
    return Result(status, cc)


async def downloader_coro(cc_list, base_url, verbose, concur_req):
    counter = collections.Counter()
    semaphore = asyncio.Semaphore(concur_req)
    to_do = [download_one(cc, base_url, semaphore, verbose) for cc in sorted(cc_list)]
    to_do_iter = asyncio.as_completed(to_do)
    if not verbose:
        to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))
    for future in to_do_iter:
        try:
            res = await future
        except FetchError as exc:
            country_code = exc.country_code
            try:
                error_msg = exc.__cause__.args[0]
            except IndexError:
                error_msg = exc.__cause__.__class__.__name__
            if verbose and error_msg:
                print(f"*** Error for {country_code}: {error_msg}")
            status = HTTPStatus.error
        else:
            status = res.status
        counter[status] += 1
    return counter


def download_many(cc_list, base_url, verbose, concur_req):
    loop = asyncio.get_event_loop()
    coro = downloader_coro(cc_list, base_url, verbose, concur_req)
    counts = loop.run_until_complete(coro)
    loop.close()
    return counts


if __name__ == "__main__":
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
