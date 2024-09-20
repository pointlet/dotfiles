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

config for:
- tmux
