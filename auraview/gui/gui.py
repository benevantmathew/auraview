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

from auraview.version import __version__
from auraview.core.image_controller import ImageController
from auraview.basic_functions.settings import load_ui_settings

# Register HEIF opener
register_heif_opener()

ZOOM_STEP = 1.25
MIN_ZOOM = 0.1
MAX_ZOOM = 8.0

class PhotoViewerGUI:
    """
    The main GUI
    """
    def __init__(
            self,
            files=None,
            loc='.',
            ui_options=None,
            recursive=True
        ):
        self.files = files
        self.ui_settings = load_ui_settings(overrides=ui_options)
        self.gui_font = (
            self.ui_settings["font_family"],
            self.ui_settings["font_size"]
        )

        self.controller = ImageController(self.files, loc, recursive=recursive)

        self.img_obj = None
        self.canvas_image_ref = None
        self.zoom = 1.0
        self.middle_scroll_x = 0

        # TEMP SIZE so window appears
        self.width = 500
        self.height = 500
        self.display_height = self.height

        self.root = tk.Tk()
        self.root.tk.call("tk", "scaling", self.ui_settings["tk_scaling"])
        self.root.geometry(
            f'{self.ui_settings["window_width"]}x{self.ui_settings["window_height"]}'
        )
        self.selected_option = tk.StringVar(self.root)
        self.date_var = tk.StringVar()

        self.root.update_idletasks()  # important under Wayland

        self.root.title(f"AuraView-{__version__}")
        self.root.resizable(True, True)

        self._create_widgets()
        self._apply_theme()
        self._bind_keys()

        self.update_screen()

        self.root.bind("<Configure>", self._on_resize)

    def run(self):
        """
        Docstring for run

        :param self: Description
        """
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

        # Allow Tk grid geometry to settle before fitting to canvas.
        self.root.after_idle(self.update_screen)

    def _get_canvas_size(self):
        """Return the actual drawable canvas size for image fitting."""
        canvas_width = self.canvas_img.winfo_width()
        canvas_height = self.canvas_img.winfo_height()

        if canvas_width <= 1:
            canvas_width = self.width
        if canvas_height <= 1:
            canvas_height = self.display_height

        return max(canvas_width, 1), max(canvas_height, 1)

    def _show_empty_state(self):
        """Show an empty app state when no image is loaded."""
        self.canvas_img.delete("all")
        canvas_width, canvas_height = self._get_canvas_size()
        self.canvas_img.config(scrollregion=(0, 0, canvas_width, canvas_height))
        self.label_zoom.config(text="Zoom: 100%")
        self.label_counter.config(text="0/0")

        for label in [
                self.label_name,
                self.label_size,
                self.label_dimensions,
                self.label_image_dpi,
                self.label_move_copy_dir,
                self.label_image_ext,
                self.label_image_datetimeoriginal,
                self.label_image_datetimedigitized,
                self.label_image_datetime,
                self.label_image_filecreationtime,
                self.label_image_dir,
            ]:
            label.config(text="")

        for button in [self.button_back, self.button_forward]:
            button.config(state=tk.DISABLED)

        self.canvas_img.create_text(
            canvas_width // 2,
            canvas_height // 2,
            text="Open an image file or folder to start",
            fill=self.ui_settings["foreground_color"],
            font=self.gui_font,
            anchor="center"
        )

    # -------------------------------------------------
    # Screen Update
    # -------------------------------------------------
    def update_screen(self):
        """
        Docstring for update_screen

        :param self: Description
        """

        canvas_width, canvas_height = self._get_canvas_size()

        img = self.controller.get_resized_image(
            canvas_width,
            canvas_height,
            zoom=self.zoom
        )
        if not img:
            self._show_empty_state()
            return

        self.img_obj = ImageTk.PhotoImage(img)
        self.canvas_img.delete("all")

        image_width = self.img_obj.width()
        image_height = self.img_obj.height()
        x_offset = max((canvas_width - image_width) // 2, 0)
        y_offset = max((canvas_height - image_height) // 2, 0)

        self.canvas_img.create_image(
            x_offset,
            y_offset,
            image=self.img_obj,
            anchor="nw"
        )
        self.canvas_image_ref = self.img_obj # prevent Garbage collection
        self.canvas_img.config(
            scrollregion=(
                0,
                0,
                max(image_width, canvas_width),
                max(image_height, canvas_height)
            )
        )
        self.label_zoom.config(text=f"Zoom: {int(self.zoom * 100)}%")

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

        self.reset_view(update=False)
        self.update_screen()

    def zoom_image(self, direction):
        """Zoom the current image in or out."""
        if direction == "in":
            self.zoom = min(MAX_ZOOM, self.zoom * ZOOM_STEP)
        elif direction == "out":
            self.zoom = max(MIN_ZOOM, self.zoom / ZOOM_STEP)
        else:
            return

        self.update_screen()

    def reset_view(self, update=True):
        """Reset the current image to fit the viewer area."""
        self.zoom = 1.0
        if update:
            self.update_screen()

    def start_pan(self, event):
        """Start Ctrl + left-mouse panning for zoomed images."""
        if self.zoom <= 1.0:
            return "break"

        self.canvas_img.scan_mark(event.x, event.y)
        self.canvas_img.config(cursor="fleur")
        return "break"

    def pan_image(self, event):
        """Pan the zoomed image while Ctrl + left mouse is dragged."""
        if self.zoom <= 1.0:
            return "break"

        self.canvas_img.scan_dragto(event.x, event.y, gain=1)
        return "break"

    def end_pan(self, event):
        """Restore the pointer after Ctrl + left-mouse panning."""
        self.canvas_img.config(cursor="")
        return "break"

    def zoom_with_mouse_wheel(self, event):
        """Zoom with Ctrl + mouse wheel on Windows/macOS and Linux."""
        if getattr(event, "num", None) == 4 or getattr(event, "delta", 0) > 0:
            self.zoom_image("in")
        elif getattr(event, "num", None) == 5 or getattr(event, "delta", 0) < 0:
            self.zoom_image("out")

        return "break"

    def reset_view_from_mouse(self, event):
        """Reset zoom with Ctrl + middle mouse button."""
        self.reset_view()
        return "break"

    def scroll_vertical_with_mouse(self, event):
        """Scroll the image canvas vertically with the mouse wheel."""
        if getattr(event, "num", None) == 4 or getattr(event, "delta", 0) > 0:
            units = -3
        else:
            units = 3

        self.canvas_img.yview_scroll(units, "units")
        return "break"

    def scroll_horizontal_with_mouse(self, event):
        """Scroll the image canvas horizontally with tilt/shift mouse wheel."""
        if getattr(event, "num", None) == 6 or getattr(event, "delta", 0) > 0:
            units = -3
        else:
            units = 3

        self.canvas_img.xview_scroll(units, "units")
        return "break"

    def start_middle_vertical_scroll(self, event):
        """Start middle-button drag scrolling constrained to vertical movement."""
        self.middle_scroll_x = event.x
        self.canvas_img.scan_mark(event.x, event.y)
        self.canvas_img.config(cursor="sb_v_double_arrow")
        return "break"

    def middle_vertical_scroll(self, event):
        """Scroll vertically while the middle mouse button is dragged."""
        self.canvas_img.scan_dragto(self.middle_scroll_x, event.y, gain=1)
        return "break"

    def end_middle_vertical_scroll(self, event):
        """Restore the pointer after middle-button vertical scrolling."""
        self.canvas_img.config(cursor="")
        return "break"

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
        self.reset_view(update=False)
        self.update_screen()

    def end_button(self):
        """
        Docstring for end_button
        """
        self.controller.end()
        self.reset_view(update=False)
        self.update_screen()

    def _apply_theme(self):
        """Apply configured theme colors and font to all Tk widgets."""
        self.root.configure(background=self.ui_settings["background_color"])

        def apply_to_widget(widget):
            common_options = {}
            if isinstance(widget, (tk.Frame, tk.LabelFrame)):
                common_options["background"] = self.ui_settings["background_color"]
            if isinstance(widget, tk.LabelFrame):
                common_options["foreground"] = self.ui_settings["foreground_color"]
                common_options["font"] = self.gui_font
            elif isinstance(widget, tk.Label):
                common_options.update({
                    "background": self.ui_settings["background_color"],
                    "foreground": self.ui_settings["foreground_color"],
                    "font": self.gui_font,
                })
            elif isinstance(widget, tk.Button):
                common_options.update({
                    "background": self.ui_settings["button_background_color"],
                    "foreground": self.ui_settings["button_foreground_color"],
                    "activebackground": self.ui_settings["canvas_background_color"],
                    "activeforeground": self.ui_settings["foreground_color"],
                    "font": self.gui_font,
                })
            elif isinstance(widget, tk.Entry):
                common_options.update({
                    "background": self.ui_settings["input_background_color"],
                    "foreground": self.ui_settings["input_foreground_color"],
                    "insertbackground": self.ui_settings["input_foreground_color"],
                    "font": self.gui_font,
                })
            elif isinstance(widget, tk.Canvas):
                common_options["background"] = self.ui_settings["canvas_background_color"]
            elif isinstance(widget, tk.Scrollbar):
                common_options.update({
                    "background": self.ui_settings["scrollbar_background_color"],
                    "troughcolor": self.ui_settings["background_color"],
                    "activebackground": self.ui_settings["button_background_color"],
                })

            if common_options:
                try:
                    widget.configure(**common_options)
                except tk.TclError:
                    pass

            for child in widget.winfo_children():
                apply_to_widget(child)

        apply_to_widget(self.root)

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
        gui_bg = self.ui_settings["canvas_background_color"]
        self.image_frame = tk.Frame(self.main_frame, background=gui_bg)
        self.image_frame.grid(row=1, column=0, columnspan=6, sticky="nsew")
        self.image_frame.grid_rowconfigure(0, weight=1)
        self.image_frame.grid_columnconfigure(0, weight=1)

        self.canvas_img = tk.Canvas(
            self.image_frame,
            highlightthickness=0,
            background=gui_bg
        )
        self.canvas_img.grid(row=0, column=0, sticky="nsew")

        self.scrollbar_y = tk.Scrollbar(
            self.image_frame,
            orient="vertical",
            command=self.canvas_img.yview
        )
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")

        self.scrollbar_x = tk.Scrollbar(
            self.image_frame,
            orient="horizontal",
            command=self.canvas_img.xview
        )
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")

        self.canvas_img.configure(
            xscrollcommand=self.scrollbar_x.set,
            yscrollcommand=self.scrollbar_y.set
        )
        self.canvas_img.bind('<Control-ButtonPress-1>', self.start_pan)
        self.canvas_img.bind('<Control-B1-Motion>', self.pan_image)
        self.canvas_img.bind('<Control-ButtonRelease-1>', self.end_pan)
        self.canvas_img.bind('<Control-MouseWheel>', self.zoom_with_mouse_wheel)
        self.canvas_img.bind('<Control-Button-4>', self.zoom_with_mouse_wheel)
        self.canvas_img.bind('<Control-Button-5>', self.zoom_with_mouse_wheel)
        self.canvas_img.bind('<Control-Button-2>', self.reset_view_from_mouse)
        self.canvas_img.bind('<MouseWheel>', self.scroll_vertical_with_mouse)
        self.canvas_img.bind('<Button-4>', self.scroll_vertical_with_mouse)
        self.canvas_img.bind('<Button-5>', self.scroll_vertical_with_mouse)
        self.canvas_img.bind('<Shift-MouseWheel>', self.scroll_horizontal_with_mouse)
        self.canvas_img.bind('<Button-6>', self.scroll_horizontal_with_mouse)
        self.canvas_img.bind('<Button-7>', self.scroll_horizontal_with_mouse)
        self.canvas_img.bind('<ButtonPress-2>', self.start_middle_vertical_scroll)
        self.canvas_img.bind('<B2-Motion>', self.middle_vertical_scroll)
        self.canvas_img.bind('<ButtonRelease-2>', self.end_middle_vertical_scroll)

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

        self.button_zoom_out = tk.Button(
            self.main_frame,
            text="Zoom -",
            command=lambda: self.zoom_image('out'),
            width=20
        )
        self.button_zoom_out.grid(row=8, column=2)

        self.button_zoom_in = tk.Button(
            self.main_frame,
            text="Zoom +",
            command=lambda: self.zoom_image('in'),
            width=20
        )
        self.button_zoom_in.grid(row=8, column=3)

        button_update_ext=tk.Button(
            self.main_frame,
            text="Update Ext",
            command=self.update_extension,
            width=20
        )
        button_update_ext.grid(row=8, column=4)

        self.button_reset_view = tk.Button(
            self.main_frame,
            text="Reset View",
            command=self.reset_view,
            width=20
        )
        self.button_reset_view.grid(row=8, column=5)

        ## row 9
        self.label_zoom = tk.Label(self.main_frame)
        self.label_zoom.grid(row=9, column=0)

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
        self.reset_view(update=False)
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
        self.root.bind('<Control-plus>', lambda e: self.zoom_image('in'))
        self.root.bind('<Control-equal>', lambda e: self.zoom_image('in'))
        self.root.bind('<Control-KP_Add>', lambda e: self.zoom_image('in'))
        self.root.bind('<Control-minus>', lambda e: self.zoom_image('out'))
        self.root.bind('<Control-KP_Subtract>', lambda e: self.zoom_image('out'))
        self.root.bind('<Control-0>', lambda e: self.reset_view())
        self.root.bind('<Control-KP_0>', lambda e: self.reset_view())
        #entry binds
        self.entry_index.bind("<Button-1>", lambda e: self.enable_entry())
        self.entry_index.bind("<Return>", lambda e: self.return_key2photo_number(e))
        ################## Initially, disable the entry widget
        self.entry_index.config(state="disabled")
