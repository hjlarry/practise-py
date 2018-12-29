import time


class Stats:
    def __init__(self):
        self.stats = {}

    def add(self, key, count=1):
        self.stats[key] = self.stats.get(key, 0) + count

    def report(self, file=None):
        for key, count in sorted(self.stats.items()):
            print(f"{count} {key}", file=file)


def report(crawler, file=None):
    t1 = crawler.t1 or time.time()
    dt = t1 - crawler.t0
    if dt and crawler.max_tasks:
        speed = len(crawler.done) / dt / crawler.max_tasks
    else:
        speed = 0
    stats = Stats()
    print("*** Report ***", file=file)
    try:
        show = list(crawler.done)
        for stat in show:
            url_report(stat, stats, file=file)
    except KeyboardInterrupt:
        print("\nInterrupted\n", file=file)
    print(
        f"Finished {len(crawler.done)} urls in {dt:.3f} secs, (max_tasks={crawler.max_tasks}) (speed={speed})",
        file=file,
    )
    stats.report(file=file)
    print("Todo:", crawler.q.qsize(), file=file)
    print("Done:", len(crawler.done), file=file)
    print("Date:", time.ctime(), "local time", file=file)


def url_report(stat, stats, file=None):
    if stat.exception:
        stats.add("fail")
        stats.add("fail_" + str(stat.exception.__class__.__name__))
        print(stat.url, "error", stat.exception, file=file)
    elif stat.next_url:
        stats.add("redirect")
        print(stat.url, stat.status, "redirect", stat.next_url, file=file)
    elif stat.content_type == "text/html":
        stats.add("html")
        stats.add("html_bytes", stat.size)
        print(
            stat.url,
            stat.status,
            stat.content_type,
            stat.encoding,
            stat.size,
            f"{stat.num_new_urls}/{stat.num_urls}",
            file=file,
        )
    else:
        if stat.status == 200:
            stats.add("other")
            stats.add("other_bytes", stat.size)
        else:
            stats.add("error")
            stats.add("error_bytes", stat.size)
            stats.add(f"status_{stat.status}")
        print(
            stat.url,
            stat.status,
            stat.content_type,
            stat.encoding,
            stat.size,
            file=file,
        )
