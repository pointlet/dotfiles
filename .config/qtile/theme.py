"""Shared theme values for Qtile configuration."""

# Fonts (smaller to reduce rendered surface size)
BAR_FONT = "IBM Plex Mono SemiBold"
BAR_FONT_SIZE = 13  # was 15
BAR_PADDING = 4      # was 6

# Dimensions / spacing
BAR_HEIGHT = 24
BORDER_WIDTH = 4
OUTER_GAP = 8
INNER_GAP = 8

# Colors
COLOR_FOREGROUND = "#000000"
COLOR_INACTIVE = "#a0a0a0"
COLOR_ACTIVE_BORDER = "#f0f0f0"
COLOR_URGENT = "#ff0000"
COLOR_BORDER_FOCUS = "#f5f5f5"   # Off-white
COLOR_BORDER_NORMAL = "#545454"   # Subtle gray

# Volume bar colors
COLOR_VOLUME_BAR_ACTIVE = "#000000"        # Filled bars when unmuted
COLOR_VOLUME_BAR_INACTIVE = COLOR_INACTIVE  # Empty bars when unmuted
COLOR_VOLUME_BAR_MUTED_ACTIVE = "#ff0000"  # Filled bars when muted
COLOR_VOLUME_BAR_MUTED_INACTIVE = "#ff8080"  # Empty bars when muted (faded red)

# Bar (opaque to avoid compositor translucency overhead)
BAR_BACKGROUND = "#00000000" 
CLOCK_FORMAT = "%H:%M %a %d/%m"

# Wallpaper (None avoids decoding/keeping a large image in memory)
WALLPAPER_PATH = "/home/pointlet/images/wallpaper.jpg"
WALLPAPER_MODE = "fill"
