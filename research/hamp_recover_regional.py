"""Recover the indexed regional payloads listed in a research manifest."""

import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from datetime import datetime
import gzip
import hashlib
import json
from pathlib import Path
import tempfile
from urllib.request import Request, urlopen

from hamp_2016_snapshot import archived_headers


@contextmanager
def payload(item):
    if "warc_url" not in item:
        with urlopen(item["replay_url"], timeout=45) as response:
            yield response
        return

    start = item["warc_offset"]
    end = start + item["warc_record_bytes"] - 1
    request = Request(item["warc_url"], headers={"Range": f"bytes={start}-{end}"})
    with urlopen(request, timeout=45) as response:
        if response.status != 206 or not response.headers.get("Content-Range", "").startswith(
            f"bytes {start}-{end}/"
        ):
            raise ValueError("Unexpected byte range for the archived response.")
        with gzip.GzipFile(fileobj=response) as source:
            if not source.readline().startswith(b"WARC/"):
                raise ValueError("Expected a compressed WARC record.")
            headers = archived_headers(source)
            capture = datetime.strptime(item["capture_utc"], "%Y%m%d%H%M%S")
            capture_header = capture.strftime("%Y-%m-%dT%H:%M:%SZ").encode()
            if headers.get(b"warc-target-uri") != item["url"].encode() or headers.get(b"warc-date") != capture_header:
                raise ValueError("The WARC response URL or capture date does not match the manifest.")
            status = source.readline().split()
            response_headers = archived_headers(source)
            if status[1:2] != [b"200"] or int(response_headers.get(b"content-length", b"0")) != item["bytes"]:
                raise ValueError("Unexpected status or payload length in the archived response.")
            yield source
            if source.read(16) != b"\r\n\r\n":
                raise ValueError("Expected exactly one complete WARC response.")


def recover(item, directory):
    name = item["file"]
    if Path(name).name != name or Path(name).suffix.lower() not in {".csv", ".zip"}:
        raise ValueError("Expected a CSV or ZIP file name.")
    size = item["bytes"]
    if not isinstance(size, int) or size <= 0:
        raise ValueError("Expected a positive integer payload length.")
    target = directory / name
    with tempfile.TemporaryDirectory(dir=directory) as scratch:
        staged = Path(scratch) / name
        sha1, sha256 = hashlib.sha1(), hashlib.sha256()
        remaining = size
        with payload(item) as source, staged.open("xb") as destination:
            while remaining:
                block = source.read(min(remaining, 4 * 1024 * 1024))
                if not block:
                    raise ValueError(f"Truncated archive payload for {name}.")
                sha1.update(block)
                sha256.update(block)
                destination.write(block)
                remaining -= len(block)
            if "warc_url" not in item and source.read(1):
                raise ValueError(f"Unexpected extra payload bytes for {name}.")
        if (
            base64.b32encode(sha1.digest()).decode() != item["payload_sha1_base32"]
            or sha256.hexdigest() != item["sha256"]
        ):
            raise ValueError(f"Archive digest mismatch for {name}.")
        staged.replace(target)
    return name


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--source-dir", required=True, type=Path)
    args = parser.parse_args()
    entries = json.loads(args.manifest.read_text(encoding="utf-8"))
    if not entries or len({item["file"] for item in entries}) != len(entries):
        raise ValueError("A nonempty manifest with unique file names is required.")
    args.source_dir.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        for name in pool.map(lambda item: recover(item, args.source_dir), entries):
            print(f"Verified {name}")


if __name__ == "__main__":
    main()
