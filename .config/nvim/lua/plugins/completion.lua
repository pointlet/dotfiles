return {
    {
        "zbirenbaum/copilot.lua",
        cmd = "Copilot",
        event = "InsertEnter",
        config = function()
            require("copilot").setup({
                suggestion = {
                    enabled = true,
                    auto_trigger = true,
                    keymap = {
                        accept = false,        -- Handled manually in Tab mapping
                        accept_word = "<C-w>", -- Ctrl+w to accept word
                        accept_line = "<C-j>", -- Ctrl+j to accept line
                        next = "<C-n>",        -- Ctrl+n next suggestion
                        prev = "<C-p>",        -- Ctrl+p prev suggestion
                        dismiss = "<C-]>",     -- Ctrl+] dismiss
                    },
                },
                panel = { enabled = false },
            })
        end,
    },
    {
        "zbirenbaum/copilot-cmp",
        dependencies = { "zbirenbaum/copilot.lua" },
        config = function()
            require("copilot_cmp").setup()
        end,
    },
    {
        "hrsh7th/nvim-cmp",
        event = "InsertEnter",
        dependencies = {
            "hrsh7th/cmp-nvim-lsp",
            "hrsh7th/cmp-buffer",
            "hrsh7th/cmp-path",
            "L3MON4D3/LuaSnip",
            "saadparwaiz1/cmp_luasnip",
            "zbirenbaum/copilot-cmp",
        },
        config = function()
            local cmp = require("cmp")
            local luasnip = require("luasnip")

            cmp.setup({
                snippet = {
                    expand = function(args)
                        luasnip.lsp_expand(args.body)
                    end,
                },
                formatting = {
                    format = function(entry, vim_item)
                        vim_item.kind = ({
                            Text = "[Text]",
                            Method = "[Method]",
                            Function = "[Func]",
                            Constructor = "[Ctor]",
                            Field = "[Field]",
                            Variable = "[Var]",
                            Class = "[Class]",
                            Interface = "[Iface]",
                            Module = "[Mod]",
                            Property = "[Prop]",
                            Unit = "[Unit]",
                            Value = "[Val]",
                            Enum = "[Enum]",
                            Keyword = "[Key]",
                            Snippet = "[Snip]",
                            Color = "[Color]",
                            File = "[File]",
                            Reference = "[Ref]",
                            Folder = "[Dir]",
                            EnumMember = "[EnumM]",
                            Constant = "[Const]",
                            Struct = "[Struct]",
                            Event = "[Event]",
                            Operator = "[Op]",
                            TypeParameter = "[TParam]",
                            Copilot = "[AI]",
                        })[vim_item.kind] or vim_item.kind
                        vim_item.menu = ({
                            copilot = "[Copilot]",
                            nvim_lsp = "[LSP]",
                            luasnip = "[Snip]",
                            buffer = "[Buf]",
                            path = "[Path]",
                        })[entry.source.name]
                        return vim_item
                    end,
                },
                mapping = cmp.mapping.preset.insert({
                    ["<c-b>"] = cmp.mapping.scroll_docs(-4),
                    ["<c-f>"] = cmp.mapping.scroll_docs(4),
                    ["<c-space>"] = cmp.mapping.complete(),
                    ["<c-e>"] = cmp.mapping.abort(),
                    ["<cr>"] = cmp.mapping.confirm({ select = true }),
                    ["<tab>"] = cmp.mapping(function(fallback)
                        local suggestion = require("copilot.suggestion")
                        if suggestion.is_visible() then
                            suggestion.accept()
                        elseif cmp.visible() then
                            cmp.select_next_item()
                        elseif luasnip.expand_or_jumpable() then
                            luasnip.expand_or_jump()
                        else
                            fallback()
                        end
                    end, { "i", "s" }),
                    ["<s-tab>"] = cmp.mapping(function(fallback)
                        if cmp.visible() then
                            cmp.select_prev_item()
                        elseif luasnip.jumpable(-1) then
                            luasnip.jump(-1)
                        else
                            fallback()
                        end
                    end, { "i", "s" }),
                }),
                sources = cmp.config.sources({
                    { name = "copilot", group_index = 2 },
                    { name = "nvim_lsp", group_index = 2 },
                    { name = "luasnip", group_index = 2 },
                }, {
                    { name = "buffer", group_index = 3 },
                    { name = "path", group_index = 3 },
                }),
            })

        end,
    },
}
