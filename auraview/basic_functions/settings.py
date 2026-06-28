"""
auraview/basic_functions/settings.py

Load user-editable UI settings from ~/.config/auraview/settings.json.
"""
import json
import os
import shutil

DEFAULT_UI_SETTINGS = {
    "font_family": "Arial",
    "font_size": 12,
    "tk_scaling": 1.0,
    "window_width": 900,
    "window_height": 700,
    "theme": "dark",
}

THEME_COLORS = {
    "dark": {
        "background_color": "#1e1e1e",
        "foreground_color": "#f2f2f2",
        "input_background_color": "#2d2d2d",
        "input_foreground_color": "#ffffff",
        "button_background_color": "#3a3a3a",
        "button_foreground_color": "#ffffff",
        "canvas_background_color": "#1e1e1e",
        "scrollbar_background_color": "#2d2d2d",
    },
    "light": {
        "background_color": "#f4f4f5",
        "foreground_color": "#111827",
        "input_background_color": "#ffffff",
        "input_foreground_color": "#111827",
        "button_background_color": "#e5e7eb",
        "button_foreground_color": "#111827",
        "canvas_background_color": "#f4f4f5",
        "scrollbar_background_color": "#e5e7eb",
    },
}

COLOR_KEYS = tuple(next(iter(THEME_COLORS.values())).keys())
APP_NAME = "auraview"
SETTINGS_FILENAME = "settings.json"


def get_user_settings_dir():
    """Return ~/.config/auraview, honoring HOME for tests and XDG-style use."""
    return os.path.join(os.path.expanduser("~"), ".config", APP_NAME)


def get_user_settings_path():
    """Return the user settings.json path."""
    return os.path.join(get_user_settings_dir(), SETTINGS_FILENAME)


def get_factory_settings_path():
    """Return the bundled default settings.json path."""
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "application", SETTINGS_FILENAME)
    )


def ensure_user_settings_file():
    """Create ~/.config/auraview/settings.json from bundled defaults if missing."""
    settings_dir = get_user_settings_dir()
    settings_path = get_user_settings_path()
    os.makedirs(settings_dir, exist_ok=True)

    if os.path.exists(settings_path):
        return settings_path

    factory_path = get_factory_settings_path()
    if os.path.exists(factory_path):
        shutil.copy2(factory_path, settings_path)
    else:
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump({"ui": DEFAULT_UI_SETTINGS}, f, indent=4)

    return settings_path


def _positive_int(value, default_value):
    """Convert config values to positive int with fallback."""
    try:
        int_value = int(value)
    except (TypeError, ValueError):
        return default_value
    return int_value if int_value > 0 else default_value


def _positive_float(value, default_value):
    """Convert config values to positive float with fallback."""
    try:
        float_value = float(value)
    except (TypeError, ValueError):
        return default_value
    return float_value if float_value > 0 else default_value


def _normalize_theme(value):
    """Normalize theme name with dark fallback."""
    theme = str(value or DEFAULT_UI_SETTINGS["theme"]).strip().lower()
    return theme if theme in THEME_COLORS else DEFAULT_UI_SETTINGS["theme"]


def load_ui_settings(settings_filepath=None, overrides=None):
    """Load UI settings from settings.json and apply optional overrides."""
    settings_filepath = settings_filepath or ensure_user_settings_file()

    try:
        with open(settings_filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        data = {}

    file_settings = {}
    if isinstance(data, dict) and isinstance(data.get("ui"), dict):
        file_settings = data["ui"]

    theme = _normalize_theme(file_settings.get("theme", DEFAULT_UI_SETTINGS["theme"]))
    if overrides and overrides.get("theme") is not None:
        theme = _normalize_theme(overrides["theme"])

    settings = DEFAULT_UI_SETTINGS.copy()
    settings.update(THEME_COLORS[theme])
    settings.update(file_settings)

    for key, value in (overrides or {}).items():
        if value is not None:
            settings[key] = value

    settings["theme"] = _normalize_theme(settings.get("theme"))
    if settings["theme"] != theme:
        explicit_colors = {
            key: settings[key]
            for key in COLOR_KEYS
            if key in file_settings or (overrides or {}).get(key) is not None
        }
        settings.update(THEME_COLORS[settings["theme"]])
        settings.update(explicit_colors)

    settings["font_family"] = str(
        settings.get("font_family") or DEFAULT_UI_SETTINGS["font_family"]
    )
    settings["font_size"] = _positive_int(
        settings.get("font_size"),
        DEFAULT_UI_SETTINGS["font_size"]
    )
    settings["window_width"] = _positive_int(
        settings.get("window_width"),
        DEFAULT_UI_SETTINGS["window_width"]
    )
    settings["window_height"] = _positive_int(
        settings.get("window_height"),
        DEFAULT_UI_SETTINGS["window_height"]
    )
    settings["tk_scaling"] = _positive_float(
        settings.get("tk_scaling"),
        DEFAULT_UI_SETTINGS["tk_scaling"]
    )

    for key in COLOR_KEYS:
        settings[key] = str(settings.get(key) or THEME_COLORS[settings["theme"]][key])

    return settings
