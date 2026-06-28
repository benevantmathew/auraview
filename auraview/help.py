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
    (No arguments)     Launch the GUI application
    [folder_path]  or [filelist/single file]

Shortcuts:
    Ctrl + +          Zoom in
    Ctrl + -          Zoom out
    Ctrl + 0          Reset view
    Ctrl + Left Mouse Pan zoomed image
    """
    print(help_message)
    sys.exit(0)
