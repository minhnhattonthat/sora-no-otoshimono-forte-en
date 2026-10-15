-- Debug jumps for Sora no Otoshimono Forte (DeSmuME QA fork, appended to emu.py's driver with --script).
-- Globals (set with emu.py --var):
--   STORY="ch,num"  replace the next story script load (Story/ChapterCC/NNN.dat) with chapter ch, script num, and
--                   set the current chapter byte so the rest of the episode (Action Select, Event Select, next
--                   parts) follows that chapter. ch is 0-based (Episode 4 = 3); num 0/100/200/300 = episode parts,
--                   ch 6 num 0-7 = endings, ch 7 num 0 = epilogue.
--   STORY_ALL=1     keep overriding every story load, not just the first (rarely wanted).
--   POKES="addr=val,.."  bytes written once at frame POKE_AT (default 2); POKE_EVERY=1 rewrites them every frame.
--   SCRIPTLOG=1     log every script id the game builds (type 0 chara event, 2 story, 3 extra).
-- RAM map: docs/re/debug.md.
local G = 0x020DB158               -- global game state (accessor 0x02031904)
local CHAPTER = G + 0x14E9         -- current chapter, 0-based (getter 0x02031D6C)
local LOADID = 0x0206964C          -- builds a script id + path: r2 num, r3 chapter, [sp] type, [sp+4] chara, [sp+8] sub

local jch, jnum = nil, nil
if STORY then jch, jnum = STORY:match("^(%d+),(%d+)$"); jch, jnum = tonumber(jch), tonumber(jnum) end
local jumped = false
-- EVENTS="3,10,1 3,11,1 ..." (chapter, chara, sub = Chara/ChapterCC/AA/BB_000.dat = text/en/chara/chCC_AA_BB_000):
-- each later story part (num 100/200/300, picked as NEXT in Event Select) is replaced by the next side event, so
-- autoplay chains through them; once the list is used up the story goes on.
local events = {}
for c, a, b in (EVENTS or ""):gmatch("(%d+),(%d+),(%d+)") do events[#events + 1] = { tonumber(c), tonumber(a), tonumber(b) } end
local nev = 0

L.on_exec(LOADID, function()
  local sp = memory.getregister("arm9.r13")
  local typ = memory.readdword(sp)
  if typ == 2 and nev < #events and memory.getregister("arm9.r2") > 0 and (jumped or not jch) then
    nev = nev + 1
    local e = events[nev]
    if e then
      memory.writedword(sp, 0); memory.writedword(sp + 4, e[2]); memory.writedword(sp + 8, e[3])
      memory.setregister("arm9.r3", e[1]); memory.setregister("arm9.r2", 0)
      L.log(string.format("f%d event ch%02d_%02d_%02d", L.frame, e[1], e[2], e[3]))
      typ = 0
    end
  end
  if jch and typ == 2 and (not jumped or STORY_ALL) then
    jumped = true
    memory.setregister("arm9.r3", jch)
    memory.setregister("arm9.r2", jnum)
    memory.writebyte(CHAPTER, jch)
    L.log(string.format("f%d jump story ch=%d num=%d", L.frame, jch, jnum))
  end
  if SCRIPTLOG then
    L.log(string.format("f%d script type=%d ch=%d num=%d chara=%d sub=%d chapter=%d", L.frame, typ,
      memory.getregister("arm9.r3"), memory.getregister("arm9.r2"), memory.readdword(sp + 4),
      memory.readdword(sp + 8), memory.readbyte(CHAPTER)))
  end
end)

-- Scene switch: 0x020538D4(id) news the next CProc. PROC=id replaces the first switch to PROC_FROM (default 3 =
-- title menu); PROC_FROM=-1 replaces the very next switch of any kind. Ids: docs/re/debug.md.
local SWITCH = 0x020538D4
local proc_done = false
-- UNLOCK=1: at each switch to the title menu, mark every Album item, Delusion Communication scene and clear as done
-- in the system data (what the save keeps across slots). Values: docs/re/debug.md.
local function unlock()
  for i = 0, 27 do memory.writebyte(G + 0xC4 + i, 1) end      -- Album/gallery items (getter 0x02031B94)
  for i = 0, 21 do memory.writebyte(G + 0xE0 + i, 4) end      -- communication scenes: 2 cleared, 4 + Advanced
  for i = 0, 2 do memory.writebyte(G + 0xF6 + i, 1) end       -- Tomo-Colle menu: Free Comm., Album, Member Roster
  if memory.readdword(G + 0x12C) == 0 then memory.writedword(G + 0x12C, 1) end  -- game clear count
  -- per-slot game data (G+0x210; replaced by New Game / Continue, so this only shows on screens opened with PROC)
  for i = 0, 27 do memory.writebyte(G + 0x1668 + i, 1) end    -- Titles (emblems) earned (getter 0x02032440)
  for i = 0, 5 do memory.writebyte(G + 0x1684 + i, 1) end     -- Help topics (getter 0x020324F8; 2 = read)
  memory.writedword(G + 0x1150, 9999)                         -- Growth Points (stat 5 at G+0x113C + 4*i)
  for i = 0, 4 do                                              -- stat levels (bytes, 1-10): a New Game starts at 1
    if memory.readbyte(G + 0x1154 + i) == 0 then memory.writebyte(G + 0x1154 + i, 1) end
  end
end
L.on_exec(SWITCH, function()
  local id = memory.getregister("arm9.r0")
  if UNLOCK and id == 3 then unlock(); L.log(string.format("f%d unlock", L.frame)) end
  if PROC and not proc_done and (id == (PROC_FROM or 3) or PROC_FROM == -1) and L.frame > (PROC_AFTER or 0) then
    proc_done = true
    memory.setregister("arm9.r0", PROC)
    L.log(string.format("f%d proc %d -> %d", L.frame, id, PROC))
    id = PROC
  end
  if SCENELOG then L.log(string.format("f%d scene %d", L.frame, id)) end
  -- SAVECLEAR=1: on the Clear Data save screen (scene 15) save to slot 1 (autoplay alone backs out with B).
  -- The run's OUT/<rom>.dsv then holds Clear Data: pass it to later runs with --sav.
  if SAVECLEAR and id == 15 then
    for _, s in ipairs({ { "-", 150 }, { "a", 6 }, { "-", 60 }, { "left", 6 }, { "-", 40 }, { "a", 6 }, { "-", 600 },
                         { "a", 6 }, { "-", 200 } }) do L.press(s[1], s[2]) end
    L.log(string.format("f%d saving Clear Data to slot 1", L.frame))
  end
end)

-- Script choices (ops 2F/D0 share exec 0x02089398): at 0x020893E0 r1 holds the picked index and r5 the command
-- (option count at +0x14). CHOICE="last" (skips "View the tutorial?" and its endless explanation menu), "first",
-- or a 0-based index; unset = whatever the cursor picked.
-- "last" picks the second-to-last option when the previous choice was < 400 frames ago: the tutorial menu's last
-- options are "Next page" / "Previous page", so plain "last" would page back and forth forever.
if CHOICE then
  local lastf = -1000
  L.on_exec(0x020893E0, function()
    local n = memory.readbyte(memory.getregister("arm9.r5") + 0x14)
    local pick = CHOICE == "first" and 0 or tonumber(CHOICE)
    if CHOICE == "last" then pick = (L.frame - lastf < 400 and n > 1) and n - 2 or n - 1 end
    lastf = L.frame
    if n > 0 and pick and pick < n then
      memory.setregister("arm9.r1", pick)
      L.log(string.format("f%d choice %d of %d", L.frame, pick, n))
    end
  end)
end

-- SKIP=1: the GAME OVER menu of a communication scene (handler 0x0206092C, picked item in r0 at 0x02060970:
-- 0 Retry, 1 Title, 2 Skip) always takes Skip, even on the first GAME OVER where Skip is not shown yet.
-- The scene then counts as given up (results screen, story continues).
if SKIP then
  L.on_exec(0x02060970, function()
    if memory.getregister("arm9.r0") ~= 2 then
      memory.setregister("arm9.r0", 2)
      L.log(string.format("f%d gameover -> skip", L.frame))
    end
  end)
end

local pokes = {}
for a, v in (POKES or ""):gmatch("(%w+)=(%w+)") do pokes[#pokes + 1] = { tonumber(a), tonumber(v) } end
L.on_frame(function(f)
  if #pokes > 0 and (f == (POKE_AT or 2) or (POKE_EVERY and f > (POKE_AT or 2))) then
    for _, p in ipairs(pokes) do memory.writebyte(p[1], p[2]) end
    if f == (POKE_AT or 2) then L.log(string.format("f%d poked %d bytes", f, #pokes)) end
  end
end)
