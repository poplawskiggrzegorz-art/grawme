#!/usr/bin/env python3
"""Create small WebP previews for the site's gallery and category cards."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "images" / "webp"
OUTPUT_DIR = ROOT / "images" / "thumbs"
MAX_SIZE = (720, 720)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for source in sorted(SOURCE_DIR.glob("*.webp")):
        with Image.open(source) as image:
            image.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
            image.save(OUTPUT_DIR / source.name, "WEBP", quality=76, method=6)


if __name__ == "__main__":
    main()
