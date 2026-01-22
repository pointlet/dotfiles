local servers = {
    pyright = {},
    ts_ls = {},
    gopls = {
        settings = {
            gopls = {
                gofumpt = true,
                codelenses = {
                    gc_details = false,
                    generate = true,
                    regenerate_cgo = true,
                    run_govulncheck = true,
                    test = true,
                    tidy = true,
                    upgrade_dependency = true,
                    vendor = true,
                },
                hints = {
                    assignVariableTypes = true,
                    compositeLiteralFields = true,
                    compositeLiteralTypes = true,
                    constantValues = true,
                    functionTypeParameters = true,
                    parameterNames = true,
                    rangeVariableTypes = true,
                },
                analyses = {
                    nilness = true,
                    unusedparams = true,
                    unusedwrite = true,
                    useany = true,
                },
                usePlaceholders = true,
                completeUnimported = true,
                staticcheck = true,
                directoryFilters = { "-.git", "-.vscode", "-.idea", "-.venv", "-node_modules" },
                semanticTokens = true,
            },
        },
    },
    bashls = {},
    lua_ls = {
        settings = {
            Lua = {
                runtime = { 
                    version = "LuaJIT",
                    meta = false,
                },
                diagnostics = { globals = { "vim" } },
                workspace = { library = vim.api.nvim_get_runtime_file("", true) },
                telemetry = { enable = false },
            },
        },
    },
}

-- Diagnostic configuration (virtual lines below code)
vim.diagnostic.config({
    virtual_text = false, -- Disable default virtual text
    virtual_lines = { only_current_line = true }, -- Show on current line only to reduce noise
    signs = true,
    underline = true,
    update_in_insert = false,
    severity_sort = true,
    float = {
        border = "rounded",
        source = true,
    },
})

-- Use fzf-lua for LSP pickers
vim.lsp.handlers["textDocument/definition"] = function(...)
    require('fzf-lua').lsp_definitions(...)
end
vim.lsp.handlers["textDocument/references"] = function(...)
    require('fzf-lua').lsp_references(...)
end
vim.lsp.handlers["textDocument/implementations"] = function(...)
    require('fzf-lua').lsp_implementations(...)
end
vim.lsp.handlers["textDocument/typeDefinition"] = function(...)
    require('fzf-lua').lsp_type_definitions(...)
end

-- LSP keymaps (set when server attaches to buffer)
vim.api.nvim_create_autocmd("LspAttach", {
    group = vim.api.nvim_create_augroup("lsp-attach", { clear = true }),
    callback = function(event)
        local map = function(mode, lhs, rhs, desc)
            vim.keymap.set(mode, lhs, rhs, { buffer = event.buf, desc = desc })
        end

        -- Navigation (g prefix for "go to")
        map("n", "<leader>l", vim.lsp.buf.definition, "Go to definition")
        map("n", "<leader>gD", vim.lsp.buf.declaration, "Go to declaration")
        map("n", "<leader>gi", vim.lsp.buf.implementation, "Go to implementation")
        map("n", "<leader>gt", vim.lsp.buf.type_definition, "Go to type definition")
        map("n", "<leader>gr", vim.lsp.buf.references, "Show references")

        -- Info
        map("n", "<leader>t", vim.lsp.buf.hover, "Hover info")
        map("n", "<leader>s", vim.lsp.buf.signature_help, "Signature help")

        -- Actions
        map("n", "<leader>rn", vim.lsp.buf.rename, "Rename symbol")
        map({ "n", "v" }, "<leader>ca", vim.lsp.buf.code_action, "Code action")
        map("n", "<leader>f", function() vim.lsp.buf.format({ async = true }) end, "Format")

        -- Inlay hints toggle (useful for Go type hints)
        if vim.lsp.inlay_hint then
            map("n", "<leader>th", function()
                vim.lsp.inlay_hint.enable(not vim.lsp.inlay_hint.is_enabled())
            end, "Toggle inlay hints")
        end
    end,
})

return {
    {
        "https://git.sr.ht/~whynothugo/lsp_lines.nvim",
        config = function()
            require("lsp_lines").setup()
        end,
    },
    {
        "mason-org/mason.nvim",
        lazy = false,
        opts = {},
    },
    {
        "mason-org/mason-lspconfig.nvim",
        lazy = false,
        dependencies = {
            "mason-org/mason.nvim",
            "neovim/nvim-lspconfig",
            "hrsh7th/cmp-nvim-lsp",
        },
        config = function()
            -- Configure servers BEFORE automatic_enable runs
            local capabilities = require("cmp_nvim_lsp").default_capabilities()

            for server, config in pairs(servers) do
                config.capabilities = capabilities
                vim.lsp.config(server, config)
            end

            require("mason-lspconfig").setup({
                ensure_installed = vim.tbl_keys(servers),
                automatic_enable = true,
            })
        end,
    },
    {
        "neovim/nvim-lspconfig",
        lazy = false,
    },
    {
        "WhoIsSethDaniel/mason-tool-installer.nvim",
        lazy = false,
        dependencies = { "mason-org/mason.nvim" },
        opts = {
            ensure_installed = {
                -- Linters
                "eslint",
                "golangci-lint",
                "flake8",
                "shellcheck",
                "selene",
                -- Formatters
                "prettier",
                "black",
                "shfmt",
                "stylua",
                "goimports",
                "gofumpt",
            },
        },
    },
}
