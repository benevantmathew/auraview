"""
core/core.py

Author: Benevant Mathew
Date: 2025-12-16
"""

from PIL import ImageTk, Image
from pillow_heif import register_heif_opener

from chitram.core.photo_module import create_image_obj,  get_image_files
from chitram.basic_functions.os_funs import get_all_files

register_heif_opener()

class PhotoViewerCore:
    """
    The main GUI
    """
    def __init__(self, files=None, loc='.'):

        self.folder_path = ''
        self.folder_q = ''

        # TEMP SIZE so window appears
        self.width = 500
        self.height = 500


        self.files = get_image_files(
            get_all_files(loc)) if files is None else get_image_files(files
        )

        # initiate
        self.img_nos = list(range(len(self.files)))
        self.img_no = 0
        self.img_obj = None
        flag = False

        # derived
        self.count = len(self.img_nos)

        while not flag and self.img_no < self.count:
            try:
                self.image_file = self.files[self.img_nos[self.img_no]]
                self.img_obj = ImageTk.PhotoImage(create_image_obj(self.image_file, self.width, self.height))
                flag = True
            except Exception as e:
                print(f"Error occurred: {e}")
                if self.img_nos:  # Ensure list is not empty before popping
                    self.img_nos.pop(self.img_no)
                self.img_no += 1
        if not flag:
            print('No photos found!')
            self.image_file = None


    def rotate_image(self, direction):
        """
        Docstring for rotate_image
        Rotate and Save

        :param self: Description
        :param direction: Description
        """
        im = Image.open(self.image_file)
        im = im.transpose(Image.ROTATE_90 if direction == 'left' else Image.ROTATE_270)
        im.save(self.image_file)
        self.update_screen()

    def update_screen(self):
        """
        Docstring for update_screen
        fill the image object with new image

        :param self: Description
        """
        if not self.img_nos:
            print('No photos found!')
            return

        if self.img_no >= len(self.img_nos):
            self.img_no = len(self.img_nos) - 1

        try:
            self.image_file = self.files[self.img_nos[self.img_no]]
            self.img_obj = ImageTk.PhotoImage(create_image_obj(self.image_file, self.width, self.height))
        except Exception as e:
            print(f"Error occurred: {e}")
            if self.img_nos:  # Ensure list is not empty before popping
                self.img_nos.pop(self.img_no)
            self.img_no += 1
            self.update_screen()
