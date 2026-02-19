"""
basic_functions/trash.py

Author: Benevant Mathew
Date: 2025-12-16
"""

import os

from send2trash import send2trash

def delete_to_trash(path):
    """
    a function to handle deletion to recycle bin in multiple os
    """
    if not os.path.exists(path):
        print(f"Path not found: {path}")
        return 0
    try:
        send2trash(path)
        return 1
    except Exception as e:
        print(f"Failed: {e}")
        return 0
