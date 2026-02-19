"""
application/gui_functions.py

Author: Benevant Mathew
Date: 2025-12-16
"""

import os
from chitram.core.photo_module import get_native_dpi
from chitram.basic_functions.os_funs import get_previous_dir_from_path,get_end_from_path


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

def get_photo_file(image_file):
    """
    Docstring for get_photo_file

    :param image_file: Description
    """
    if get_previous_dir_from_path(image_file)==image_file:
        out=image_file
    else:
        out=get_end_from_path(image_file)
    return(out)

def get_photo_dir(image_file):
    """
    Docstring for get_photo_dir

    :param image_file: Description
    """
    if get_previous_dir_from_path(image_file)==image_file:
        out=os.getcwd()
    else:
        out=get_previous_dir_from_path(image_file)
    return(out)
