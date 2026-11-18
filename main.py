#!/usr/bin/env python3
"""Entry point for "The World Today" — 18 November 2026 (news-image-20261118).

The entry image is a fixed front page rendered at build time by build_image.py
and stored next to this file as entry.png. This program simply copies it to
the output directory, so repeated runs always produce byte-identical output.
Standard library only; no network.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    print("wrote", dest, os.path.getsize(dest), "bytes")


if __name__ == "__main__":
    main()
