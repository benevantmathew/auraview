"""
gui/gui.py


Author: Benevant Mathew
Date: 2025-12-16
"""
import os
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from pillow_heif import register_heif_opener
from chitram.gui.gui_functions import get_photo_file
from chitram.core.photo_module import create_image_obj,  get_image_files,get_pic_wh
from chitram.basic_functions.os_funs import (
    get_all_files, get_end_from_path, move, copy, get_file_size
)
register_heif_opener()

class PhotoViewerGUI:
    """
    The main GUI
    """
    def __init__(self, files=None, loc='.'):

        self.image_file = None
        self.img_obj = None
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

        self.img_nos = list(range(len(self.files)))

        self.root = tk.Tk()
        self.root.update_idletasks()  # important under Wayland

        self.root.title("Chitram")
        self.root.resizable(True, True)

        self.folder_path = ''
        self.folder_q = ''

        # TEMP SIZE so window appears
        self.width = 500
        self.height = 500
        self.display_height = self.height

        # self.root.geometry(f"{self.width}x{self.height}")

        self._create_widgets()
        self._bind_keys()

        self.initialize()

        self.root.bind("<Configure>", self._on_resize)
        self.root.mainloop()

    def _on_resize(self, event):

        # Only react to root window resize
        if event.widget != self.root:
            return

        # Ignore tiny initial size if needed
        if event.width < 50 or event.height < 50:
            return

        if event.width == self.width and event.height == self.height:
            return

        self.width = event.width
        self.height = event.height

        self.display_height = self.height
        if self.display_height<0:
            return

        # print("Resized to:", self.width, self.height)

        # to rescale image dynamically:
        self.update_screen()

    def update_screen(self):
        """
        Updates the displayed image and metadata safely.
        """

        if not self.img_nos:
            print('No photos found!')
            return

        # Clamp index safely
        if self.img_no >= len(self.img_nos):
            self.img_no = len(self.img_nos) - 1

        loaded = False

        while self.img_nos and not loaded:
            try:
                self.image_file = self.files[self.img_nos[self.img_no]]

                img = create_image_obj(
                    self.image_file,
                    self.width,
                    self.display_height
                )

                self.img_obj = ImageTk.PhotoImage(img)
                loaded = True

            except Exception as e:
                print(f"Error loading {self.files[self.img_nos[self.img_no]]}: {e}")

                # Remove bad image
                self.img_nos.pop(self.img_no)

                # If list became empty
                if not self.img_nos:
                    break

                # Clamp again
                if self.img_no >= len(self.img_nos):
                    self.img_no = len(self.img_nos) - 1

        if not loaded:
            print("No valid images remaining.")
            self.image_file = None
            return

        # Update UI
        self.label_img.config(image=self.img_obj)
        self.label_img.image = self.img_obj  # prevent garbage collection

        self.label_name.config(text=get_photo_file(self.image_file))
        self.label_size.config(text=f'Size: {get_file_size(self.image_file)} Mb')
        self.label_dimensions.config(
            text=f'Image Dimensions: {get_pic_wh(self.image_file)}'
        )

    def initialize(self):
        """
        Initializes the image viewer state.
        """
        if not self.img_nos:
            print("No photos found!")
            self.image_file = None
            return

        # Let update_screen handle everything
        self.update_screen()

    def move_f(self, quick=False):
        """
        Docstring for move_f

        :param self: Description
        :param quick: Description
        """
        if not quick:
            self.folder_q = filedialog.askdirectory()
            if not self.folder_q:
                print('Folder not selected!')
                return

        self.folder_path = '\\'.join(self.folder_q.split('/'))
        move(self.image_file, f'{self.folder_path}\\{get_photo_file(self.image_file)}')
        self.img_nos.pop(self.img_no)
        self.update_screen()

    def copy_f(self, quick=False):
        """
        Docstring for copy_f

        :param self: Description
        :param quick: Description
        """
        if not quick:
            self.folder_q = filedialog.askdirectory()
            if not self.folder_q:
                print('Folder not selected!')
                return

        self.folder_path = '\\'.join(self.folder_q.split('/'))
        copy(self.image_file, f'{self.folder_path}\\{get_end_from_path(self.image_file)}')
        self.update_screen()

    def rotate_image(self, direction):
        """
        Docstring for rotate_image

        :param self: Description
        :param direction: Description
        """
        im = Image.open(self.image_file)
        im = im.transpose(Image.ROTATE_90 if direction == 'left' else Image.ROTATE_270)
        im.save(self.image_file)
        self.update_screen()

    def navigate(self, direction):
        """
        Docstring for navigate

        :param self: Description
        :param direction: Description
        """
        if direction == 'forward' and self.img_no < len(self.img_nos) - 1:
            self.img_no += 1
        elif direction == 'back' and self.img_no > 0:
            self.img_no -= 1
        self.update_screen()

    def _create_widgets(self):
        """
        Docstring for _create_widgets

        :param self: Description
        """
        # main frame
        self.main_frame = tk.LabelFrame(
            self.root,
            padx=10,
            pady=10
        )
        self.main_frame.pack(fill="both", expand=True)

        self.main_frame.grid_rowconfigure(1, weight=1)   # image row grows
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(3, weight=1)
        self.main_frame.grid_columnconfigure(4, weight=1)
        self.main_frame.grid_columnconfigure(5, weight=1)

        self.label_img = tk.Label(self.main_frame, image=self.img_obj)
        self.label_img.grid(row=1, column=0, columnspan=6, sticky="nsew")

        self.label_name = tk.Label(self.main_frame)
        self.label_name.grid(row=2, column=1, columnspan=2)

        self.label_size = tk.Label(self.main_frame)
        self.label_size.grid(row=2, column=5)

        self.label_dimensions = tk.Label(self.main_frame)
        self.label_dimensions.grid(row=2, column=3)

        self.button_back = tk.Button(
            self.main_frame,
            text="Back",
            command=lambda: self.navigate('back'),
            width=20
        )
        self.button_forward = tk.Button(
            self.main_frame,
            text="Forward",
            command=lambda: self.navigate('forward'),
            width=20
        )
        self.button_exit = tk.Button(
            self.main_frame,
            text="Exit",
            command=self.root.destroy,
            width=20
        )

        self.button_move = tk.Button(
            self.main_frame,
            text="Move",
            command=self.move_f,
            width=20
        )
        self.button_copy = tk.Button(
            self.main_frame,
            text="Copy",
            command=self.copy_f,
            width=20
        )
        self.button_rotate_left = tk.Button(
            self.main_frame,
            text="Rotate Left",
            command=lambda: self.rotate_image('left'),
            width=20
        )
        self.button_rotate_right = tk.Button(
            self.main_frame,
            text="Rotate Right",
            command=lambda: self.rotate_image('right'),
            width=20
        )

        self.button_back.grid(row=6, column=0)
        self.button_forward.grid(row=6, column=1)
        self.button_exit.grid(row=6, column=5)
        self.button_move.grid(row=7, column=1)
        self.button_copy.grid(row=7, column=2)
        self.button_rotate_left.grid(row=7, column=4)
        self.button_rotate_right.grid(row=7, column=5)

    def _bind_keys(self):
        """
        Docstring for _bind_keys

        :param self: Description
        """
        self.root.bind('<Right>', lambda e: self.navigate('forward'))
        self.root.bind('<Left>', lambda e: self.navigate('back'))
        self.root.bind('<Escape>', lambda e: self.root.destroy())
