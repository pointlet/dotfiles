"""Qtile configuration - Main assembly file.

This file imports all dependencies and injects them into configuration modules.
Only shared variables are configured here. Module-specific configuration
should be edited in the respective module files.
"""

# Qtile imports - all dependencies are imported here
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from pathlib import Path

# Configuration modules
from screen_layout import ScreenConfig, BarPosition
from layout_config import create_layouts
from workspaces import create_groups
from widgets_config import create_widgets
from bars import create_screens
from key_bindings import create_key_bindings
from mouse_bindings import create_mouse_config
from theme import (
    WALLPAPER_PATH,
    WALLPAPER_MODE,
    BAR_HEIGHT,
    BORDER_WIDTH,
    OUTER_GAP,
    INNER_GAP,
)
import subprocess

# ============================================================================
# SHARED CONFIGURATION - Variables used across multiple modules
# ============================================================================

# Modifier key - used by key_bindings and mouse_bindings
MOD_KEY = "mod1"  # Left Alt 

# Terminal - used by key_bindings
TERMINAL = "alacritty"

# Screen configuration - used by all modules
SCREEN = ScreenConfig(
    screen_width=1920,
    screen_height=1080,
    bar_height=BAR_HEIGHT,
    bar_position=BarPosition.TOP,
    border_width=BORDER_WIDTH,
    outer_gap=OUTER_GAP,
    inner_gap=INNER_GAP, # Even number so they split evenly between windows
)


# ============================================================================
# MODULE-SPECIFIC CONFIGURATION
# ============================================================================
# To customize:
# - Layouts: edit layout_config.py
# - Workspaces: edit workspaces.py
# - Widgets: edit widgets_config.py
# - Bar/screens: edit bars.py
# - Key bindings: edit key_bindings.py
# - Mouse bindings: edit mouse_bindings.py


# ============================================================================
# CONFIGURATION ASSEMBLY - Dependencies are injected from here
# ============================================================================

# Workspaces
groups = create_groups(Group)

# Widgets and screens/bar
widget_defaults, bar_widgets = create_widgets(widget_module=widget, lazy_module=lazy)

screens = create_screens(
    screen_class=Screen,
    bar_class=bar.Bar,
    screen_config=SCREEN,
    bar_widgets=bar_widgets,
    wallpaper_path=WALLPAPER_PATH,
    wallpaper_mode=WALLPAPER_MODE,
)

extension_defaults = widget_defaults.copy()

# Create key bindings
keys = create_key_bindings(
    key_class=Key,
    lazy_module=lazy,
    mod_key=MOD_KEY,
    terminal=TERMINAL,
    screen_config=SCREEN,
    groups=groups,
)

# Create mouse bindings
mouse = create_mouse_config(
    drag_class=Drag,
    click_class=Click,
    lazy_module=lazy,
    mod_key=MOD_KEY,
    screen_config=SCREEN,
)

# Create layouts
layouts, floating_layout = create_layouts(
    layout_module=layout,
    match_class=Match,
    screen_config=SCREEN,
)


# ============================================================================
# Hooks
# ============================================================================
@hook.subscribe.startup
def _autostart():
    subprocess.Popen(["/home/pointlet/dotfiles/.config/qtile/autostart.sh"])

@hook.subscribe.client_focus
def raise_focused_window(window):
    """Raises the newly focused window."""
    window.bring_to_front()


@hook.subscribe.client_new
def float_and_center(window):
    """Float and center new windows."""
    if not window.floating:
        window.floating = True
        window.center()
    window.bring_to_front()


# ============================================================================
# QTILE SETTINGS
# ============================================================================

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = False
floats_kept_above = True
bring_front_click = True
cursor_warp = True
auto_fullscreen = True
focus_on_window_activation = "always"
reconfigure_screens = True
auto_minimize = True
wmname = "LG3D"

# Wayland-specific settings
wl_input_rules = {
    "type:touchpad": {
        "tap": True,
        "natural_scroll": True,
        "dwt": True,
    },
    "type:keyboard": {
        "kb_repeat_rate": 50,
        "kb_repeat_delay": 300,
    },
}

wl_xcursor_theme = None
wl_xcursor_size = 24
