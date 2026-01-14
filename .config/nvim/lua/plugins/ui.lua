return {
    {
        "nvim-lualine/lualine.nvim",
        event = "VeryLazy",
        dependencies = { "nvim-tree/nvim-web-devicons" },
        config = function()
            local c = require("theme.colors")
            require("lualine").setup({
                options = {
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
                    lualine_b = { "branch", "diff", "diagnostics" },
                    lualine_c = { "filename" },
                    lualine_x = { "encoding", "fileformat", "filetype" },
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
        dependencies = { "nvim-tree/nvim-web-devicons" },
        opts = {
            view = { width = 30, side = "left" },
            renderer = {
                icons = {
                    show = { file = true, folder = true, folder_arrow = true, git = true },
                },
            },
            git = { enable = true, ignore = false },
        },
    },
    {
        "folke/which-key.nvim",
        event = "VeryLazy",
        opts = {},
    },
}
