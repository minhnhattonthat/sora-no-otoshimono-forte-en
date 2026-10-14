-- At the horizontal row-draw loop exit (0x0208F064): rows, last-row length, col/row start, x offset, row bytes.
local from, to, n = FROM or 0, TO or math.huge, 0
L.on_exec(0x0208F064, function()
  if L.frame < from or L.frame > to or n > 200 then return end
  n = n + 1
  local sl = memory.getregister("arm9.r10")
  local rows, len = memory.readbyte(sl + 0x9EE), memory.readbyte(sl + 0x9EF)
  local col, row = memory.readword(sl + 0x9F0), memory.readword(sl + 0x9F2)
  local off = memory.readdword(sl + 0x76C)
  local s = {}
  for r = 0, rows - 1 do
    local t = {}
    for i = 0, 15 do t[#t + 1] = string.format("%02X", memory.readbyte(sl + 0x7BE + r * 0x38 + i)) end
    s[#s + 1] = table.concat(t, "")
  end
  L.log(string.format("f%d rows=%d len=%d col=%d row=%d off=%d %s", L.frame, rows, len, col, row, off, table.concat(s, " | ")))
end)
