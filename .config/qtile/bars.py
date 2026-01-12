"""Screen and bar assembly for Qtile."""

from typing import Any, List, Sequence

from screen_layout import ScreenConfig
from theme import BAR_BACKGROUND, WALLPAPER_MODE, WALLPAPER_PATH


def create_screens(
    screen_class: Any,
    bar_class: Any,
    screen_config: ScreenConfig,
    bar_widgets: Sequence[Any],
    wallpaper_path: str = WALLPAPER_PATH,
    wallpaper_mode: str = WALLPAPER_MODE,
) -> List[Any]:
    """Create screen configuration with an attached bar."""
    bar_section = {
        screen_config.bar_position.value: bar_class(
            bar_widgets,
            screen_config.bar_height,
            background=BAR_BACKGROUND,
        )
    }

    screen_kwargs = {
        **bar_section,
        "wallpaper": wallpaper_path,
        "wallpaper_mode": wallpaper_mode,
    }

    return [screen_class(**screen_kwargs)]
