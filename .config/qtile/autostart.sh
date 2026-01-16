#!/bin/sh

echo "qtile autostart ran at $(date)" >> /tmp/qtile-autostart.log
dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP=wlroots
systemctl --user restart xdg-desktop-portal xdg-desktop-portal-wlr

# Import current Wayland session environment into the user systemd manager
systemctl --user import-environment WAYLAND_DISPLAY XDG_RUNTIME_DIR XDG_SESSION_TYPE

# Restart swayidle so it runs with the correct Wayland vars
systemctl --user restart swayidle.service