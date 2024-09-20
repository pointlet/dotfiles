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
3. 'stow .'
    - 'stow --adpot .' if you want to override conflicting files 
```
stow .
```

config for:
- tmux
