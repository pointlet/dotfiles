local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.uv.fs_stat(lazypath) then
    vim.fn.system({
        "git", "clone", "--filter=blob:none",
        "https://github.com/folke/lazy.nvim.git",
        "--branch=stable", lazypath,
    })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
    spec = {
        { import = "plugins.lsp" },
        { import = "plugins.completion" },
        { import = "plugins.treesitter" },
        { import = "plugins.telescope" },
        { import = "plugins.ui" },
        { import = "plugins.git" },
        { 'echasnovski/mini.nvim', version = false, config = function() require('mini.pairs').setup() end },
        { 'stevearc/conform.nvim', opts = {
            format_on_save = { timeout_ms = 500, lsp_fallback = true },
            formatters_by_ft = {
                lua = { "stylua" },
                python = { "black" },
                javascript = { "prettier" },
                typescript = { "prettier" },
                javascriptreact = { "prettier" },
                typescriptreact = { "prettier" },
                go = { "goimports", "gofumpt" },
                sh = { "shfmt" },
            },
        } },
        { 'mfussenegger/nvim-lint', config = function()
            require('lint').linters_by_ft = {
                lua = { 'selene' },
                python = { 'flake8' },
                javascript = { 'eslint' },
                typescript = { 'eslint' },
                go = { 'golangci-lint' },
                sh = { 'shellcheck' },
            }
        end },
        { 'ibhagwan/fzf-lua', opts = {
            file_icon_padding = '',
            preview = true,
            fzf_opts = {
                ['--color'] = 'bg:#e6e2e1,fg:#3b3936,hl:#596369,fg+:#3b3936,bg+:#e6e2e1,hl+:#3b3936,info:#83909a,prompt:#83909a,pointer:#83909a,marker:#83909a,spinner:#83909a,header:#83909a'
            },
            files = { file_icons = false, git_icons = false },
            grep = { file_icons = false, git_icons = false },
            buffers = { file_icons = false, git_icons = false },
            lsp = {
                symbols = 'disabled'
            }
        }, config = function()
            vim.env.FZF_DEFAULT_OPTS = '--color=bg:#e6e2e1,fg:#3b3936,hl:#596369,fg+:#3b3936,bg+:#e6e2e1,hl+:#3b3936,info:#83909a,prompt:#83909a,pointer:#83909a,marker:#83909a,spinner:#83909a,header:#83909a'
        end },
    },
    checker = { enabled = false },
})
