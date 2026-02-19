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
Usage: chitram [OPTIONS]

A small package to compare the files between two project folders.

Options:
    --version, -v      Show the version of chitram and exit
    --help, -h         Show this help message and exit
    --email, -e        Show email and exit
    --author, -a       Show author and exit
    (No arguments)     Launch the GUI application
    [folder_path]  or [filelist/single file]
    """
    print(help_message)
    sys.exit(0)
