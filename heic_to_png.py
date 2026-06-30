#!/usr/bin/env python3
"""Convert HEIC image files to PNG format."""

import sys
import os
import argparse


def check_dependencies():
    missing = []
    try:
        import pillow_heif  # noqa: F401
    except ImportError:
        missing.append("pillow-heif")
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        missing.append("Pillow")
    if missing:
        print(f"Missing required packages: {', '.join(missing)}")
        print(f"Install with: pip3 install {' '.join(missing)}")
        sys.exit(1)


def convert_heic_to_png(input_path, output_path=None):
    import pillow_heif
    from PIL import Image

    pillow_heif.register_heif_opener()

    if not os.path.isfile(input_path):
        print(f"Error: file not found: {input_path}")
        return False

    if not input_path.lower().endswith(".heic"):
        print(f"Warning: {input_path} does not have a .heic extension, skipping")
        return False

    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + ".png"

    try:
        img = Image.open(input_path)
        img.save(output_path, format="PNG")
        print(f"Converted: {input_path} -> {output_path}")
        return True
    except Exception as e:
        print(f"Error converting {input_path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Convert HEIC image files to PNG format."
    )
    parser.add_argument("files", nargs="+", help="HEIC file(s) to convert")
    parser.add_argument(
        "-o", "--output", help="Output file path (only valid when converting a single file)"
    )
    args = parser.parse_args()

    if args.output and len(args.files) > 1:
        print("Error: -o/--output can only be used when converting a single file")
        sys.exit(1)

    check_dependencies()

    success_count = 0
    for f in args.files:
        output = args.output if args.output else None
        if convert_heic_to_png(f, output):
            success_count += 1

    total = len(args.files)
    if total > 1:
        print(f"\nDone: {success_count}/{total} files converted successfully")

    if success_count < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
