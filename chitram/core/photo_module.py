"""
application/photo_module.py

Author: Benevant Mathew
Date: 2025-12-16
"""

from PIL import Image
from chitram.basic_functions.os_funs import (
    cwdfiles, get_ext_files, get_ext, get_rootname, rename
)
from chitram.basic_functions.convert import (
    metric_convert
)

# Photo module
def pic_auto_size(img, max_w, max_h):
    """
    Docstring for pic_auto_size

    :param img: Description
    :param max_w: Description
    :param max_h: Description
    """

    with Image.open(img) as im:
        w, h = im.size

    if w == 0 or h == 0:
        return (0, 0)

    scale = min(max_w / w, max_h / h)

    new_w = int(w * scale)
    new_h = int(h * scale)

    return new_w, new_h

def image_datetime(file):
    """
    Docstring for image_datetime

    :param file: Description
    """
    # DateTime Tag
    im = Image.open(file)
    tags=im.getexif()
    im.close()
    try:
        dt=tags[306]
    except:
        dt='NA'
    return(dt)

def image_datetime_original(file):
    """
    Docstring for image_datetime_original

    :param file: Description
    """
    # DateTimeOriginal Tag
    im = Image.open(file)
    tags = im.getexif()
    im.close()
    try:
        dt = tags[36867]
    except:
        dt = 'NA'
    return dt

def image_datetime_digitized(file):
    """
    Docstring for image_datetime_digitized

    :param file: Description
    """
    # DateTimeDigitized Tag
    im = Image.open(file)
    tags = im.getexif()
    im.close()
    try:
        dt = tags[36868]
    except:
        dt = 'NA'
    return dt

def create_image_obj(file, width, height):
    """
    Docstring for create_image_obj

    :param file: Description
    :param width: Description
    :param height: Description
    """
    pic_size = pic_auto_size(file, width, height)
    obj = Image.open(file).resize(pic_size,Image.LANCZOS)
    return obj

def get_image_ext(file):
    """
    Docstring for get_image_ext

    :param file: Description
    """
    img = Image.open(file)
    return img.format

def get_image_files(files=None, loc=None):
    """
    Docstring for get_image_files

    :param files: Description
    :param loc: Description
    """
    if files == None:
        files = cwdfiles(loc)
    filtered = get_ext_files(['png', 'PNG', 'JPEG', 'jpeg', 'jpg', 'JPG', 'heic', 'HEIC'], files=files)
    return filtered

def correct_image_ext(file):
    """
    Docstring for correct_image_ext

    :param file: Description
    """
    try:
        ext = get_image_ext(file)
        if get_ext(file).lower() != ext.lower():
            y = get_rootname(file) + '.' + ext
            rename(file, y)
            print('file [{}] renamed to {}.'.format(file, y))
    except:
        pass
    return print('function_completed')

def get_pic_wh(img,mode='pixel',dpi='default'):
    """
    Docstring for get_pic_wh

    :param img: Description
    :param mode: Description
    :param dpi: Description
    """
    im=Image.open(img)
    w,h=im.size
    if mode=='pixel' and dpi=='default':
        pass
    elif mode=='mm' and dpi!='default':
        w=metric_convert(w/dpi,'inch','mm')
        h=metric_convert(h/dpi,'inch','mm')
    elif mode=='cm' and dpi!='default':
        w=metric_convert(w/dpi,'inch','cm')
        h=metric_convert(h/dpi,'inch','cm')
    elif mode=='inch' and dpi!='default':
        w=w/dpi
        h=h/dpi
    return(w,h)

def get_native_dpi(file):
    """
    Docstring for get_native_dpi

    :param file: Description
    """
    #dpi out id a tuple with x and y dpi values
    try:
        im = Image.open(file)
        dpi = im.info.get('dpi', None)
        im.close()
        return dpi
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
