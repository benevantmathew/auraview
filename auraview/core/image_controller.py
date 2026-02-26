"""
auraview/core/image_controller.py

Author: Benevant Mathew
Date: 2026-02-21
"""
import os

from PIL import Image, UnidentifiedImageError, ImageOps
from pillow_heif import register_heif_opener

from auraview.basic_functions.trash import delete_to_trash
from auraview.basic_functions.os_funs import (
    get_all_files, get_end_from_path, move, copy, get_file_size, cwdfiles
)
from auraview.basic_functions.time_funs import file_creation_time
from auraview.core.photo_module import (
    create_image_obj, get_image_files, get_pic_wh, update_datetime, correct_image_ext,
    get_dpi_text, get_image_ext, get_photo_dir, image_datetime_original, image_datetime_digitized,
    image_datetime
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
        self.folder_path=''
        self.folder_quick_operation=''

        # Normalize loc always
        loc = os.path.abspath(os.path.expanduser(loc))

        # If a single file is passed
        if isinstance(files, str):

            # Normalize file path
            files = os.path.abspath(os.path.expanduser(files))

            if os.path.isfile(files):
                loc = os.path.dirname(files)
                all_files = get_image_files(cwdfiles(loc))

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
            # Normalize every file
            files = [
                os.path.abspath(os.path.expanduser(f))
                for f in files
            ]

            # review if file exist
            files = [
                f
                for f in files
                if os.path.exists(f)
            ]

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

    def home(self):
        """
        Docstring for home

        :param self: Description
        """
        if self.files:
            self.img_no = 0

    def end(self):
        """
        Docstring for end

        :param self: Description
        """
        if self.files:
            self.img_no = len(self.files) - 1

    def go_to(self, index):
        """
        Docstring for go_to

        :param self: Description
        :param index: Description
        """
        if 0 <= index < len(self.files):
            self.img_no = index
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
        Return resized image object.
        Automatically removes invalid/corrupted images.
        """

        while self.files:
            path = self.get_current_path()

            if not path:
                return None

            if not os.path.exists(path):
                print(f"Path does not exist: {path}")
                self._remove_current()
                continue

            try:
                return create_image_obj(path, width, height)

            except UnidentifiedImageError:
                print(f"Removing invalid image: {path}")
                self._remove_current()

        return None

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
            "dpi_text": get_dpi_text(path),
            "ext": str(get_image_ext(path)),
            "image_dir": get_photo_dir(path),
            "image_datetimeoriginal":image_datetime_original(path),
            "image_datetimedigitized": image_datetime_digitized(path),
            "image_datetime":image_datetime(path),
            "image_filecreationtime": file_creation_time(path),
            "move_copy_dir": self.folder_path
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
    def quick_move(self):
        """
        Docstring for quick_move
        """

        if self.folder_quick_operation=='':
            print('folder not selected!')
            return False

        self.move_current(self.folder_quick_operation)
        return True

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
    def quick_copy(self):
        """
        Docstring for quick_copy
        """

        if self.folder_quick_operation=='':
            print('folder not selected!')
            return

        self.copy_current(self.folder_quick_operation)

    def rotate_current(self, direction):
        """
        Docstring for rotate_current

        :param self: Description
        :param direction: Description
        """
        path = self.get_current_path()
        if not path:
            return

        with Image.open(path) as im:
            # Preserve metadata
            exif = im.getexif()
            icc_profile = im.info.get("icc_profile")

            # Step 1: Normalize orientation automatically
            im = ImageOps.exif_transpose(im)

            # Step 2: Apply user rotation
            if direction == "left":
                im = im.rotate(90, expand=True)
            elif direction == "right":
                im = im.rotate(-90, expand=True)
            else:
                return

            # Step 3: Reset orientation tag
            if exif:
                exif[274] = 1  # Orientation tag

            # Step 4: Save safely
            im.save(
                path,
                format=im.format,
                exif=exif.tobytes() if exif else None,
                icc_profile=icc_profile,
                quality=95
            )

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
    # -------------------------------------------------
    # Image Operations
    # -------------------------------------------------
    def update_datetime(self, date_str):
        """
        Docstring for update_datetime

        :param self: Description
        :param date_str: Description
        """
        path = self.get_current_path()
        if not path:
            return
        update_datetime(path, date_str)

    def correct_extension(self):
        """
        Docstring for correct_extension

        :param self: Description
        """
        path = self.get_current_path()
        if not path:
            return

        new_path = correct_image_ext(path)

        # If renamed → update internal list
        if new_path != path:
            self.files[self.img_no] = new_path
