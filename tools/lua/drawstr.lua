-- Log calls to the NNS-style DrawString at 0x203A198: x, y, string bytes, caller. Distinct (lr, x, y, text) only.
--   emu.py ... --script tools/lua/drawstr.lua [--var FROM=2600 --var TO=3200]
local from, to = FROM or 0, TO or math.huge
local seen, n = {}, 0
L.on_exec(0x0203A198, function()
  if L.frame < from or L.frame > to or n > 400 then return end
  local r1, r2, r3 = memory.getregister("arm9.r1"), memory.getregister("arm9.r2"), memory.getregister("arm9.r3")
  local lr = memory.getregister("arm9.r14")
  local s = {}
  for i = 0, 23 do
    local b = memory.readbyte(r3 + i)
    if b == 0 then break end
    s[#s + 1] = string.format("%02X", b)
  end
  local k = string.format("lr=%08X x=%d y=%d s=%s", lr, r1, r2, table.concat(s, " "))
  if not seen[k] then
    seen[k] = true; n = n + 1
    L.log(string.format("f%d %s ptr=%08X", L.frame, k, r3))
  end
end)
