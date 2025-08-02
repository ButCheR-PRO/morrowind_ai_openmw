-- scripts/morrowind_ai/config.lua
-- Регистрирует все подпакеты мода и экспортирует точку входа

local package_root = (...):gsub("%.[^%.]+$", "") -- "morrowind_ai"

-- Список подпакетов, которые должен видеть require()
local submodules = {
  "player",       -- scripts/morrowind_ai/player.lua
  "init",         -- scripts/morrowind_ai/init.lua
  "ui",           -- scripts/morrowind_ai/ui.lua (если есть)
  -- добавляйте свои файлы сюда
}

for _, name in ipairs(submodules) do
  local full = package_root .. "." .. name
  package.preload[full] = function()
    return require("scripts." .. full:gsub("%.", "/"))
  end
end

return true
