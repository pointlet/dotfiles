#!/bin/sh

# Import current Wayland session environment into the user systemd manager
systemctl --user import-environment WAYLAND_DISPLAY XDG_RUNTIME_DIR XDG_SESSION_TYPE

# Restart swayidle so it runs with the correct Wayland vars
systemctl --user restart swayidle.service