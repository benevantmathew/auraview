"""
auraview/main.py

Author: Benevant Mathew
Date: 2026-02-19
"""

import sys
import os
import argparse

from auraview.gui.gui import PhotoViewerGUI
from auraview.version import (
    __version__, __email__, __release_date__, __author__
)
from auraview.help import print_help


def parse_arguments():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        prog="auraview",
        description="A minimal and fast photo viewer.",
        add_help=False
    )

    # Standard flags
    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument("-a", "--author", action="store_true")
    parser.add_argument("-e", "--email", action="store_true")
    parser.add_argument("-d", "--date", action="store_true")

    # New logfile support
    parser.add_argument(
        "--logfile",
        type=str,
        help="Path to a logfile containing full image paths (one per line)"
    )

    # Positional argument (file or directory)
    parser.add_argument(
        "path",
        nargs="?",
        help="Image file or directory path"
    )

    return parser.parse_args()


def main():
    """
    Docstring for main
    """
    args = parse_arguments()

    # --- Meta info flags ---
    if args.help:
        print_help()
        sys.exit(0)

    if args.version:
        print(f"version {__version__}")
        sys.exit(0)

    if args.author:
        print(f"Author {__author__}")
        sys.exit(0)

    if args.email:
        print(f"Mailto {__email__}")
        sys.exit(0)

    if args.date:
        print(f"Release Date {__release_date__}")
        sys.exit(0)

    # --- Logfile mode ---
    if args.logfile:
        if not os.path.isfile(args.logfile):
            print("Invalid logfile path")
            sys.exit(1)

        with open(args.logfile, "r") as f:
            files = [line.strip() for line in f if line.strip()]

        obj = PhotoViewerGUI(files=files)
        obj.run()
        return

    # --- Normal mode ---
    if args.path:
        if os.path.isdir(args.path):
            obj=PhotoViewerGUI(loc=args.path)
            obj.run()
        else:
            obj = PhotoViewerGUI(files=args.path)
            obj.run()
    else:
        obj = PhotoViewerGUI()
        obj.run()


if __name__ == "__main__":
    main()
