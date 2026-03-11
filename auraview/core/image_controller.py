"""
auraview/core/image_controller.py

Author: Benevant Mathew
Date: 2026-02-21
"""
import os
from natsort import natsorted

from PIL import Image, UnidentifiedImageError, ImageOps
from pillow_heif import register_heif_opener

from auraview.basic_functions.trash import delete_to_trash
from auraview.basic_functions.os_funs import (
    get_all_files, get_end_from_path, move, copy, get_file_size
)
from auraview.basic_functions.time_funs import file_creation_time
from auraview.core.photo_module import (
    create_image_obj, get_pic_wh, update_datetime, correct_image_ext,
    get_dpi_text, get_image_ext, get_photo_dir, image_datetime_original,
    image_datetime_digitized,image_datetime
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
        self.files = files
        self.loc = loc
        self.img_no = 0
        self.folder_path=''
        self.folder_quick_operation=''

        # defaults
        self.image_ext = {".png", ".jpg", ".jpeg", ".heic"}

        # Normalize loc always
        self.loc = os.path.abspath(os.path.expanduser(self.loc))

        # If a single file is passed
        if isinstance(self.files, str):

            # Normalize file path
            self.files = os.path.abspath(os.path.expanduser(self.files))

            if os.path.isfile(self.files):
                self.loc = os.path.dirname(self.files)
                all_files = self._get_image_files(loc=self.loc)

                # Set index to the clicked file
                try:
                    self.img_no = all_files.index(self.files)
                except ValueError:
                    self.img_no = 0

                self.files = all_files

        # If multiple files passed
        elif isinstance(self.files, (list, tuple)):
            # Normalize every file
            self.files = [
                os.path.abspath(os.path.expanduser(f))
                for f in self.files
            ]

            # review if file exist
            self.files = [
                f
                for f in self.files
                if os.path.exists(f)
            ]

            self.files = self._get_image_files(files=self.files)

        # If nothing passed
        else:
            self.files = self._get_all_image_files(loc=self.loc)

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
    # -------------------------------------------------
    # File Operations
    # -------------------------------------------------
    def _get_image_files(self, files=None, loc=None, full_path=True, reverse=False):
        """
        Return image files from a list or directory.
        if input is files do not sort

        Parameters
        ----------
        files : list[str] | None
            List of file paths or names
        loc : str | None
            Directory to scan if files is None
        full_path : bool
            Return absolute paths if True
        reverse : bool
            Reverse sorting order
        """
        scanned = False

        # If files not provided, read directory
        if files is None:
            if loc is None:
                raise ValueError("Either 'files' or 'loc' must be provided")

            scanned = True
            files = []
            for entry in os.scandir(loc):
                if entry.is_file():
                    files.append(entry.path if full_path else entry.name)

        # Filter image extensions
        filtered = []
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in self.image_ext:
                filtered.append(f)

        # Only sort if scanned from directory
        if scanned:
            filtered = natsorted(
                filtered,
                key=lambda x: os.path.basename(x),
                reverse=reverse
            )

        return filtered

    def _get_all_image_files(self, loc, reverse=False):
        """
        Return all image files inside a directory and its subdirectories.

        Parameters
        ----------
        loc : str
            Root directory
        reverse : bool
            Reverse sorting order

        Returns
        -------
        list[str]
        """

        out = []

        for path, _, files in os.walk(loc):
            for name in files:
                ext = os.path.splitext(name)[1].lower()
                if ext in self.image_ext:
                    out.append(os.path.join(path, name))

        out = natsorted(out, key=lambda x: os.path.basename(x), reverse=reverse)

        return out
