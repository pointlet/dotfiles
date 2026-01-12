# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi

# User specific environment and startup programs
if [ -z "$DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
	# Nvidia + wlroots: disable hw cursors and avoid atomic modesetting to reduce resume crashes
	export WLR_NO_HARDWARE_CURSORS=1
	export WLR_DRM_NO_ATOMIC=1
	# Ensure Wayland session type for Qtile
	export XDG_SESSION_TYPE=wayland
	exec qtile start -b wayland
fi
