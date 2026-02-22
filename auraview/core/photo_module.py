"""
application/photo_module.py

Author: Benevant Mathew
Date: 2025-12-16
"""
import os
from PIL import Image
import piexif
from auraview.basic_functions.os_funs import (
    cwdfiles, get_ext_files, get_ext, get_rootname, rename,
    get_previous_dir_from_path,get_end_from_path
)
from auraview.basic_functions.convert import (
    metric_convert
)
from auraview.basic_functions.time_funs import (
	unix_time2norm,datetime2string,string2datetime
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
    Ensure file extension matches actual image format.
    Returns new file path if renamed, otherwise original path.
    """

    ext = get_image_ext(file)  # true format from image
    current_ext = get_ext(file)

    if not ext:
        return file

    if current_ext.lower() == ext.lower():
        return file  # already correct

    new_path = get_rootname(file) + '.' + ext.lower()

    # Avoid overwriting existing file
    if os.path.exists(new_path):
        return file

    try:
        rename(file, new_path)
        print(f"file [{file}] renamed to {new_path}")
        return new_path
    except OSError:
        return file

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

def update_datetime(image_path, new_datetime,mode='string',format='%m/%d/%y'):
    """
    Docstring for update_datetime

    :param image_path: Description
    :param new_datetime: Description
    :param mode: Description
    :param format: Description
    """
    try:
        # get current datetime from the image
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data is not None:
            if 306 in exif_data:
                dt=exif_data[306]
            elif 36867 in exif_data:
                dt=exif_data[36867]
            elif 36868 in exif_data:
                dt=exif_data[36868]
            else:
                dt=unix_time2norm(os.path.getctime(image_path))
                dt=datetime2string(dt)
            # now modify the datetime
            if mode=='string':
                if format=='%m/%d/%y':
                    new_datetime=string2datetime(new_datetime,format)
                    new_datetime=datetime2string(new_datetime,format='%Y:%m:%d')
                    if dt.split()!=[dt]:
                        new_datetime=new_datetime+' '+dt.split()[1]
                    else:
                        new_datetime=new_datetime+' 00:00:00'
            else:
                new_datetime=datetime2string(new_datetime)
            exif_dict = piexif.load(image_path)
            exif_dict['0th'][piexif.ImageIFD.DateTime] = new_datetime
            exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_datetime
            exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_datetime
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, image_path)
            print(f"Datetime value updated successfully.")
        else: # print(f"No EXIF data found in the image {image_path}.")
            new_datetime=string2datetime(new_datetime,format)
            new_datetime=datetime2string(new_datetime,format='%Y:%m:%d')
            new_datetime=new_datetime+' 00:00:00'
            exif_dict = piexif.load(image_path)
            #Update DateTimeOriginal
            exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_datetime
            #Update DateTimeDigitized
            exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_datetime
            #Update DateTime
            exif_dict['0th'][piexif.ImageIFD.DateTime] = new_datetime
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, image_path)
            print(f"Datetime value updated successfully.")
    except Exception as e:
        print(f"An error occurred: {e} for {image_path}")

def get_photo_file(image_file):
    """
    Docstring for get_photo_file

    :param image_file: Description
    """
    if get_previous_dir_from_path(image_file)==image_file:
        out=image_file
    else:
        out=get_end_from_path(image_file)
    return out

def get_photo_dir(image_file):
    """
    Docstring for get_photo_dir

    :param image_file: Description
    """
    if get_previous_dir_from_path(image_file)==image_file:
        out=os.getcwd()
    else:
        out=get_previous_dir_from_path(image_file)
    return out
