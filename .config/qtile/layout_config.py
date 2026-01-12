"""Layout configuration for Qtile."""

from typing import Any, List

from screen_layout import ScreenConfig
from theme import COLOR_BORDER_FOCUS, COLOR_BORDER_NORMAL


# ============================================================================
# IMPLEMENTATION
# ============================================================================

class LayoutConfig:
    """Configure window layouts and floating rules."""
    
    def __init__(
        self,
        layout_module: Any,
        match_class: Any,
        screen_config: ScreenConfig,
    ):
        """Initialize layout configuration.
        
        Args:
            layout_module: Qtile layout module
            match_class: Qtile Match class
            screen_config: Screen configuration for border width
        """
        self.layout = layout_module
        self.Match = match_class
        self.screen = screen_config
    
    def create_layouts(self) -> List:
        """Create window layouts.
        
        Returns:
            List of layout objects
        """
        return [
            self.layout.Floating(
                border_focus=COLOR_BORDER_FOCUS,
                border_normal=COLOR_BORDER_NORMAL,
                border_width=self.screen.border_width,
            ),
            self.layout.Max(margin=0),
        ]
    
    def get_floating_layout(self):
        """Get floating layout configuration.
        
        Returns:
            Configured Floating layout
        """
        return self.layout.Floating(
            border_focus=COLOR_BORDER_FOCUS,
            border_normal=COLOR_BORDER_NORMAL,
            border_width=self.screen.border_width,
            float_rules=[
                *self.layout.Floating.default_float_rules,
                self.Match(wm_class="confirmreset"),
                self.Match(wm_class="ssh-askpass"),
                self.Match(title="pinentry"),
            ]
        )


def create_layouts(
    layout_module: Any,
    match_class: Any,
    screen_config: ScreenConfig,
) -> tuple[List, Any]:
    """Factory function to create layouts.
    
    Args:
        layout_module: Qtile layout module
        match_class: Qtile Match class
        screen_config: Screen configuration
        
    Returns:
        Tuple of (layouts list, floating_layout)
    """
    config = LayoutConfig(layout_module, match_class, screen_config)
    return config.create_layouts(), config.get_floating_layout()
