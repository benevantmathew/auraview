"""
help.py

Author: Benevant Mathew
Date: 2026-02-19
"""
import sys


def print_help():
    """Print detailed AuraView command-line help."""
    help_message = """
AuraView - fast personal photo viewer

Usage:
    auraview [OPTIONS] [PATH]

PATH:
    No PATH
        Open an empty AuraView window. The current directory is not scanned.

    Image file path
        Open that image first and build the picture roll from the other images
        directly inside the same folder.

        Example:
            auraview /home/me/Pictures/trip/photo_001.jpg

    Folder path
        Open a picture roll from that folder. By default this scans the folder
        recursively, including images from all subfolders.

        Example:
            auraview /home/me/Pictures/trip

    Log file
        Use --logfile with a text file containing one full image path per line.

        Example:
            auraview --logfile /tmp/images.txt

Image collection:
    Default folder behavior is recursive.

    auraview /pictures
        Collect images from /pictures and all subfolders.

    auraview /pictures --non-recursive
        Collect only images directly inside /pictures.

    auraview /pictures/photo.jpg
        Open photo.jpg and keep sibling images from /pictures in the picture roll.

Supported image extensions:
    .png, .jpg, .jpeg, .heic

Options:
    -h, --help
        Show this help message and exit.

    -v, --version
        Show AuraView version and exit.

    -a, --author
        Show author name and exit.

    -e, --email
        Show author email and exit.

    -d, --date
        Show release date and exit.

    --logfile FILE
        Load image paths from FILE. FILE must contain one image path per line.
        Blank lines are ignored.

    --non-recursive
        For folder input only, collect images directly inside that folder and
        skip subfolders.

Theme and font options:
    AuraView reads persistent GUI settings from:
        ~/.config/auraview/settings.json

    --theme {dark,light}
        Temporarily override the configured theme for this run.

    --font_family FONT
        Temporarily override the configured GUI font family for this run.

    --font_size SIZE
        Temporarily override the configured GUI font size for this run.

    --tk_scaling SCALE
    --zoom SCALE
        Temporarily override Tk scaling for this run. Useful for high-DPI
        displays or large monitors.

Examples:
    auraview
        Open an empty viewer window.

    auraview ~/Pictures
        Open ~/Pictures recursively.

    auraview ~/Pictures --non-recursive
        Open only images directly inside ~/Pictures.

    auraview ~/Pictures/photo.jpg
        Open photo.jpg and use its folder as the picture roll.

    auraview --theme light --font_family "DejaVu Sans" --font_size 13
        Open with temporary light theme and font overrides.

Keyboard shortcuts:
    Right Arrow              Next image
    Left Arrow               Previous image
    Home                     First image
    End                      Last image
    Delete                   Delete current image to trash when photo number box is inactive
    Escape                   Exit AuraView
    k                        Rotate current image left
    l                        Rotate current image right
    q                        Quick move current image to selected quick folder
    m                        Choose folder and move current image

Zoom and canvas shortcuts:
    Ctrl + +                 Zoom in
    Ctrl + =                 Zoom in
    Ctrl + -                 Zoom out
    Ctrl + 0                 Reset image to fitted view
    Ctrl + MouseWheel        Zoom in/out
    Ctrl + Middle Click      Reset image to fitted view
    Ctrl + Left Drag         Pan zoomed image
    MouseWheel               Vertical scroll
    Middle Button Drag       Vertical scroll
    Horizontal Wheel         Horizontal scroll
    Shift + MouseWheel       Horizontal scroll fallback

Notes:
    - Rotate operations modify the current image in place.
    - Move/delete operations update the current picture roll after the file action.
    - Settings edits are persistent only when made in ~/.config/auraview/settings.json;
      command-line theme/font/scaling flags affect only the current run.
"""
    print(help_message.strip())
    sys.exit(0)
