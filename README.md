pointlet's dotfiles

repository tree mimcs local directory tree

symlink farm will set up the configuration structure for the user by using gnu stow: https://www.gnu.org/software/stow/

# setup
1. install gnu stow
```
sudo apt install stow
# or
pacman -S stow
# etc, based on your distribution
```
2. cd into dotfile directory
```
cd dotfiles
```
3. now you can stow you configuration creating symlinks to the dotfiles directory for you local user

```
stow .
# or if you want to copy existing config file overriding the dotfiles version of it
stow --adopt
```

# themgen

simple token-replacement theming system. edit colors once in `.config/themegen/palette.toml`, run the renderer, and all your configs get updated.

## how it works

1. define theme variables in `.config/themegen/palette.toml` (colors, fonts, sizes, etc)
2. create `.tmpl` files with `$$$TOKEN$$$` placeholders
3. run `python3 .config/themegen/render.py` to generate configs

the script finds all `.tmpl` files, replaces tokens with palette values, and writes the output without the `.tmpl` extension.

example:
```toml
# .config/alacritty/colors.toml.tmpl
background = "$$$BACKGROUND$$$"
foreground = "$$$FOREGROUND$$$"
```
becomes:
```toml
# .config/alacritty/colors.toml
background = "#e6e2e1"
foreground = "#3b3936"
```

## palette variables

check `.config/themegen/palette.toml` for all available tokens. includes colors (BACKGROUND, FOREGROUND, ACCENT, etc), typography (FONT, FONT_SIZE), layout stuff (BORDER_WIDTH, INNER_GAP), and system settings (WALLPAPER_PATH, CLOCK_FORMAT).

## usage

```bash
# render all templates
python3 .config/themegen/render.py

# dry-run to see what would change
python3 .config/themegen/render.py --dry-run --verbose

# render specific templates only
python3 .config/themegen/render.py --only ".config/qtile/*.tmpl"
```

## adding new templates

1. rename your config: `config` → `config.tmpl`
2. replace hardcoded values with `$$$TOKEN$$$` placeholders
3. add new tokens to `palette.toml` if needed
4. run the renderer

config for:
- tmux
- alacritty
- rofi
- swaylock
- qtile
