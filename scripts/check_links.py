"""Verify every recommendation in api/data.py still has a reachable URL.

Some sites (e.g. sverigesradio.se) return 403 to any non-browser client
(Akamai bot protection) even though the page works fine in a real browser --
those are treated as unverifiable rather than failures. Everything else
must return a successful or redirect status.
"""
import sys
import urllib.error
import urllib.request
from pathlib import Path

if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "api"))
from data import CHANNELS, PODCASTS  # noqa: E402

BOT_PROTECTED_DOMAINS = ("sverigesradio.se",)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
}


def check(url: str) -> str | None:
    request = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            if 200 <= response.status < 400:
                return None
            return f"unexpected status {response.status}"
    except urllib.error.HTTPError as exc:
        if exc.code == 403 and any(domain in url for domain in BOT_PROTECTED_DOMAINS):
            return None
        return f"HTTP {exc.code}"
    except urllib.error.URLError as exc:
        return str(exc.reason)


def main() -> int:
    failures = []
    for item in CHANNELS + PODCASTS:
        url = item.get("url")
        if not url:
            print(f"SKIP (no link on file): {item['name']}")
            continue
        error = check(url)
        if error:
            failures.append(f"{item['name']}: {error} ({url})")
        else:
            print(f"OK: {item['name']} -> {url}")

    if failures:
        print("\nBroken links found:")
        for failure in failures:
            print(f" - {failure}")
        return 1

    print("\nAll links OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
