# swayidle user service

This directory contains the user-level systemd unit to run `swayidle` with `swaylock` in a Qtile Wayland session.

## Files
- `systemd/user/swayidle.service`: user unit with ConditionEnvironment=WAYLAND_DISPLAY
- `systemd/user/swayidle.service.d/override.conf`: command overrides for swayidle/swaylock

## Setup
1) Reload and enable the user units:
```
systemctl --user daemon-reload
systemctl --user enable --now swayidle.service
```
2) Start/verify swayidle:
```
systemctl --user restart swayidle.service
systemctl --user status swayidle.service
```
3) Ensure logind suspends on lid so `before-sleep` fires. Example drop-in:
```
sudo tee /etc/systemd/logind.conf.d/10-lid.conf >/dev/null <<'EOF'
[Login]
HandleLidSwitch=suspend
HandleLidSwitchExternalPower=suspend
HandleLidSwitchDocked=suspend
EOF
sudo systemctl restart systemd-logind
```

## Daemons
- `swayidle.service`: locks on idle and before-sleep; restarts automatically.
- `lock-and-logout.service`: triggered on swayidle failure to lock and terminate the session.

## Notes
- Runs only on Wayland sessions; skips on X11.
- If you edit the swaylock path/config, update `override.conf` and reload the unit.
