import time
import sys
import string
import argparse
from collections import namedtuple
from enum import Enum
from pathlib import Path

Result = namedtuple("Result", "status data")
DownloadStatus = Enum("Status", "ok not_found error")
POP20_CC = ("CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR").split()
DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ = 1
SERVERS = {
    "REMOTE": "https://www.fluentpython.com/data/flags",
    "LOCAL": "http://localhost:8001/flags",
}
DEFAULT_SERVER = "REMOTE"
DEST_DIR = Path(__file__).parent / "downloaded"
COUNTRY_CODES_FILE = Path("country_codes.txt")


def save_flag(img, filename):
    with open(DEST_DIR / filename, "wb") as fp:
        # 修改为 fp.write(img*10)可以用来测试不同flags.py对于硬盘写入时的性能差异
        fp.write(img)


def initial_report(cc_list, actual_req, server_label):
    if len(cc_list) <= 10:
        cc_msg = ", ".join(cc_list)
    else:
        cc_msg = f"from {cc_list[0]} to {cc_list[-1]}"
    print(f"{server_label} site: {SERVERS[server_label]}")
    plural = "" if len(cc_list) == 1 else "s"
    print(f"Searching for {len(cc_list)} flag{plural} : {cc_msg}")
    plural = "" if actual_req == 1 else "s"
    print(f"{actual_req} concurrent connection{plural}")


def final_report(cc_list, counter, start_time):
    elapsed = time.time() - start_time
    print("-" * 20)
    plural = "" if counter[DownloadStatus.ok] == 1 else "s"
    print(f"{counter[DownloadStatus.ok]} flag{plural} downloaded")
    if counter[DownloadStatus.not_found]:
        print(counter[DownloadStatus.not_found], "not found")
    if counter[DownloadStatus.error]:
        print(counter[DownloadStatus.error], "error")
    print(f"Elapsed time: {elapsed:.2f}s")


def expand_cc_args(every_cc, all_cc, cc_args, limit):
    codes = set()
    if every_cc:
        codes.update(
            a + b for a in string.ascii_uppercase for b in string.ascii_uppercase
        )
    elif all_cc:
        with open(COUNTRY_CODES_FILE) as fp:
            text = fp.read()
        codes.update(text.split())
    else:
        for cc in (c.upper() for c in cc_args):
            if len(cc) == 1 and cc in string.ascii_uppercase:
                codes.update(cc + c for c in string.ascii_uppercase)
            elif len(cc) == 2 and all(c in string.ascii_uppercase for c in cc):
                codes.add(cc)
            else:
                raise ValueError(
                    "*** Usage Error: each cc argument must be A to Z or AA to ZZ"
                )
    return sorted(codes)[:limit]


def process_args(default_concur_req):
    server_options = ", ".join(sorted(SERVERS))
    parser = argparse.ArgumentParser(description="Download flags for countrycodes")
    parser.add_argument(
        "cc", metavar="CC", nargs="*", help="country code or 1st letter"
    )
    parser.add_argument(
        "-a", "--all", action="store_true", help="get all available flags (AD to ZW)"
    )
    parser.add_argument(
        "-e", "--every", action="store_true", help="get flags for code (AA to ZZ)"
    )
    parser.add_argument(
        "-l", "--limit", metavar="N", type=int, default=sys.maxsize, help="limit codes"
    )
    parser.add_argument(
        "-m",
        "--max_req",
        metavar="CONCURRENT",
        type=int,
        default=default_concur_req,
        help=f"maxium concurrent requests, default={default_concur_req}",
    )
    parser.add_argument(
        "-s",
        "--server",
        metavar="LABEL",
        default=DEFAULT_SERVER,
        help="server to select",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="output detail progress info"
    )
    args = parser.parse_args()
    if args.max_req < 1:
        print("*** Usage error")
        parser.print_usage()
        sys.exit(1)
    if args.limit < 1:
        print("*** Usage error")
        parser.print_usage()
        sys.exit(1)
    args.server = args.server.upper()
    if args.server not in SERVERS:
        print("*** Usage error")
        parser.print_usage()
        sys.exit(1)

    try:
        cc_list = expand_cc_args(args.every, args.all, args.cc, args.limit)
    except ValueError as exc:
        print(exc.args[0])
        parser.print_usage()
        sys.exit(1)

    if not cc_list:
        cc_list = sorted(POP20_CC)
    return args, cc_list


def main(download_many, default_concur_req, max_concur_req):
    args, cc_list = process_args(default_concur_req)
    actual_req = min(args.max_req, max_concur_req, len(cc_list))
    initial_report(cc_list, actual_req, args.server)
    base_url = SERVERS[args.server]
    t0 = time.time()
    counter = download_many(cc_list, base_url, args.verbose, actual_req)
    assert sum(counter.values()) == len(cc_list), "some downloads are unaccounted"
    final_report(cc_list, counter, t0)
