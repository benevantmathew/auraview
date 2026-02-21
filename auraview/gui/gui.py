"""
auraview/gui/gui.py

Author: Benevant Mathew
Date: 2025-12-16
"""
import tkinter as tk
from tkinter import filedialog

from PIL import ImageTk
from pillow_heif import register_heif_opener

from auraview.core.image_controller import ImageController

# Register HEIF opener
register_heif_opener()

class PhotoViewerGUI:
    """
    The main GUI
    """
    def __init__(
            self,
            files=None,
            loc='.'
        ):

        self.controller = ImageController(files, loc)

        self.img_obj = None

        self.root = tk.Tk()
        self.root.update_idletasks()  # important under Wayland

        self.root.title("AuraView")
        self.root.resizable(True, True)

        # TEMP SIZE so window appears
        self.width = 500
        self.height = 500
        self.display_height = self.height

        self._create_widgets()
        self._bind_keys()

        self.update_screen()

        self.root.bind("<Configure>", self._on_resize)
        self.root.mainloop()

    # -------------------------------------------------
    # Window Resize Handling
    # -------------------------------------------------
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

        # to rescale image dynamically:
        self.update_screen()

    # -------------------------------------------------
    # Screen Update
    # -------------------------------------------------
    def update_screen(self):
        """
        Docstring for update_screen

        :param self: Description
        """

        img = self.controller.get_resized_image(self.width, self.display_height)
        if not img:
            return

        self.img_obj = ImageTk.PhotoImage(img)
        self.label_img.config(image=self.img_obj)
        self.label_img.image = self.img_obj # prevent Garbage collection

        metadata = self.controller.get_metadata()

        if metadata:
            self.label_name.config(text=metadata["name"])
            self.label_size.config(text=f'Size: {metadata["size"]} Mb')
            self.label_dimensions.config(
                text=f'Image Dimensions: {metadata["dimensions"]}'
            )

    # -------------------------------------------------
    # Image Operations (Delegated to Controller)
    # -------------------------------------------------
    def navigate(self, direction):
        """
        Docstring for navigate

        :param self: Description
        :param direction: Description
        """

        if direction == "forward":
            self.controller.next()
        else:
            self.controller.previous()

        self.update_screen()

    def rotate_image(self, direction):
        """
        Docstring for rotate_image

        :param self: Description
        :param direction: Description
        """

        self.controller.rotate_current(direction)
        self.update_screen()

    def move_f(self):
        """
        Docstring for move_f

        :param self: Description
        """

        folder = filedialog.askdirectory()
        if not folder:
            return

        self.controller.move_current(folder)
        self.update_screen()

    def copy_f(self):
        """
        Docstring for copy_f

        :param self: Description
        """

        folder = filedialog.askdirectory()
        if not folder:
            return

        self.controller.copy_current(folder)
        self.update_screen()

    # -------------------------------------------------
    # UI Creation
    # -------------------------------------------------
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
