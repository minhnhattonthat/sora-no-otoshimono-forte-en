-- Log frames where the choice commands (ops 2F / D0) run their vtable[4] (execute) and vtable[5].
local hits = { [0x020894F8] = "D0.exec", [0x02089398] = "2F.exec", [0x02089450] = "choice.v5" }
local last = {}
for addr, name in pairs(hits) do
  L.on_exec(addr, function()
    if last[name] and L.frame - last[name] < 30 then return end
    last[name] = L.frame
    L.log(string.format("f%d %s", L.frame, name))
  end)
end
