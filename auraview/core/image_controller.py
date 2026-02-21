"""
auraview/core/image_controller.py

Author: Benevant Mathew
Date: 2026-02-21
"""
import os

from PIL import Image
from pillow_heif import register_heif_opener

from auraview.basic_functions.trash import delete_to_trash
from auraview.basic_functions.os_funs import (
    get_all_files, get_end_from_path, move, copy, get_file_size
)
from auraview.core.photo_module import (
    create_image_obj, get_image_files, get_pic_wh
)

# Register HEIF opener
register_heif_opener()

class ImageController:
    """Handles photo-related operations."""

    def __init__(
            self,
            files=None,
            loc='.'
        ):

        self.img_no = 0

        # If a single file is passed
        if isinstance(files, str):
            if os.path.isfile(files):
                loc = os.path.dirname(files)
                all_files = get_image_files(get_all_files(loc))

                self.files = all_files

                # Set index to the clicked file
                try:
                    self.img_no = all_files.index(files)
                except ValueError:
                    self.img_no = 0
            else:
                # fallback
                self.files = get_image_files(get_all_files(loc))

        # If multiple files passed
        elif isinstance(files, (list, tuple)):
            self.files = get_image_files(files)

        # If nothing passed
        else:
            self.files = get_image_files(get_all_files(loc))

    # ------------------------
    # Navigation
    # ------------------------

    def next(self):
        """
        Docstring for next

        :param self: Description
        """
        if self.img_no < len(self.files) - 1:
            self.img_no += 1

    def previous(self):
        """
        Docstring for previous

        :param self: Description
        """
        if self.img_no > 0:
            self.img_no -= 1

    # ------------------------
    # Image loading
    # ------------------------
    def get_current_path(self):
        """
        Docstring for get_current_path

        :param self: Description
        """
        if not self.files:
            return None
        return self.files[self.img_no]

    def get_resized_image(self, width, height):
        """
        Docstring for get_resized_image

        :param self: Description
        :param width: Description
        :param height: Description
        """
        path = self.get_current_path()
        if not path:
            return None
        return create_image_obj(path, width, height)

    def get_metadata(self):
        """
        Docstring for get_metadata

        :param self: Description
        """
        path = self.get_current_path()
        if not path:
            return None

        return {
            "name": os.path.basename(path),
            "size": get_file_size(path),
            "dimensions": get_pic_wh(path),
        }

    # ------------------------
    # File operations
    # ------------------------
    def move_current(self, destination):
        """
        Docstring for move_current

        :param self: Description
        :param destination: Description
        """
        path = self.get_current_path()
        if not path:
            return

        new_path = os.path.join(destination, get_end_from_path(path))
        move(path, new_path)
        self.files.pop(self.img_no)

    def copy_current(self, destination):
        """
        Docstring for copy_current

        :param self: Description
        :param destination: Description
        """
        path = self.get_current_path()
        if not path:
            return

        new_path = os.path.join(destination, get_end_from_path(path))
        copy(path, new_path)

    def rotate_current(self, direction):
        """
        Docstring for rotate_current

        :param self: Description
        :param direction: Description
        """
        path = self.get_current_path()
        if not path:
            return

        im = Image.open(path)
        if direction == "left":
            im = im.transpose(Image.ROTATE_90)
        else:
            im = im.transpose(Image.ROTATE_270)
        im.save(path)

    def delete_current(self):
        """
        Docstring for delete_current

        :param self: Description
        """
        path = self.get_current_path()
        if not path:
            return

        delete_to_trash(path)
        self._remove_current()

    # -------------------------------------------------
    # Internal Helpers
    # -------------------------------------------------

    def _remove_current(self):
        """
        Remove current file from list and clamp index.
        """
        if not self.files:
            return

        self.files.pop(self.img_no)

        if self.img_no >= len(self.files):
            self.img_no = max(len(self.files) - 1, 0)
