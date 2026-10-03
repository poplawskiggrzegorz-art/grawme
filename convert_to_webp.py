#!/usr/bin/env python3
"""Convert the website's source photos to optimized WebP copies."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from PIL import Image, ImageFile, ImageOps


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".heic", ".heif"}


def parse_args() -> argparse.Namespace:
    project_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Konwertuje zdjęcia JPG, PNG i opcjonalnie HEIC do WebP."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=project_dir / "images",
        help="Folder ze zdjęciami źródłowymi (domyślnie: images).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project_dir / "images" / "webp",
        help="Folder na pliki WebP (domyślnie: images/webp).",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=82,
        help="Jakość WebP od 1 do 100 (domyślnie: 82).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Zastąp już istniejące pliki WebP.",
    )
    return parser.parse_args()


def save_as_webp(source: Path, destination: Path, quality: int, *, allow_truncated: bool = False) -> None:
    previous_truncated_setting = ImageFile.LOAD_TRUNCATED_IMAGES
    ImageFile.LOAD_TRUNCATED_IMAGES = allow_truncated
    try:
        with Image.open(source) as original:
            image = ImageOps.exif_transpose(original)
            has_alpha = "A" in image.getbands() or "transparency" in image.info
            image = image.convert("RGBA" if has_alpha else "RGB")
            save_options = {"format": "WEBP", "quality": quality, "method": 6}
            icc_profile = original.info.get("icc_profile")
            if icc_profile:
                save_options["icc_profile"] = icc_profile
            image.save(destination, **save_options)
    finally:
        ImageFile.LOAD_TRUNCATED_IMAGES = previous_truncated_setting


def main() -> int:
    args = parse_args()
    if not 1 <= args.quality <= 100:
        raise SystemExit("Parametr --quality musi mieścić się w zakresie 1–100.")
    if not args.input.is_dir():
        raise SystemExit(f"Nie znaleziono folderu wejściowego: {args.input}")

    heic_enabled = False
    try:
        from pillow_heif import register_heif_opener

        register_heif_opener()
        heic_enabled = True
    except ImportError:
        pass

    candidates = sorted(
        (
            path
            for path in args.input.iterdir()
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
        ),
        key=lambda path: path.name.casefold(),
    )
    duplicate_stems = Counter(path.stem.casefold() for path in candidates)
    args.output.mkdir(parents=True, exist_ok=True)

    converted = 0
    skipped = 0
    failed = 0
    recovered = 0
    source_bytes = 0
    output_bytes = 0
    for source in candidates:
        if source.suffix.lower() in {".heic", ".heif"} and not heic_enabled:
            print(f"SKIP {source.name}: install pillow-heif to enable HEIC support.")
            skipped += 1
            continue

        output_name = f"{source.stem}.webp"
        if duplicate_stems[source.stem.casefold()] > 1:
            output_name = f"{source.stem}-{source.suffix.lstrip('.').lower()}.webp"
        destination = args.output / output_name
        if destination.exists() and not args.overwrite:
            print(f"SKIP {source.name}: {destination.name} already exists.")
            skipped += 1
            continue

        try:
            was_recovered = False
            try:
                save_as_webp(source, destination, args.quality)
            except OSError:
                if source.suffix.lower() not in {".jpg", ".jpeg"}:
                    raise
                save_as_webp(source, destination, args.quality, allow_truncated=True)
                recovered += 1
                was_recovered = True
            converted += 1
            source_bytes += source.stat().st_size
            output_bytes += destination.stat().st_size
            status = "RECOVERED" if was_recovered else "OK"
            print(f"{status} {source.name} -> {destination.name}")
        except Exception as error:  # Keep processing the rest of the folder.
            failed += 1
            print(f"ERROR {source.name}: {error}")

    print(
        f"\nDone: {converted} converted ({recovered} recovered), "
        f"{skipped} skipped, {failed} errors."
    )
    if converted:
        reduction = (1 - output_bytes / source_bytes) * 100 if source_bytes else 0
        print(
            f"File size: {source_bytes / 1_000_000:.2f} MB -> "
            f"{output_bytes / 1_000_000:.2f} MB ({reduction:.1f}% smaller)."
        )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
