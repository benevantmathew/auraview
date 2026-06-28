# AuraView
a minimal, elegant image viewer inspired by the art of melody.

---

## ✨ About

AuraView is a minimalist photo viewer designed to stay out of your way.
No clutter. No unnecessary controls. Just your images — fast and clear.

It focuses on:

- ⚡ Speed
- 🧼 Clean interface
- 🖼️ Smooth image viewing
- 🪶 Lightweight footprint

---

## 🐍 Requirements

- Python 3.14.2 (Tested)
- pandas
- pillow
- pillow_heif

---

## 🚀 Features

- View photos smoothly and instantly
- Supports Apple image formats (including HEIF/HEIC)
- Keyboard-based image navigation
- User settings at `~/.config/auraview/settings.json`
- Dark/light theme and configurable GUI font
- Image zoom with reset view shortcuts and Ctrl + mouse wheel
- Ctrl + left-mouse drag panning for zoomed images
- Mouse wheel, middle-button drag, and horizontal tilt-wheel canvas scrolling
- Image rotation support
- In-place rotation (changes persist)
- Copy images to another location
- Move images between directories
- Directory input loads images recursively by default; use `--non-recursive` to only load that folder

---

## 📦 Installation

Install AuraView using pip:

```bash
pip install auraview
```

## 🖥️ Usage

Launch AuraView:

```bash
auraview
````

Launching without arguments opens an empty viewer. It no longer scans the current directory automatically.

Open a specific directory recursively:

```bash
auraview /path/to/folder
```

Open only images directly inside a directory:

```bash
auraview /path/to/folder --non-recursive
```

Open a specific image file:

```bash
auraview /path/to/image.jpg
```

---

### 📌 Command Line Options

Show version:

```bash
auraview --version
auraview -v
```

Show help:

```bash
auraview --help
auraview -h
```

Show author:

```bash
auraview --author
auraview -a
```

Show author email:

```bash
auraview --email
auraview -e
```

Show release date:

```bash
auraview --date
auraview -d
```

### ⚙️ GUI Settings

AuraView creates and reads user settings from:

```bash
~/.config/auraview/settings.json
```

Example:

```json
{
    "ui": {
        "font_family": "Arial",
        "font_size": 12,
        "tk_scaling": 1.0,
        "window_width": 900,
        "window_height": 700,
        "theme": "dark"
    }
}
```

Supported themes are `dark` and `light`. You can also temporarily override these at launch:

```bash
auraview --theme light --font_family "DejaVu Sans" --font_size 13 --tk_scaling 1.1
```
