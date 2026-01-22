local map = vim.keymap.set

-- Files
map("n", "<leader>fs", "<cmd>w<cr>", { desc = "Save file" })
map("n", "<leader>q", "<cmd>q<cr>", { desc = "Quit" })
map("n", "<leader>x", "<cmd>x<cr>", { desc = "Save and quit" })

-- Windows (under <leader>w prefix, mirrors vim's <C-w>)
map("n", "<leader>wh", "<c-w>h", { desc = "Go to left window" })
map("n", "<leader>wj", "<c-w>j", { desc = "Go to lower window" })
map("n", "<leader>wk", "<c-w>k", { desc = "Go to upper window" })
map("n", "<leader>wl", "<c-w>l", { desc = "Go to right window" })
map("n", "<leader>wv", "<c-w>v", { desc = "Split window vertically" })
map("n", "<leader>ws", "<c-w>s", { desc = "Split window horizontally" })
map("n", "<leader>wc", "<c-w>c", { desc = "Close window" })
map("n", "<leader>wo", "<c-w>o", { desc = "Close other windows" })
map("n", "<leader>w=", "<c-w>=", { desc = "Equal window sizes" })
map("n", "<C-Up>", "<cmd>resize +2<cr>", { desc = "Increase height" })
map("n", "<C-Down>", "<cmd>resize -2<cr>", { desc = "Decrease height" })
map("n", "<C-Right>", "<cmd>vertical resize +2<cr>", { desc = "Increase width" })
map("n", "<C-Left>", "<cmd>vertical resize -2<cr>", { desc = "Decrease width" })

-- Jump list navigation (like browser back/forward)
map("n", "<leader>h", "<c-o>", { desc = "Jump back (older position)" })
map("n", "<leader>l", vim.lsp.buf.definition, { desc = "Go to definition" })
map("n", "<leader>L", "<c-i>", { desc = "Jump forward (newer position)" })

-- Buffers
map("n", "<leader>n", "<cmd>bnext<cr>", { desc = "Next buffer" })
map("n", "<leader>p", "<cmd>bprevious<cr>", { desc = "Previous buffer" })
map("n", "<leader>bd", "<cmd>bdelete<cr>", { desc = "Delete buffer" })

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

-- Diagnostics
map("n", "<leader>dd", vim.diagnostic.open_float, { desc = "Show diagnostic" })
map("n", "[d", vim.diagnostic.goto_prev, { desc = "Previous diagnostic" })
map("n", "]d", vim.diagnostic.goto_next, { desc = "Next diagnostic" })
map("n", "<leader>dl", vim.diagnostic.setloclist, { desc = "Diagnostics to loclist" })

-- Toggle diagnostic virtual lines mode
local diag_mode = 1 -- 0=off, 1=current line, 2=all lines
map("n", "<leader>td", function()
    diag_mode = (diag_mode + 1) % 3
    if diag_mode == 0 then
        vim.diagnostic.config({ virtual_lines = false })
        vim.notify("Diagnostics: off", vim.log.levels.INFO)
    elseif diag_mode == 1 then
        vim.diagnostic.config({ virtual_lines = { only_current_line = true } })
        vim.notify("Diagnostics: current line", vim.log.levels.INFO)
    else
        vim.diagnostic.config({ virtual_lines = true })
        vim.notify("Diagnostics: all lines", vim.log.levels.INFO)
    end
end, { desc = "Toggle diagnostic lines mode" })

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
