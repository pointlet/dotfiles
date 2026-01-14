local map = vim.keymap.set

-- Files
map("n", "<leader>w", "<cmd>w<cr>", { desc = "Save" })
map("n", "<leader>q", "<cmd>q<cr>", { desc = "Quit" })
map("n", "<leader>x", "<cmd>x<cr>", { desc = "Save and quit" })

-- Windows
map("n", "<leader>h", "<c-w>h", { desc = "Go to left window" })
map("n", "<leader>j", "<c-w>j", { desc = "Go to lower window" })
map("n", "<leader>k", "<c-w>k", { desc = "Go to upper window" })
map("n", "<leader>l", "<c-w>l", { desc = "Go to right window" })
map("n", "<leader>i", "<c-w>v", { desc = "Split window vertically" })
map("n", "<leader>o", "<c-w>s", { desc = "Split window horizontally" })

-- Buffers
map("n", "<leader>n", "<cmd>bnext<cr>", { desc = "Next buffer" })
map("n", "<leader>p", "<cmd>bprevious<cr>", { desc = "Previous buffer" })

-- Search
map("n", "<leader>c", "<cmd>nohlsearch<cr>", { desc = "Clear search highlight" })
map("n", "<leader>r", function()
    local word = vim.fn.expand("<cword>")
    vim.ui.input({ prompt = "Replace '" .. word .. "' with: " }, function(new)
        if new and new ~= "" then
            vim.cmd(":%s/\\<" .. word .. "\\>/" .. new .. "/gc")
        end
    end)
end, { desc = "Replace current word" })

-- LSP
map("n", "<leader>d", vim.lsp.buf.definition, { desc = "Go to definition" })
map("n", "<leader>t", vim.lsp.buf.hover, { desc = "Hover tooltip" })

-- Reload theme
map("n", "<leader>R", function()
    package.loaded["theme.colors"] = nil
    package.loaded["theme"] = nil
    require("theme").setup()
end, { desc = "Reload theme" })

-- Better defaults
map("n", "J", "mzJ`z", { desc = "Join lines (keep cursor)" })
map("n", "<c-d>", "<c-d>zz", { desc = "Scroll down (centered)" })
map("n", "<c-u>", "<c-u>zz", { desc = "Scroll up (centered)" })
map("n", "n", "nzzzv", { desc = "Next search result (centered)" })
map("n", "N", "Nzzzv", { desc = "Prev search result (centered)" })

-- Move lines
map("v", "J", ":m '>+1<cr>gv=gv", { desc = "Move selection down" })
map("v", "K", ":m '<-2<cr>gv=gv", { desc = "Move selection up" })

-- Stay in visual mode when indenting
map("v", "<", "<gv", { desc = "Indent left" })
map("v", ">", ">gv", { desc = "Indent right" })
