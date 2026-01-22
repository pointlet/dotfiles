return {
    {
        "nvim-lualine/lualine.nvim",
        event = "VeryLazy",
        config = function()
            local c = require("theme.colors")
            require("lualine").setup({
                options = {
                    icons_enabled = false,
                    theme = {
                        normal = {
                            a = { fg = c.bg, bg = c.accent },
                            b = { fg = c.fg, bg = c.muted },
                            c = { fg = c.fg, bg = c.bg },
                        },
                        insert = { a = { fg = c.bg, bg = c.accent } },
                        visual = { a = { fg = c.bg, bg = c.accent } },
                        replace = { a = { fg = c.bg, bg = c.danger } },
                        command = { a = { fg = c.bg, bg = c.accent } },
                        inactive = {
                            a = { fg = c.muted, bg = c.surface },
                            b = { fg = c.muted, bg = c.surface },
                            c = { fg = c.muted, bg = c.surface },
                        },
                    },
                    component_separators = "|",
                    section_separators = "",
                },
                sections = {
                    lualine_a = { "mode" },
                    lualine_b = {
                        { "branch", icon = "" },
                        { "diff", symbols = { added = "+", modified = "~", removed = "-" } },
                        { "diagnostics", symbols = { error = "E", warn = "W", info = "I", hint = "H" } },
                    },
                    lualine_c = { "filename" },
                    lualine_x = { "encoding", "fileformat", { "filetype", icons_enabled = false } },
                    lualine_y = { "progress" },
                    lualine_z = { "location" },
                },
            })
        end,
    },
    {
        "nvim-tree/nvim-tree.lua",
        keys = {
            { "<leader>e", "<cmd>NvimTreeToggle<cr>", desc = "Toggle file tree" },
        },
        opts = {
            view = { width = 30, side = "left" },
            renderer = {
                icons = {
                    show = { file = false, folder = false, folder_arrow = true, git = true },
                    glyphs = {
                        folder = {
                            arrow_closed = ">",
                            arrow_open = "v",
                        },
                        git = {
                            unstaged = "M",
                            staged = "S",
                            unmerged = "U",
                            renamed = "R",
                            untracked = "?",
                            deleted = "D",
                            ignored = "I",
                        },
                    },
                },
            },
            git = { enable = true, ignore = false },
        },
    },
    {
        "folke/which-key.nvim",
        event = "VeryLazy",
        opts = {
            icons = {
                mappings = false,
                breadcrumb = ">>",
                separator = "->",
                group = "+",
            },
        },
    },
}
