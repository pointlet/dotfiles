# nvim

minimal neovim setup for python, javascript, and go. uses the themegen palette for colors.

## structure

```
nvim/
├── init.lua              # entry point
├── lua/
│   ├── options.lua       # editor settings
│   ├── keymaps.lua       # key bindings
│   ├── plugins/          # plugin configs (lazy.nvim)
│   │   ├── init.lua      # bootstrap + plugin loader
│   │   ├── lsp.lua       # mason + language servers
│   │   ├── completion.lua
│   │   ├── treesitter.lua
│   │   ├── telescope.lua
│   │   ├── ui.lua        # lualine, nvim-tree, which-key
│   │   └── git.lua
│   └── theme/
│       ├── init.lua      # highlight groups
│       └── colors.lua.tmpl
└── README.md
```

## keybindings

leader is `<space>`.

| key | action |
|-----|--------|
| `<leader>w` | save |
| `<leader>q` | quit |
| `<leader>e` | toggle file tree |
| `<leader>ff` | find files |
| `<leader>fg` | grep |
| `<leader>l` | go to definition |
| `<leader>i` | hover info |
| `<leader>rn` | rename symbol |
| `<leader>ca` | code actions |
| `<leader>f` | format |

press `<leader>` and wait for which-key to show all available bindings.

## common tasks

**add a language server**

edit `lua/plugins/lsp.lua`, add to the `servers` table:
```lua
local servers = {
    pyright = {},
    your_server = {},  -- add here
}
```
mason will auto-install it on next launch.

**change colors**

edit `.config/themegen/palette.toml` and run:
```bash
python3 .config/themegen/render.py
```

**add a plugin**

create a file in `lua/plugins/` or add to an existing one. lazy.nvim auto-loads everything in that directory.

## requirements

- neovim 0.10+
- git
- a nerd font (for icons)
