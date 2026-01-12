"""Keyboard bindings configuration for Qtile."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any, Callable, List, Sequence

from screen_layout import ScreenConfig


# ============================================================================
# KEY BINDINGS CONFIGURATION
# ============================================================================

MOVEMENT_INCREMENT = 320  # Pixels to move/resize per keypress
SMALL_WINDOW_SIZE = (800, 600)
NORMAL_WINDOW_SIZE = (1200, 800)
APP_LAUNCHER = f"rofi -config {Path.home()/ 'dotfiles' / '.config' / 'rofi' / 'config.rasi'} -show drun"
MENU_LAUNCHER = "dmenu_run"
ALTERNATIVE_MOD = "mod4"
THEMEGEN = Path.home() / ".config/themegen/render.py"


def run_and_refresh_widget(cmd: Sequence[str], widget_name: str) -> Callable[[Any], None]:
    """Run a command and trigger an immediate widget refresh."""

    def _inner(qtile):
        subprocess.run(cmd, check=False)
        widget = qtile.widgets_map.get(widget_name)
        if not widget:
            return

        # Prefer built-in refresh hooks; fall back to polling if needed.
        if hasattr(widget, "force_update"):
            widget.force_update()
        elif hasattr(widget, "poll"):
            widget.poll()
        elif hasattr(widget, "cmd_poll"):
            widget.cmd_poll()

        # Schedule another tick on the event loop to catch async volume changes.
        qtile.call_later(0, getattr(widget, "poll", getattr(widget, "cmd_poll", None)))

    return _inner


# ============================================================================
# IMPLEMENTATION
# ============================================================================


class KeyBindings:
    """Configure keyboard shortcuts for window management."""

    def __init__(
        self,
        key_class: Any,
        lazy_module: Any,
        mod_key: str,
        terminal: str,
        screen_config: ScreenConfig,
    ) -> None:
        self.Key = key_class
        self.lazy = lazy_module
        self.mod = mod_key
        self.terminal = terminal
        self.screen = screen_config

    def get_all_bindings(self) -> List:
        return (
            self._window_focus_cycle()
            + self._window_movement()
            + self._window_preview()
            + self._window_resizing()
            + self._window_snapping()
            + self._window_corners()
            + self._window_preset_sizes()
            + self._window_management()
            + self._launcher_bindings()
            + self._qtile_controls()
            + self._vt_switching()
            + self._volume_control()
        )

    def _window_focus_cycle(self) -> List:
        def focus_next_and_warp(qtile):
            group = qtile.current_group
            group.next_window()
            win = qtile.current_window
            if win:
                qtile.core.warp_pointer(win.x + win.width // 2, win.y + win.height // 2)

        def focus_prev_and_warp(qtile):
            group = qtile.current_group
            group.prev_window()
            win = qtile.current_window
            if win:
                qtile.core.warp_pointer(win.x + win.width // 2, win.y + win.height // 2)

        return [
            self.Key([self.mod], "Tab", self.lazy.function(focus_next_and_warp), desc="Focus next window"),
            self.Key([self.mod, "shift"], "Tab", self.lazy.function(focus_prev_and_warp), desc="Focus previous window"),
        ]

    def _window_movement(self) -> List:
        return [
            self.Key([self.mod], "h", self.lazy.window.move_floating(-MOVEMENT_INCREMENT, 0), desc="Move window left"),
            self.Key([self.mod], "l", self.lazy.window.move_floating(MOVEMENT_INCREMENT, 0), desc="Move window right"),
            self.Key([self.mod], "k", self.lazy.window.move_floating(0, -MOVEMENT_INCREMENT), desc="Move window up"),
            self.Key([self.mod], "j", self.lazy.window.move_floating(0, MOVEMENT_INCREMENT), desc="Move window down"),
        ]

    def _window_resizing(self) -> List:
        return [
            self.Key([self.mod, "control"], "h", self.lazy.window.resize_floating(-MOVEMENT_INCREMENT, 0), desc="Shrink width"),
            self.Key([self.mod, "control"], "l", self.lazy.window.resize_floating(MOVEMENT_INCREMENT, 0), desc="Grow width"),
            self.Key([self.mod, "control"], "k", self.lazy.window.resize_floating(0, -MOVEMENT_INCREMENT), desc="Shrink height"),
            self.Key([self.mod, "control"], "j", self.lazy.window.resize_floating(0, MOVEMENT_INCREMENT), desc="Grow height"),
        ]

    def _window_snapping(self) -> List:
        return [
            self.Key([self.mod, "shift"], "h",
                self.lazy.window.set_position_floating(*self.screen.get_left_half()[:2]),
                self.lazy.window.set_size_floating(*self.screen.get_left_half()[2:]),
                desc="Snap to left half"),
            self.Key([self.mod, "shift"], "l",
                self.lazy.window.set_position_floating(*self.screen.get_right_half()[:2]),
                self.lazy.window.set_size_floating(*self.screen.get_right_half()[2:]),
                desc="Snap to right half"),
            self.Key([self.mod, "shift"], "k",
                self.lazy.window.set_position_floating(*self.screen.get_top_half()[:2]),
                self.lazy.window.set_size_floating(*self.screen.get_top_half()[2:]),
                desc="Snap to top half"),
            self.Key([self.mod, "shift"], "j",
                self.lazy.window.set_position_floating(*self.screen.get_bottom_half()[:2]),
                self.lazy.window.set_size_floating(*self.screen.get_bottom_half()[2:]),
                desc="Snap to bottom half"),
        ]

    def _window_corners(self) -> List:
        return [
            self.Key([self.mod, ALTERNATIVE_MOD], "h",
                self.lazy.window.set_position_floating(*self.screen.get_top_left_quarter()[:2]),
                self.lazy.window.set_size_floating(*self.screen.get_top_left_quarter()[2:]),
                desc="Snap to top-left corner"),
            self.Key([self.mod, ALTERNATIVE_MOD], "l",
                self.lazy.window.set_position_floating(*self.screen.get_top_right_quarter()[:2]),
                self.lazy.window.set_size_floating(*self.screen.get_top_right_quarter()[2:]),
                desc="Snap to top-right corner"),
            self.Key([self.mod, ALTERNATIVE_MOD], "j",
                self.lazy.window.set_position_floating(*self.screen.get_bottom_left_quarter()[:2]),
                self.lazy.window.set_size_floating(*self.screen.get_bottom_left_quarter()[2:]),
                desc="Snap to bottom-left corner"),
            self.Key([self.mod, ALTERNATIVE_MOD], "k",
                self.lazy.window.set_position_floating(*self.screen.get_bottom_right_quarter()[:2]),
                self.lazy.window.set_size_floating(*self.screen.get_bottom_right_quarter()[2:]),
                desc="Snap to bottom-right corner"),
            self.Key([self.mod, ALTERNATIVE_MOD], "m", self.lazy.window.center(), desc="Center window"),
        ]

    def _window_preset_sizes(self) -> List:
        return [
            self.Key([self.mod, ALTERNATIVE_MOD], "f",
                self.lazy.window.set_size_floating(*self.screen.get_full_screen()[2:]),
                desc="Full screen size"),
            self.Key([self.mod, ALTERNATIVE_MOD], "s",
                self.lazy.window.set_size_floating(*SMALL_WINDOW_SIZE),
                desc="Small size"),
            self.Key([self.mod, ALTERNATIVE_MOD], "n",
                self.lazy.window.set_size_floating(*NORMAL_WINDOW_SIZE),
                desc="Normal size"),
        ]

    def _window_management(self) -> List:
        return [
            self.Key([self.mod], "q", self.lazy.window.kill(), desc="Kill window"),
            self.Key([self.mod], "t", self.lazy.window.toggle_floating(), desc="Toggle floating"),
            self.Key([self.mod], "f", self.lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
            self.Key([self.mod, "shift"], "Return",
                self.lazy.window.set_position_floating(*self.screen.get_full_screen()[:2]),
                self.lazy.window.set_size_floating(*self.screen.get_full_screen()[2:]),
                desc="Maximize window (respecting bar)"),
        ]

    def _window_preview(self) -> List:
        return [
            self.Key([ALTERNATIVE_MOD], "Tab", self.lazy.spawn("rofi -show window"), desc="Launch rofi window switcher"),
        ]

    def _launcher_bindings(self) -> List:
        return [
            self.Key([self.mod], "Return", self.lazy.spawn(self.terminal), desc="Launch terminal"),
            self.Key([self.mod], "space", self.lazy.spawn(APP_LAUNCHER), desc="Launch application launcher"),
            self.Key([self.mod], "d", self.lazy.spawn(MENU_LAUNCHER), desc="Launch menu launcher"),
            self.Key([ALTERNATIVE_MOD], "r", self.lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
        ]

    def _qtile_controls(self) -> List:
        def regenerate_and_reload(qtile):
            subprocess.run(["python3", str(THEMEGEN)], check=False)
            qtile.reload_config()

        return [
            self.Key([self.mod, ALTERNATIVE_MOD, "control"], "l", self.lazy.spawn(f"swaylock -f -C {Path.home() / '.config' / 'swaylock' / 'config'}"), desc="Lock screen"),
            self.Key([self.mod, "control"], "r", self.lazy.function(regenerate_and_reload), desc="Regenerate theme and reload"),
            self.Key([self.mod, "control"], "q", self.lazy.shutdown(), desc="Shutdown qtile"),
        ]

    def _vt_switching(self) -> List:
        vt_keys = []
        for vt in range(1, 8):
            vt_keys.append(
                self.Key(
                    ["control", ALTERNATIVE_MOD],
                    f"f{vt}",
                    self.lazy.core.change_vt(vt).when(func=lambda: self.lazy.qtile.core.name == "wayland"),
                    desc=f"Switch to VT{vt}",
                )
            )
        return vt_keys

    def _volume_control(self) -> List:
        return [
            self.Key([], "F1", self.lazy.widget["pulsevol"].mute(), desc="Toggle mute"),
            self.Key([], "F2", self.lazy.widget["pulsevol"].decrease_vol(), desc="Volume down"),
            self.Key([], "F3", self.lazy.widget["pulsevol"].increase_vol(), desc="Volume up"),
        ]

    def get_group_bindings(self, groups) -> List:
        """Generate keybindings for workspace groups.
        
        Args:
            groups: List of Group objects
            
        Returns:
            List of Key configurations for group switching
        """
        group_keys = []
        for group in groups:
            group_keys.extend([
                self.Key([self.mod], group.name, self.lazy.group[group.name].toscreen(),
                    desc=f"Switch to group {group.name}"),
                self.Key([self.mod, "shift"], group.name, 
                    self.lazy.window.togroup(group.name, switch_group=True),
                    desc=f"Move window to group {group.name}"),
            ])
        return group_keys

def create_key_bindings(
    key_class: Any,
    lazy_module: Any,
    mod_key: str,
    terminal: str,
    screen_config: ScreenConfig,
    groups: List,
) -> List:
    """Factory function to create all key bindings."""
    kb = KeyBindings(key_class, lazy_module, mod_key, terminal, screen_config)
    return kb.get_all_bindings() + kb.get_group_bindings(groups)
