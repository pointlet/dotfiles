# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi

# User specific environment and startup programs
if [ -z "$DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
	export XDG_SESSION_TYPE=wayland
	exec qtile start -b wayland
fi
