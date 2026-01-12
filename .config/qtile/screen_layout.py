"""Screen layout management for Qtile configuration."""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

# Type alias for window geometry (x, y, width, height)
WindowGeometry = Tuple[int, int, int, int]


class BarPosition(Enum):
    """Position of the status bar on screen."""
    TOP = "top"
    BOTTOM = "bottom"


@dataclass(frozen=True)
class ScreenConfig:
    """Screen configuration with dimensions accounting for bar, borders, and gaps.
    
    All window positioning calculations automatically adjust based on
    bar position, border width, and gap settings.
    
    Attributes:
        screen_width: Total screen width in pixels
        screen_height: Total screen height in pixels
        bar_height: Height of the status bar
        bar_position: Where the bar is placed (top or bottom)
        border_width: Window border width in pixels
        outer_gap: Gap between windows and screen edges
        inner_gap: Gap between adjacent windows (split evenly between them)
    """
    
    screen_width: int = 1920
    screen_height: int = 1080
    bar_height: int = 24
    bar_position: BarPosition = BarPosition.TOP
    border_width: int = 2
    outer_gap: int = 8
    inner_gap: int = 8

    # -------------------------------------------------------------------------
    # Base calculations
    # -------------------------------------------------------------------------

    @property
    def _border_total(self) -> int:
        """Border width for both sides of a window."""
        return self.border_width * 2

    @property
    def _inner_gap_half(self) -> int:
        """Each window's contribution to the inner gap."""
        return self.inner_gap // 2

    @property
    def _outer_gap_total(self) -> int:
        """Outer gap on both edges."""
        return self.outer_gap * 2

    @property
    def _half_edge_gap(self) -> int:
        """Gap deduction for half-screen windows (outer edge + inner edge contribution)."""
        return self.outer_gap + self._inner_gap_half

    @property
    def _usable_height(self) -> int:
        """Screen height minus bar."""
        return self.screen_height - self.bar_height

    @property
    def _content_start_y(self) -> int:
        """Y coordinate where content area begins."""
        return self.bar_height if self.bar_position == BarPosition.TOP else 0

    @property
    def _center_x(self) -> int:
        """Horizontal center of screen."""
        return self.screen_width // 2

    @property
    def _center_y(self) -> int:
        """Vertical center of usable area."""
        return self._content_start_y + (self._usable_height // 2)

    # -------------------------------------------------------------------------
    # X positions
    # -------------------------------------------------------------------------

    @property
    def _x_left(self) -> int:
        """X position for left-aligned windows."""
        return self.outer_gap

    @property
    def _x_right(self) -> int:
        """X position for right-aligned windows."""
        return self._center_x + self._inner_gap_half

    # -------------------------------------------------------------------------
    # Y positions
    # -------------------------------------------------------------------------

    @property
    def _y_top(self) -> int:
        """Y position for top-aligned windows."""
        return self._content_start_y + self.outer_gap

    @property
    def _y_bottom(self) -> int:
        """Y position for bottom-aligned windows."""
        return self._center_y + self._inner_gap_half

    # -------------------------------------------------------------------------
    # Widths
    # -------------------------------------------------------------------------

    @property
    def _width_full(self) -> int:
        """Width spanning entire screen."""
        return self.screen_width - self._border_total - self._outer_gap_total

    @property
    def _width_half(self) -> int:
        """Width for half-screen windows."""
        return self._center_x - self._border_total - self._half_edge_gap

    # -------------------------------------------------------------------------
    # Heights
    # -------------------------------------------------------------------------

    @property
    def _height_full(self) -> int:
        """Height spanning entire usable area."""
        return self._usable_height - self._border_total - self._outer_gap_total

    @property
    def _height_half(self) -> int:
        """Height for half-screen windows."""
        return (self._usable_height // 2) - self._border_total - self._half_edge_gap

    # -------------------------------------------------------------------------
    # Public geometry methods
    # -------------------------------------------------------------------------

    def get_full_screen(self) -> WindowGeometry:
        """Full screen window geometry."""
        return (self._x_left, self._y_top, self._width_full, self._height_full)

    def get_left_half(self) -> WindowGeometry:
        """Left half of screen."""
        return (self._x_left, self._y_top, self._width_half, self._height_full)

    def get_right_half(self) -> WindowGeometry:
        """Right half of screen."""
        return (self._x_right, self._y_top, self._width_half, self._height_full)

    def get_top_half(self) -> WindowGeometry:
        """Top half of screen."""
        return (self._x_left, self._y_top, self._width_full, self._height_half)

    def get_bottom_half(self) -> WindowGeometry:
        """Bottom half of screen."""
        return (self._x_left, self._y_bottom, self._width_full, self._height_half)

    def get_top_left_quarter(self) -> WindowGeometry:
        """Top-left quarter of screen."""
        return (self._x_left, self._y_top, self._width_half, self._height_half)

    def get_top_right_quarter(self) -> WindowGeometry:
        """Top-right quarter of screen."""
        return (self._x_right, self._y_top, self._width_half, self._height_half)

    def get_bottom_left_quarter(self) -> WindowGeometry:
        """Bottom-left quarter of screen."""
        return (self._x_left, self._y_bottom, self._width_half, self._height_half)

    def get_bottom_right_quarter(self) -> WindowGeometry:
        """Bottom-right quarter of screen."""
        return (self._x_right, self._y_bottom, self._width_half, self._height_half)
