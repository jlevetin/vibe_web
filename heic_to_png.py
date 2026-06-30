#!/usr/bin/env python3
"""Convert HEIC image files to PNG format using heif-convert (no pip required)."""

import sys
import os
import argparse
import subprocess
import shutil


def check_dependencies():
    if shutil.which("heif-convert") is None:
        print("Missing required tool: heif-convert")
        print("Install with: sudo apt install libheif-examples")
        sys.exit(1)


def convert_heic_to_png(input_path, output_path=None):
    if not os.path.isfile(input_path):
        print(f"Error: file not found: {input_path}")
        return False

    if not input_path.lower().endswith(".heic"):
        print(f"Warning: {input_path} does not have a .heic extension, skipping")
        return False

    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + ".png"

    try:
        result = subprocess.run(
            ["heif-convert", input_path, output_path],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"Error converting {input_path}: {result.stderr.strip()}")
            return False
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
        "-o", "--output",
        help="Output file path (only valid when converting a single file)",
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
