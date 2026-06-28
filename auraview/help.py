"""
help.py

Author: Benevant Mathew
Date: 2026-02-19
"""
import sys
# Function to display help
def print_help():
    """
    help function
    """
    help_message = """
Usage: auraview [OPTIONS]

A small package to compare the files between two project folders.

Options:
    --version, -v      Show the version of auraview and exit
    --help, -h         Show this help message and exit
    --email, -e        Show email and exit
    --author, -a       Show author and exit
    --theme THEME      Override settings theme: dark or light
    --font_family FONT Override GUI font family for this run
    --font_size SIZE   Override GUI font size for this run
    --tk_scaling ZOOM  Override Tk scaling for this run
    --non-recursive    With folder input, only add images directly in that folder
    (No arguments)     Launch an empty GUI application
    [folder_path]  or [filelist/single file]

Shortcuts:
    Ctrl + +          Zoom in
    Ctrl + -          Zoom out
    Ctrl + 0          Reset view
    Ctrl + MouseWheel Zoom in/out
    Ctrl + Middle     Reset view
    Ctrl + Left Mouse Pan zoomed image
    MouseWheel        Vertical scroll
    Middle Drag       Vertical scroll
    Horizontal Wheel  Horizontal scroll
    """
    print(help_message)
    sys.exit(0)
