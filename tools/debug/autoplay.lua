-- QA autoplay for Sora Forte (run with an emu.py route that ends at once, e.g. --route-str "1 -", no --mash).
-- Default input alternates A / left (A opens "Go to the next episode?", left picks Yes, A confirms; A advances text).
-- On a GAME OVER screen it presses A (Retry) until the third option "Skip" is shown, then down, down, A.
-- Logs each Skip and each GAME OVER to log.txt with the frame number.
-- gui.getpixel returns stale/blended colours on the QA fork; gui.gdscreenshot matches the PNG shots
-- (gd truecolor: 11-byte header, then A,R,G,B per pixel, 256 x 384).
local shot
local function white(x0, y0, x1, y1)
  local n = 0
  for y = y0, y1, 2 do
    for x = x0, x1, 2 do
      local o = 11 + (y * 256 + x) * 4
      if shot:byte(o + 2) + shot:byte(o + 3) + shot:byte(o + 4) > 600 then n = n + 1 end
    end
  end
  return n
end

local phase, cooldown, gameovers, savecount, still, lasthash = 0, 0, 0, 0, 0, nil
L.on_frame(function(f)
  if f < (AUTO_FROM or 200) then  -- after a state load the JIT screen stays grey for a while: wait, don't guess
    if L.route_done() then L.press("-", 10) end
    return
  end
  if cooldown > 0 then cooldown = cooldown - 1 end
  if cooldown == 0 and L.route_done() then   -- the queue empties every 20 frames
    shot = gui.gdscreenshot()
    local go = white(40, 92, 200, 104)          -- "GAME OVER" logo on the top screen
    local skip = white(84, 322, 112, 332)        -- "Skip" (third option) on the bottom screen
    if go > 350 and white(2, 92, 24, 104) == 0 then  -- calibrated: GAME OVER 408, gameplay <= 250
      gameovers = gameovers + 1
      if (skip > 15 and skip < 70) or gameovers >= (SKIP_AFTER or 99) then  -- SKIP_AFTER=2 for the JP ROM
        gameovers = 0
        L.log(string.format("%d gameover+skip -> Skip", f))
        L.press("-", 30); L.press("down", 8); L.press("-", 30); L.press("down", 8); L.press("-", 30); L.press("a", 8)
        L.press("-", 200)
      else
        L.log(string.format("%d gameover -> Retry", f))
        L.press("-", 30); L.press("a", 8); L.press("-", 200)
      end
      cooldown = 400
      return
    end
    -- Rotated (DS held sideways) GAME OVER: vertical logo at x 118-146, dim strip at x 100-112, Skip at 72-88/245-275.
    -- Calibrated on Mikako's scene: logo 511, strip 0, Skip 46 (gameplay: strip 275, Skip 23).
    if white(118, 20, 146, 180) > 400 and white(100, 0, 112, 190) == 0 then
      if white(72, 245, 88, 275) > 35 then
        L.log(string.format("%d rotated gameover+skip -> Skip", f))
        L.press("-", 30); L.press("left", 8); L.press("-", 40); L.press("left", 8); L.press("-", 40); L.press("a", 8)
      else
        L.log(string.format("%d rotated gameover -> Retry", f))
        L.press("-", 30); L.press("a", 8)
      end
      L.press("-", 200); cooldown = 400
      return
    end
    -- Stuck on a static screen (help pages, menus that A/left can't leave): press B.
    local h = shot:sub(11 + (100 * 256) * 4, 11 + (101 * 256) * 4) .. shot:sub(11 + (300 * 256) * 4, 11 + (301 * 256) * 4)
    if h == lasthash then still = still + 1 else still = 0; lasthash = h end
    if still >= 60 then
      L.log(string.format("%d static screen -> B", f))
      L.press("b", 8); L.press("-", 60); still = 0
      return
    end
    -- Data Save screen (pink header bar at 200,197; 55,24,39 when the game's dark band covers it):
    -- A/left alone loops saving forever, so back out with B.
    local o = 11 + (197 * 256 + 200) * 4
    local r, g, b = shot:byte(o + 2), shot:byte(o + 3), shot:byte(o + 4)
    if (r == 223 and g == 97 and b == 158) or (r == 55 and g == 24 and b == 39) then
      savecount = savecount + 1
      if savecount >= 15 then
        L.log(string.format("%d data save screen -> B", f))
        L.press("b", 8); L.press("-", 40); L.press("b", 8); L.press("-", 120); savecount = 0
        return
      end
    else
      savecount = 0
    end
  end
  if L.route_done() then
    -- "Go to the next episode?" dialog (blue frame at 128,300 and tree at 20,312): left = Yes, then A.
    local function px(x, y)
      local o = 11 + (y * 256 + x) * 4
      return shot:byte(o + 2) * 65536 + shot:byte(o + 3) * 256 + shot:byte(o + 4)
    end
    if shot and px(128, 300) == 0x245DFF and px(20, 312) == 0x41798E then
      L.press("left", 8); L.press("-", 20)
    end
    L.press("a", 8)
    L.press("-", 12)
  end
end)
