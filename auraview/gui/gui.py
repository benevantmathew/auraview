"""
auraview/gui/gui.py

Author: Benevant Mathew
Date: 2025-12-16
"""
import tkinter as tk
from tkinter import filedialog
from tkcalendar import Calendar

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

        # TEMP SIZE so window appears
        self.width = 500
        self.height = 500
        self.display_height = self.height

        self.root = tk.Tk()
        self.selected_option = tk.StringVar(self.root)
        self.date_var = tk.StringVar()

        self.root.update_idletasks()  # important under Wayland

        self.root.title("AuraView")
        self.root.resizable(True, True)

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
            self.label_name.config(text=metadata.get("name",""))
            self.label_size.config(text=f'Size: {metadata.get("size","")} Mb')
            self.label_dimensions.config(
                text=f'Image Dimensions: {metadata.get("dimensions","")}'
            )
            self.label_image_dpi.config(
                text=metadata.get("dpi_text","NA")
            )
            self.label_move_copy_dir.config(
                text=metadata.get("move_copy_dir","")
            )
            self.label_image_ext.config(
                text=metadata.get("ext","")
            )
            self.label_image_datetimeoriginal.config(
                text=f'DateTimeOriginal - {metadata.get("image_datetimeoriginal","")}'
            )
            self.label_image_datetimedigitized.config(
                text=f'DateTimeDigitized - {metadata.get("image_datetimedigitized","")}'
            )
            self.label_image_datetime.config(
                text=f'DateTime - {metadata.get("image_datetime","")}'
            )
            self.label_image_filecreationtime.config(
                text=f'FileCreationTime - {metadata.get("image_filecreationtime","")}'
            )
            self.label_image_dir.config(
                text=metadata.get("image_dir","")
            )

        total = len(self.controller.files)
        current = self.controller.img_no

        self.label_counter.config(text=f"{current+1}/{total}")

        # Button state control
        if current == 0:
            self.button_back.config(state=tk.DISABLED)
        else:
            self.button_back.config(state=tk.NORMAL)

        if current == total - 1:
            self.button_forward.config(state=tk.DISABLED)
        else:
            self.button_forward.config(state=tk.NORMAL)
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
    def move_f2(self):
        """
        Docstring for move_f2
        """
        if self.controller.quick_move():
            # update for successful move operation
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
    def copy_f2(self):
        """
        Docstring for copy_f2
        """
        self.controller.quick_copy()

    def delete_f(self):
        """
        Docstring for delete_f

        :param self: Description
        """

        self.controller.delete_current()
        self.update_screen()

    def home_button(self):
        """
        Docstring for home_button
        """
        self.controller.home()
        self.update_screen()

    def end_button(self):
        """
        Docstring for end_button
        """
        self.controller.end()
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

        ##
        self.main_frame.grid_rowconfigure(1, weight=1)   # image row grows
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(3, weight=1)
        self.main_frame.grid_columnconfigure(4, weight=1)
        self.main_frame.grid_columnconfigure(5, weight=1)

        #All labels
        ## row 1
        self.label_img = tk.Label(self.main_frame, image=self.img_obj)
        self.label_img.grid(row=1, column=0, columnspan=6, sticky="nsew")

        ## row 2
        self.label_counter = tk.Label(self.main_frame)
        self.label_counter.grid(row=2, column=0)

        self.label_name = tk.Label(self.main_frame)
        self.label_name.grid(row=2, column=1, columnspan=2)

        self.label_dimensions = tk.Label(self.main_frame)
        self.label_dimensions.grid(row=2, column=3)

        self.label_image_dpi=tk.Label(self.main_frame)
        self.label_image_dpi.grid(row=2, column=4)

        self.label_size = tk.Label(self.main_frame)
        self.label_size.grid(row=2, column=5)

        ## row 3
        self.label_image_ext = tk.Label(self.main_frame)
        self.label_image_ext.grid(row=3, column=3)

        self.label_image_dir = tk.Label(self.main_frame)
        self.label_image_dir.grid(row=3, column=4)

        ## row 4
        self.label_image_datetimeoriginal = tk.Label(self.main_frame)
        self.label_image_datetimeoriginal.grid(row=4, column=1)

        self.label_image_datetimedigitized = tk.Label(self.main_frame)
        self.label_image_datetimedigitized.grid(row=4, column=2)

        self.label_image_datetime = tk.Label(self.main_frame)
        self.label_image_datetime.grid(row=4, column=3)

        self.label_image_filecreationtime = tk.Label(self.main_frame)
        self.label_image_filecreationtime.grid(row=4, column=4)

        ## row 5
        # label15=tk.Label(self.main_frame,text=f'Selected Date : {self.date_var.get()}')
        # label15.grid(row=5, column=3)

        # select_date_button = tk.Button(
        #     self.main_frame,
        #     text="Select Date",
        #     command=self.select_date
        # )
        # select_date_button.grid(row=5, column=4)

        # update_button = tk.Button(
        #     self.main_frame,
        #     text="Update Datetime",
        #     command=self.update_datetime
        # )
        # update_button.grid(row=5, column=5)

        ## row 6
        self.button_back = tk.Button(
            self.main_frame,
            text="Back",
            command=lambda: self.navigate('back'),
            width=20
        )
        self.button_back.grid(row=6, column=0)

        self.button_forward = tk.Button(
            self.main_frame,
            text="Forward",
            command=lambda: self.navigate('forward'),
            width=20
        )
        self.button_forward.grid(row=6, column=1)

        self.button_delete=tk.Button(
            self.main_frame,
            text="Delete",
            command=self.delete_f,
            width=20
        )
        self.button_delete.grid(row=6,column=2)

        self.button_home=tk.Button(
            self.main_frame,
            text="Home",
            command=self.home_button,
            width=20
        )
        self.button_home.grid(row=6, column=3)

        self.button_end=tk.Button(
            self.main_frame,
            text="End",
            command=self.end_button,
            width=20
        )
        self.button_end.grid(row=6, column=4)

        self.button_exit = tk.Button(
            self.main_frame,
            text="Exit",
            command=self.root.destroy,
            width=20
        )
        self.button_exit.grid(row=6, column=5)

        ## row 7
        self.button_quick_move=tk.Button(
            self.main_frame,
            text="Quick_Move",
            command=self.move_f2,
            width=20
        )
        self.button_quick_move.grid(row=7, column=0)

        self.button_move = tk.Button(
            self.main_frame,
            text="Move",
            command=self.move_f,
            width=20
        )
        self.button_move.grid(row=7, column=1)

        self.button_copy = tk.Button(
            self.main_frame,
            text="Copy",
            command=self.copy_f,
            width=20
        )
        self.button_copy.grid(row=7, column=2)

        self.button_quick_copy=tk.Button(
            self.main_frame,
            text="Quick_Copy",
            command=self.copy_f2,
            width=20
        )
        self.button_quick_copy.grid(row=7, column=3)

        self.button_rotate_left = tk.Button(
            self.main_frame,
            text="Rotate Left",
            command=lambda: self.rotate_image('left'),
            width=20
        )
        self.button_rotate_left.grid(row=7, column=4)

        self.button_rotate_right = tk.Button(
            self.main_frame,
            text="Rotate Right",
            command=lambda: self.rotate_image('right'),
            width=20
        )
        self.button_rotate_right.grid(row=7, column=5)

        ## row 8
        self.label_move_copy_dir=tk.Label(self.main_frame)
        self.label_move_copy_dir.grid(row=8, column=0,columnspan=2)

        button_update_ext=tk.Button(
            self.main_frame,
            text="Update Ext",
            command=self.update_extension,
            width=20
        )
        button_update_ext.grid(row=8, column=4)

        ## row 9
        # dropdown = tk.OptionMenu(
        #     self.main_frame,
        #     self.selected_option,
        #     *options,
        #     command=go_button_fun
        # )
        # dropdown.grid(row=9,column=1)

        label8=tk.Label(self.main_frame,text='Photo Number')
        label8.grid(row=9, column=2)

        self.entry_index = tk.Entry(self.main_frame, width=10)
        self.entry_index.grid(row=9, column=3)

        self.button_go = tk.Button(
            self.main_frame,
            text="Go",
            command=self.go_to_index,
            width=10
        )
        self.button_go.grid(row=9, column=4)
        ##

    def go_to_index(self):
        """
        Docstring for go_to_index

        :param self: Description
        """
        try:
            user_input = int(self.entry_index.get())
        except ValueError:
            return

        total = len(self.controller.files)

        if total == 0:
            return

        # Convert from 1-based (user) to 0-based (internal)
        internal_index = user_input - 1

        # Bounds check
        if internal_index < 0:
            internal_index = 0
        elif internal_index >= total:
            internal_index = total - 1

        self.controller.go_to(internal_index)
        self.update_screen()

    def select_date(self):
        """
        Docstring for select_date

        :param self: Description
        """
        top = tk.Toplevel(self.root)
        cal = Calendar(top, selectmode="day")
        cal.pack()

        def confirm():
            selected_date = cal.get_date()
            self.controller.update_datetime(selected_date)
            top.destroy()
            self.update_screen()

        tk.Button(top, text="Set Date", command=confirm).pack()

    def update_extension(self):
        """
        Docstring for update_extension

        :param self: Description
        """
        self.controller.correct_extension()
        self.update_screen()

    def update_datetime(self):
        """
        Docstring for update_datetime

        :param self: Description
        """
        self.controller.update_datetime(self.date_var.get())
        self.update_screen()

    def disable_entry(self,e):
        """
        Docstring for disable_entry

        :param self: Description
        :param e: Description
        """
        if not (self.entry_index==e.widget):
            self.entry_index.config(state="disabled")

    def enable_entry(self):
        """
        Docstring for enable_entry

        :param self: Description
        :param e: Description
        """
        self.entry_index.config(state="normal")

    def return_key2photo_number(self,e):
        """
        Docstring for return_key2photo_number

        :param self: Description
        :param e: Description
        """
        if self.entry_index['state']=='normal':
            self.go_to_index()

    def delete_key(self):
        """
        Docstring for delete_key

        :param self: Description
        :param e: Description
        """
        if self.entry_index['state']=='disabled':
            self.delete_f()

    def _bind_keys(self):
        """
        Docstring for _bind_keys

        :param self: Description
        """
        #root binds
        self.root.bind('<Right>',lambda e: self.navigate('forward'))
        self.root.bind('<Left>',lambda e: self.navigate('back'))
        self.root.bind('<Home>',lambda e: self.home_button())
        self.root.bind('<End>',lambda e: self.end_button())
        self.root.bind('<k>',lambda e: self.rotate_image('left'))
        self.root.bind('<l>',lambda e: self.rotate_image('right'))
        self.root.bind('<q>',lambda e: self.move_f2())
        self.root.bind('<m>',lambda e: self.move_f())
        self.root.bind('<Escape>',lambda e: self.root.destroy())
        self.root.bind("<Button-1>", lambda e: self.disable_entry(e))
        self.root.bind('<Delete>', lambda e: self.delete_key())
        #entry binds
        self.entry_index.bind("<Button-1>", lambda e: self.enable_entry())
        self.entry_index.bind("<Return>", lambda e: self.return_key2photo_number(e))
        ################## Initially, disable the entry widget
        self.entry_index.config(state="disabled")
