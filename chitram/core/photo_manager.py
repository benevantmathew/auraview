"""
core/photo_manager.py

Author: Benevant Mathew
Date: 2026-02-16
"""
from PIL import Image
from pillow_heif import register_heif_opener

from chitram.basic_functions.trash import delete_to_trash
from chitram.basic_functions.os_funs import (
    get_all_files, get_end_from_path, move, copy
)
from chitram.core.photo_module import get_image_files
from chitram.gui.gui_functions import get_photo_file

# Register HEIF opener
register_heif_opener()

class PhotoManager:
    """Handles photo-related operations."""

    def __init__(self, files=None, loc='.'):
        self.files = get_image_files(get_all_files(loc)) if files is None else get_image_files(files)
        self.img_nos = list(range(len(self.files)))
        self.img_no = 0
        self.folder_path = ''
        self.folder_q = ''
        print(f'self.files {self.files}')

    def move_photo(self, destination):
        """
        Docstring for move_photo

        :param self: Description
        :param destination: Description
        """
        if not destination:
            print("Folder not selected!")
            return
        image_file = self.files[self.img_nos[self.img_no]]
        move(image_file, f"{destination}/{get_photo_file(image_file)}")
        self.img_nos.pop(self.img_no)

    def copy_photo(self, destination):
        """
        Docstring for copy_photo

        :param self: Description
        :param destination: Description
        """
        if not destination:
            print("Folder not selected!")
            return
        image_file = self.files[self.img_nos[self.img_no]]
        copy(image_file, f"{destination}/{get_end_from_path(image_file)}")

    def delete_photo(self):
        """
        Docstring for delete_photo

        :param self: Description
        """
        delete_to_trash(self.files[self.img_nos[self.img_no]])
        self.img_nos.pop(self.img_no)

    def rotate_photo(self, direction):
        """
        Docstring for rotate_photo

        :param self: Description
        :param direction: Description
        """
        image_file = self.files[self.img_nos[self.img_no]]
        im = Image.open(image_file)
        im = im.transpose(Image.ROTATE_90 if direction == "left" else Image.ROTATE_270)
        im.save(image_file)
