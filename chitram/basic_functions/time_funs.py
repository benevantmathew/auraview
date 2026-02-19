"""
basic_functions/time_funs.py

Author: Benevant Mathew
Date: 2025-12-16
"""

import os
from datetime import datetime

def unix_time2norm(unix_val):
    """
    Docstring for unix_time2norm

    :param unix_val: Description
    """
    return(datetime.fromtimestamp(unix_val))

def datetime2string(dobj,format='%Y:%m:%d %H:%M:%S'):
    """
    Docstring for datetime2string

    :param dobj: Description
    :param format: Description
    """
    return(dobj.strftime(format))

def file_creation_time(file):
    """
    Docstring for file_creation_time

    :param file: Description
    """
    # FileCreationTime Tag
    dt=unix_time2norm(os.path.getctime(file))
    dt=datetime2string(dt)
    return dt
