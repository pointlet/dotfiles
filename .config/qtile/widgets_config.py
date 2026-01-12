"""Widget defaults and bar widget factory for Qtile."""

import subprocess
from typing import Any, Dict, List, Optional, Tuple

from libqtile import bar
from libqtile.widget.pulse_volume import PulseVolume

from theme import (
    BAR_FONT,
    BAR_FONT_SIZE,
    BAR_PADDING,
    CLOCK_FORMAT,
    COLOR_ACTIVE_BORDER,
    COLOR_FOREGROUND,
    COLOR_INACTIVE,
    COLOR_URGENT,
    COLOR_VOLUME_BAR_ACTIVE,
    COLOR_VOLUME_BAR_INACTIVE,
    COLOR_VOLUME_BAR_MUTED_ACTIVE,
    COLOR_VOLUME_BAR_MUTED_INACTIVE,
    OUTER_GAP,
)

WidgetDefaults = Dict[str, Any]
WidgetList = List[Any]


class TenBarPulseVolume(PulseVolume):
    """PulseVolume with 10-bar ASCII output instead of emoji."""

    def __init__(self, **config: Any) -> None:
        config.setdefault("markup", True)
        self.active_color: str = config.pop("active_color")
        self.inactive_color: str = config.pop("inactive_color")
        self.mute_active_color: str = config.pop("mute_active_color")
        self.mute_inactive_color: str = config.pop("mute_inactive_color")
        super().__init__(**config)

    def _update_drawer(self) -> None:
        volume = self.volume if self.volume is not None else 0
        clamped = max(0, min(100, volume))
        filled = min(10, (clamped + 9) // 10)  # 0-10 bars

        active_color = self.mute_active_color if self.is_mute else self.active_color
        inactive_color = self.mute_inactive_color if self.is_mute else self.inactive_color

        bars: List[str] = []
        for i in range(10):
            color = active_color if i < filled else inactive_color
            bars.append(f"<span foreground=\"{color}\">|</span>")

        self.text = "".join(bars)


def get_primary_connection_status() -> str:
    """Return a short connection label preferring wired over Wi-Fi."""
    try:
        result = subprocess.run(
            ["nmcli", "-t", "-f", "DEVICE,TYPE,STATE,CONNECTION", "device"],
            capture_output=True,
            text=True,
            check=True,
            timeout=1.5,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        return "Net: unknown"

    best: Optional[Tuple[int, str, str]] = None  # priority, label, connection name

    for line in result.stdout.strip().splitlines():
        parts = line.split(":", maxsplit=3)
        if len(parts) != 4:
            continue

        _device, dev_type, state, connection = parts
        if state.lower() != "connected":
            continue

        priority = 0 if dev_type == "ethernet" else 1 if dev_type == "wifi" else 2
        label = "LAN" if dev_type == "ethernet" else "" if dev_type == "wifi" else dev_type
        if best is None or priority < best[0]:
            best = (priority, label, connection or dev_type)

    if best:
        _, label, connection = best
        return f"{connection}" if not label else f"{label}: {connection}"

    return "Offline"


def create_widget_defaults() -> WidgetDefaults:
    """Return default widget styling."""
    return {
        "font": BAR_FONT,
        "fontsize": BAR_FONT_SIZE,
        "padding": BAR_PADDING,
        "foreground": COLOR_FOREGROUND,
    }


def create_bar_widgets(widget_module: Any, lazy_module: Optional[Any] = None) -> WidgetList:
    """Create widgets for the status bar.

    Args:
        widget_module: Qtile widget module
        lazy_module: Optional Qtile lazy module for mouse callbacks
    """
    return [
        widget_module.GroupBox(
            active=COLOR_FOREGROUND,
            inactive=COLOR_INACTIVE,
            highlight_method="block",
            this_current_screen_border=COLOR_ACTIVE_BORDER,
            urgent_border=COLOR_URGENT,
            margin_y=0,
            margin_x=OUTER_GAP,  # respect outer gap on the left
            padding_y=0,
            padding=BAR_PADDING,
            width=bar.CALCULATED,  # auto-size so all workspaces fit
        ),
        widget_module.WindowName(
            padding_y=0,
            format="{name}",  # drop state prefixes like V/F
            max_chars=40,
            ellipsis=True,
            padding=0,
            width=200,
        ),
        widget_module.Prompt(name="prompt", padding=0, width=140),
        widget_module.Spacer(length=bar.STRETCH, padding=0),
        widget_module.Clock(
            format=CLOCK_FORMAT,
            timezone="Europe/Stockholm",
            padding=0,
            width=160,
            fmt="{:^20}",  # center the rendered text within the widget
        ),
        widget_module.Spacer(length=bar.STRETCH, padding=0),
        widget_module.GenPollText(
            func=get_primary_connection_status,
            update_interval=10,
            padding=OUTER_GAP,
        ),
        widget_module.Battery(
            # Percent first, space, then state symbol at the end.
            format="{percent:>4.0%} {char}",
            charge_char="+",
            discharge_char="-",
            full_char="",
            empty_char="",
            unknown_char="",
            not_charging_char="",
            markup=False,
            padding=OUTER_GAP,
        ),
        TenBarPulseVolume(
            name="pulsevol",
            limit_max_volume=True,
            step=10,  # 10% steps
            font=BAR_FONT,
            fontsize=BAR_FONT_SIZE,
            active_color=COLOR_VOLUME_BAR_ACTIVE,  # black for filled bars
            inactive_color=COLOR_VOLUME_BAR_INACTIVE,  # theme gray for empty bars
            mute_active_color=COLOR_VOLUME_BAR_MUTED_ACTIVE,  # red for filled when muted
            mute_inactive_color=COLOR_VOLUME_BAR_MUTED_INACTIVE,  # faded red for empty when muted
            fmt="{0}",  # positional to avoid KeyError on older Qtile
            width=bar.CALCULATED,  # let the widget size itself while still providing a valid int width
            padding=OUTER_GAP,
        ),
    ]


def create_widgets(widget_module: Any, lazy_module: Optional[Any] = None) -> Tuple[WidgetDefaults, WidgetList]:
    """Return widget defaults and a bar widget list."""
    defaults = create_widget_defaults()
    widgets = create_bar_widgets(widget_module, lazy_module=lazy_module)
    return defaults, widgets
