# Changelog

## Version 1.1.0 26-07-2026
- Use Zenity for GUI file/folder pickers when available.
- Add GUI buttons for Open Image, Open Folder, and Open Non-Recursive.
- Keep file, recursive folder, and non-recursive folder picture-roll behavior available from the GUI.
- Expand CLI help with detailed usage, picker behavior, shortcuts, and notes.

## Version 1.0.0 28-06-2026
- Add image zoom controls with Ctrl+plus, Ctrl+minus, Ctrl+0 reset view shortcuts.
- Add Ctrl+mouse-wheel zoom and Ctrl+middle-click reset view.
- Add Ctrl+left-mouse drag panning for zoomed images.
- Add mouse-wheel vertical scrolling, middle-button vertical drag scrolling, and horizontal tilt-wheel scrolling.
- Keep canvas background matched to the GUI instead of black.
- Fit normal view to the actual canvas area above the bottom controls without changing aspect ratio.
- Add `~/.config/auraview/settings.json` with dark/light theme and GUI font settings.
- Open an empty app when launched without arguments instead of scanning the current directory.
- Keep file input as a folder picture roll and add `--non-recursive` for folder-only directory rolls.
- Use Zenity for GUI file/folder pickers when available, falling back to Tk dialogs.
- Add scrollable image canvas for zoomed images.

## Version 0.7.0 28-03-2026
- bugfix on --logfile mode
## Version 0.6.0 24-02-2026
- Natural sort feature added.
- Transfer dev workflow to pure uv.
- Rotate image based on exif tags to avoid pixel conversion.
## Version 0.5.0 23-02-2026
- Bug on file input.
## Version 0.4.0 23-02-2026
- removed recursive selection of all images while using file as input.
## Version 0.3.0 23-02-2026
- added additional requirement to pyproject.toml
## Version 0.2.0 23-02-2026
- Added image counter
- Added go to image index feature
- added copy, move, Delete, Rotate
- Update extension feature.
- Datetime labels
## Version 0.1.0 - 19-02-2026
- Initial release
- Able to view photos.
- supports apple image extensions.
- Navigation supported.
- Image transform: Rotation possible.
- Rotations are considered inplace.
- Copy and Move functions available.
