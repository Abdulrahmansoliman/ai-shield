#!/usr/bin/env python3
"""
prepare_dataset.py

Script to download/organize real and generated images, deduplicate, and split into train/val/test/unseen.
"""

from pathlib import Path


def download_datasets():
    """Placeholder: implement downloads from COCO, OpenImages, GenImage, etc."""
    pass


def deduplicate_and_split(base_dir: Path):
    """Placeholder: dedupe and create splits with metadata."""
    pass


def main():
    base_dir = Path("data")
    download_datasets()
    deduplicate_and_split(base_dir)


if __name__ == "__main__":
    main()
