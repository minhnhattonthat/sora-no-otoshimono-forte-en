-- Like probes/watch.lua, but logs distinct (pc, lr) pairs for reads of WATCH_LO..WATCH_HI in FROM..TO.
--   emu.py ... --script tools/lua/who_reads.lua --var WATCH_LO=0x22B3C18 --var WATCH_HI=0x22D0000 --var FROM=2600
local lo, hi = assert(WATCH_LO), assert(WATCH_HI)
local from, to = FROM or 0, TO or math.huge
local seen = {}
L.on_read(lo, hi, function(addr, size)
  if L.frame < from or L.frame > to then return end
  local pc, lr = L.pc(), memory.getregister("arm9.r14")
  local k = pc * 4096 + (lr % 4096)
  if seen[k] then return end
  seen[k] = true
  L.log(string.format("f%d pc=%08X lr=%08X addr=%08X size=%s", L.frame, pc, lr, addr, tostring(size)))
end)
