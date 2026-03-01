#!/usr/bin/env python3
"""
download_sanity_data.py

Downloads a small sanity dataset for pipeline testing.

Default behavior:
- real images from Picsum (quick placeholder real-photo source)
- generated images from ThisPersonDoesNotExist (quick placeholder generated source)

You can also pass a CSV manifest with columns:
  url,label,source,generator,prompt
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import ssl
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download a sanity dataset.")
    parser.add_argument("--base-dir", default="data", help="Base data directory.")
    parser.add_argument(
        "--real-count",
        type=int,
        default=25,
        help="Number of placeholder real images to fetch.",
    )
    parser.add_argument(
        "--generated-count",
        type=int,
        default=25,
        help="Number of placeholder generated images to fetch.",
    )
    parser.add_argument(
        "--manifest-csv",
        default="",
        help="Optional CSV manifest path with explicit URL rows.",
    )
    parser.add_argument(
        "--timeout-seconds", type=int, default=20, help="HTTP timeout per request."
    )
    parser.add_argument(
        "--sleep-ms",
        type=int,
        default=200,
        help="Sleep between requests to reduce throttling.",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable SSL cert verification (only use in restricted local environments).",
    )
    return parser.parse_args()


def download_bytes(url: str, timeout_seconds: int, insecure: bool) -> bytes:
    request = Request(
        url,
        headers={
            "User-Agent": "ai-shield-data-bootstrap/1.0",
            "Accept": "image/*,*/*;q=0.8",
        },
    )
    context = ssl._create_unverified_context() if insecure else None
    with urlopen(request, timeout=timeout_seconds, context=context) as response:
        return response.read()


def write_image(content: bytes, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(content)


def safe_suffix_from_url(url: str) -> str:
    path = urlparse(url).path.lower()
    if path.endswith(".png"):
        return ".png"
    if path.endswith(".webp"):
        return ".webp"
    return ".jpg"


def download_placeholder_real(
    base_dir: Path, count: int, timeout_seconds: int, sleep_ms: int, insecure: bool
) -> int:
    success = 0
    target = base_dir / "raw" / "real" / "picsum"
    for idx in range(count):
        url = f"https://picsum.photos/seed/ai-shield-real-{idx}/512/512"
        try:
            content = download_bytes(url, timeout_seconds, insecure)
            file_name = f"real_picsum_{idx:04d}.jpg"
            write_image(content, target / file_name)
            success += 1
        except (HTTPError, URLError, TimeoutError) as exc:
            print(f"[real] failed {url} -> {exc}")
        time.sleep(max(0, sleep_ms) / 1000.0)
    return success


def download_placeholder_generated(
    base_dir: Path, count: int, timeout_seconds: int, sleep_ms: int, insecure: bool
) -> int:
    success = 0
    target = base_dir / "raw" / "generated" / "tpdne"
    url = "https://thispersondoesnotexist.com/"
    for idx in range(count):
        try:
            content = download_bytes(url, timeout_seconds, insecure)
            file_name = f"generated_tpdne_{idx:04d}.jpg"
            write_image(content, target / file_name)
            success += 1
        except (HTTPError, URLError, TimeoutError) as exc:
            print(f"[generated] failed {url} -> {exc}")
        time.sleep(max(0, sleep_ms) / 1000.0)
    return success


def download_from_manifest(
    base_dir: Path, manifest_csv: Path, timeout_seconds: int, sleep_ms: int, insecure: bool
) -> int:
    if not manifest_csv.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_csv}")

    success = 0
    with manifest_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for idx, row in enumerate(reader):
            url = (row.get("url") or "").strip()
            label = (row.get("label") or "").strip().lower()
            source = (row.get("source") or "").strip() or "unknown_source"
            generator = (row.get("generator") or "").strip() or "unknown_generator"
            if not url or label not in {"real", "generated"}:
                print(f"[manifest] skipping row {idx}: invalid url/label")
                continue

            try:
                content = download_bytes(url, timeout_seconds, insecure)
                content_hash = hashlib.sha256(content).hexdigest()[:12]
                suffix = safe_suffix_from_url(url)

                if label == "real":
                    dst = base_dir / "raw" / "real" / source / f"real_{content_hash}{suffix}"
                else:
                    dst = (
                        base_dir
                        / "raw"
                        / "generated"
                        / generator
                        / source
                        / f"generated_{content_hash}{suffix}"
                    )
                write_image(content, dst)
                success += 1
            except (HTTPError, URLError, TimeoutError) as exc:
                print(f"[manifest] failed {url} -> {exc}")
            time.sleep(max(0, sleep_ms) / 1000.0)
    return success


def main() -> None:
    args = parse_args()
    base_dir = Path(args.base_dir)
    base_dir.mkdir(parents=True, exist_ok=True)

    downloaded = 0
    if args.real_count > 0:
        downloaded += download_placeholder_real(
            base_dir, args.real_count, args.timeout_seconds, args.sleep_ms, args.insecure
        )
    if args.generated_count > 0:
        downloaded += download_placeholder_generated(
            base_dir, args.generated_count, args.timeout_seconds, args.sleep_ms, args.insecure
        )

    if args.manifest_csv:
        downloaded += download_from_manifest(
            base_dir,
            Path(args.manifest_csv),
            args.timeout_seconds,
            args.sleep_ms,
            args.insecure,
        )

    print(f"Downloaded {downloaded} files into {base_dir / 'raw'}.")


if __name__ == "__main__":
    main()
