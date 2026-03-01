#!/usr/bin/env python3
"""
prepare_dataset.py

Builds metadata from locally downloaded data, deduplicates by content hash,
and creates train/val/test/unseen_generator splits.

Expected raw layout:
  data/raw/real/<source_name>/**/*.jpg
  data/raw/generated/<generator_name>/**/*.jpg
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import shutil
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}


@dataclass
class SampleRecord:
    id: str
    path: str
    type: str
    source: str
    generator: str | None
    prompt: str | None
    compression: int | None
    transforms: list[str] = field(default_factory=list)
    split: str = ""
    label: str = ""
    sha256: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare AI Shield dataset splits.")
    parser.add_argument("--base-dir", default="data", help="Base data directory.")
    parser.add_argument(
        "--train-ratio", type=float, default=0.8, help="Train split ratio."
    )
    parser.add_argument(
        "--val-ratio", type=float, default=0.1, help="Validation split ratio."
    )
    parser.add_argument("--test-ratio", type=float, default=0.1, help="Test split ratio.")
    parser.add_argument(
        "--unseen-generators",
        default="",
        help="Comma-separated generator names to reserve for unseen_generator split.",
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Random seed for deterministic splits."
    )
    parser.add_argument(
        "--materialize",
        action="store_true",
        help="Copy split files into data/processed/splits/<split>/<label>/.",
    )
    return parser.parse_args()


def iter_image_files(root: Path) -> Iterable[Path]:
    if not root.exists():
        return
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            yield path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_raw_records(base_dir: Path) -> list[SampleRecord]:
    records: list[SampleRecord] = []
    raw_real = base_dir / "raw" / "real"
    raw_generated = base_dir / "raw" / "generated"

    for file_path in iter_image_files(raw_real):
        relative = file_path.relative_to(raw_real)
        source = relative.parts[0] if len(relative.parts) > 1 else "unknown_real_source"
        file_hash = sha256_file(file_path)
        records.append(
            SampleRecord(
                id=file_hash[:16],
                path=str(file_path),
                type="image",
                source=source,
                generator=None,
                prompt=None,
                compression=None,
                label="real",
                sha256=file_hash,
            )
        )

    for file_path in iter_image_files(raw_generated):
        relative = file_path.relative_to(raw_generated)
        generator = relative.parts[0] if len(relative.parts) > 1 else "unknown_generator"
        source = relative.parts[1] if len(relative.parts) > 2 else "generated_source"
        file_hash = sha256_file(file_path)
        records.append(
            SampleRecord(
                id=file_hash[:16],
                path=str(file_path),
                type="image",
                source=source,
                generator=generator,
                prompt=None,
                compression=None,
                label="generated",
                sha256=file_hash,
            )
        )

    return records


def deduplicate(records: list[SampleRecord]) -> list[SampleRecord]:
    unique: dict[str, SampleRecord] = {}
    for record in records:
        if record.sha256 not in unique:
            unique[record.sha256] = record
    return list(unique.values())


def split_bucket(
    records: list[SampleRecord], train_ratio: float, val_ratio: float, seed: int
) -> tuple[list[SampleRecord], list[SampleRecord], list[SampleRecord]]:
    if not records:
        return [], [], []
    rng = random.Random(seed)
    shuffled = records[:]
    rng.shuffle(shuffled)
    n = len(shuffled)
    n_train = int(n * train_ratio)
    n_val = int(n * val_ratio)
    train = shuffled[:n_train]
    val = shuffled[n_train : n_train + n_val]
    test = shuffled[n_train + n_val :]
    return train, val, test


def assign_splits(
    records: list[SampleRecord],
    train_ratio: float,
    val_ratio: float,
    test_ratio: float,
    unseen_generators: set[str],
    seed: int,
) -> list[SampleRecord]:
    if abs((train_ratio + val_ratio + test_ratio) - 1.0) > 1e-9:
        raise ValueError("train/val/test ratios must sum to 1.0")

    real_records = [r for r in records if r.label == "real"]
    seen_generated = [
        r
        for r in records
        if r.label == "generated" and (r.generator or "") not in unseen_generators
    ]
    unseen_generated = [
        r
        for r in records
        if r.label == "generated" and (r.generator or "") in unseen_generators
    ]

    real_train, real_val, real_test = split_bucket(real_records, train_ratio, val_ratio, seed)
    gen_train, gen_val, gen_test = split_bucket(
        seen_generated, train_ratio, val_ratio, seed + 1
    )

    for record in real_train + gen_train:
        record.split = "train"
    for record in real_val + gen_val:
        record.split = "val"
    for record in real_test + gen_test:
        record.split = "test"
    for record in unseen_generated:
        record.split = "unseen_generator"

    return real_train + real_val + real_test + gen_train + gen_val + gen_test + unseen_generated


def write_outputs(base_dir: Path, records: list[SampleRecord], materialize: bool) -> None:
    processed_dir = base_dir / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    metadata_jsonl = processed_dir / "metadata.jsonl"
    metadata_csv = processed_dir / "metadata.csv"

    with metadata_jsonl.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")

    fieldnames = [
        "id",
        "path",
        "type",
        "source",
        "generator",
        "prompt",
        "compression",
        "transforms",
        "split",
        "label",
        "sha256",
    ]
    with metadata_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            row = asdict(record)
            row["transforms"] = ";".join(record.transforms)
            writer.writerow(row)

    splits_dir = processed_dir / "splits"
    splits_dir.mkdir(parents=True, exist_ok=True)
    for split_name in ["train", "val", "test", "unseen_generator"]:
        split_path = splits_dir / f"{split_name}.csv"
        with split_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for record in records:
                if record.split != split_name:
                    continue
                row = asdict(record)
                row["transforms"] = ";".join(record.transforms)
                writer.writerow(row)

    if materialize:
        materialized_root = processed_dir / "materialized"
        for record in records:
            src = Path(record.path)
            dst = materialized_root / record.split / record.label / f"{record.id}{src.suffix.lower()}"
            dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists():
                shutil.copy2(src, dst)


def print_summary(records: list[SampleRecord]) -> None:
    by_split_label: dict[tuple[str, str], int] = {}
    for record in records:
        key = (record.split, record.label)
        by_split_label[key] = by_split_label.get(key, 0) + 1

    print("Prepared dataset summary:")
    for split_name in ["train", "val", "test", "unseen_generator"]:
        real_count = by_split_label.get((split_name, "real"), 0)
        generated_count = by_split_label.get((split_name, "generated"), 0)
        print(f"  {split_name:16} real={real_count:5d} generated={generated_count:5d}")


def main() -> None:
    args = parse_args()
    base_dir = Path(args.base_dir)

    records = collect_raw_records(base_dir)
    if not records:
        print(
            "No image files found under data/raw/real or data/raw/generated. "
            "Download/place files first, then rerun."
        )
        return

    deduped_records = deduplicate(records)
    unseen_generators = {
        item.strip() for item in args.unseen_generators.split(",") if item.strip()
    }
    split_records = assign_splits(
        deduped_records,
        train_ratio=args.train_ratio,
        val_ratio=args.val_ratio,
        test_ratio=args.test_ratio,
        unseen_generators=unseen_generators,
        seed=args.seed,
    )

    write_outputs(base_dir, split_records, materialize=args.materialize)
    print_summary(split_records)


if __name__ == "__main__":
    main()
