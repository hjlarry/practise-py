from urllib.request import urlopen
import warnings
import os
import json

URL = "http://www.oreilly.com/pub/sc/osconfeed"
JSON = "osconfeed.json"


def load():
    if not os.path.exists(JSON):
        msg = f"downloading {JSON} from {URL}"
        warnings.warn(msg)
        with urlopen(URL) as remote, open(JSON, "wb") as local:
            local.write(remote.read())

    with open(JSON) as fp:
        return json.load(fp)

if __name__ == "__main__":
    feed = load()
    print(sorted(feed['Schedule'].keys()))
    for key, value in feed['Schedule'].items():
        print(f"{key} : {len(value)}")
    print(feed['Schedule']['events'][40]['name'])
    print(feed['Schedule']['speakers'][40]['name'])