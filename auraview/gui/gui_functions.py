"""
application/gui_functions.py

Author: Benevant Mathew
Date: 2025-12-16
"""

from auraview.core.photo_module import get_native_dpi

def get_dpi_text(image_file):
    """
    Docstring for get_dpi_text
    # GUI support functions (independent) (without nonlocal varaiable)

    :param image_file: Description
    """

    dpi = get_native_dpi(image_file)
    if dpi!=None:
        out_txt='Native DPI: {} x {}'.format(dpi[0],dpi[1])
    else:
        out_txt='Native DPI: NA'
    return out_txt
