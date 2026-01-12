"""Mouse interaction configuration for Qtile."""

from typing import List, Any

from screen_layout import ScreenConfig


class MouseConfig:
    """Configure mouse interactions for window management."""
    
    def __init__(
        self,
        drag_class: Any,
        click_class: Any,
        lazy_module: Any,
        mod_key: str,
        screen_config: ScreenConfig,
    ):
        """Initialize mouse configuration.
        
        Args:
            drag_class: Qtile Drag class
            click_class: Qtile Click class
            lazy_module: Qtile lazy module
            mod_key: Modifier key (typically "mod4" for Super key)
            screen_config: Screen configuration for window positioning
        """
        self.Drag = drag_class
        self.Click = click_class
        self.lazy = lazy_module
        self.mod = mod_key
        self.screen = screen_config
    
    def get_bindings(self) -> List:
        """Get all mouse bindings.
        
        Returns:
            List of Drag and Click configurations
        """
        return self._drag_bindings() + self._click_bindings()
    
    def _drag_bindings(self) -> List:
        """Mouse drag bindings for moving and resizing."""
        return [
            self.Drag(
                [self.mod],
                "Button1",
                self.lazy.window.set_position_floating(),
                start=self.lazy.window.get_position()
            ),
            self.Drag(
                [self.mod],
                "Button3",
                self.lazy.window.set_size_floating(),
                start=self.lazy.window.get_size()
            ),
        ]
    
    def _click_bindings(self) -> List:
        """Mouse click bindings."""
        return [
            self.Click(
                [self.mod],
                "Button2",
                self.lazy.window.bring_to_front()
            ),
        ]


def create_mouse_config(
    drag_class: Any,
    click_class: Any,
    lazy_module: Any,
    mod_key: str,
    screen_config: ScreenConfig,
) -> List:
    """Factory function to create mouse configuration.
    
    Args:
        drag_class: Qtile Drag class
        click_class: Qtile Click class
        lazy_module: Qtile lazy module
        mod_key: Modifier key for mouse bindings
        screen_config: Screen configuration
        
    Returns:
        List of mouse bindings
    """
    config = MouseConfig(drag_class, click_class, lazy_module, mod_key, screen_config)
    return config.get_bindings()
