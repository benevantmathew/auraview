"""
chitram/main.py


Author: Benevant Mathew
Date: 2026-02-19
"""

import sys
import os

from chitram.gui.gui import PhotoViewerGUI

from chitram.version import (
    __version__,__email__,__release_date__,__author__
)
from chitram.help import print_help

# Main entry point
def main():
    """
    main
    """
    # Check for command-line arguments
    if "--version" in sys.argv or "-v" in sys.argv:
        print(f"version {__version__}")
        sys.exit(0)
    if "--help" in sys.argv or "-h" in sys.argv:
        print_help()
        sys.exit(0)
    if "--author" in sys.argv or "-a" in sys.argv:
        print(f"Author {__author__}")
        sys.exit(0)
    if "--email" in sys.argv or "-e" in sys.argv:
        print(f"Mailto {__email__}")
        sys.exit(0)
    if "--date" in sys.argv or "-d" in sys.argv:
        print(f"Release Date {__release_date__}")
        sys.exit(0)
    if len(sys.argv) > 1:
        if os.path.isdir(sys.argv[1]):
            loc=sys.argv[1]
            PhotoViewerGUI(loc=loc)

        else:
            files=sys.argv[1]
            PhotoViewerGUI(files=files)
    else:
        PhotoViewerGUI()

if __name__ == "__main__":
    main()
