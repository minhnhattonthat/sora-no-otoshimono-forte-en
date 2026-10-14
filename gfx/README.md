# Graphics text: edit specs

Each image with Japanese text gets one JSON spec under `gfx/edits/<Folder>/<Name>.json`. `tools/build.py` applies every
spec (tools/gfxedit.py). Inventory of images: `docs/re/graphics.md`. Glossary: `glossary.md` (same names/terms as the
dialogue; title text in Title Case).

## Workflow (per image)
1. Write a spec with `"ops": []` and run `python -X utf8 tools/gfxedit.py orig gfx/edits/<Folder>/<Name>.json`
   -> `work/gfx/preview/<Folder>_<Name>.orig.png` (true size). Look at it (Read tool); measure pixel rects.
   To read pixel colours: `python -X utf8 -c "from PIL import Image; im=Image.open('...orig.png'); print(im.getpixel((x,y)))"`.
2. Add ops, then `python -X utf8 tools/gfxedit.py preview gfx/edits/<Folder>/<Name>.json` -> `..._<Name>.png` (2x zoom).
   Look at it. Iterate until the English is clean, readable, inside the original text's area, and matches the original
   look (colour, outline, size).
3. The preview also proves the image re-encodes. A text op that spills outside its rect raises an error.

## Spec
```json
{
  "file": "_Data/<Folder>/<Name>_LZ.NCBR",        // NitroFS path of the NCBR/NCGR (as listed by tools/romfs.py)
  "palette": "_Data/<Folder>/<Name>.NCLR",          // optional; default = same base name + .NCLR
  "screen": "_Data/<Folder>/<Name>.NSCR",           // only for tiled backgrounds (NCGR + NSCR)
  "cells": "_Data/<Folder>/<Name>.NCER", "cell": 0, // only for OBJ images (NCGR/NCBR + NCER)
  "ops": [ ... ]
}
```
(The `//` notes above are explanations only: real spec files are plain JSON without comments.)
Without "screen"/"cells" the file must be a linear bitmap (most `*_TEX*_LZ.NCBR`).
Optional `"preview_zoom": 2`. A `"_note"` key is ignored and can hold your remarks.

Ops (coordinates are pixels in the orig.png; rect = [x, y, w, h]):
- `{"op":"fill","rect":[..],"color":"#rrggbb"|"transparent"}` - flat fill (erase text on a flat box / transparent area).
- `{"op":"erase","rect":[..],"colors":["#rrggbb",..],"tolerance":24}` - replace pixels of the listed colours (the
  text and its outline) by the nearest other pixel on the same row; for text over gradients/artwork.
- `{"op":"copy","from":[x,y,w,h],"to":[x,y]}` - copy a clean patch of background over the text.
- `{"op":"text","rect":[..],"text":"...","font":"f12"|"f10"|"<file>.ttf:<px>","color":"#rrggbb",
   "outline":"#rrggbb","shadow":"#rrggbb","align":"left|center|right","valign":"top|middle|bottom",
   "lineh":13,"wrap":true,"bold":false}`
  - f12 / f10: the game's own 12 px / 10 px fonts (pixel-perfect, best for small body text and labels).
  - TTF from C:/Windows/Fonts, drawn without anti-aliasing: arialbd.ttf, arialnb.ttf (narrow bold, for tight
    labels), verdanab.ttf, tahomabd.ttf, comicbd.ttf / comicz.ttf (cute bold / bold italic, for pink title-style
    text), segoeuib.ttf, trebucbd.ttf, ariblk.ttf, impact.ttf. Sizes ~9-20 px.
  - Colours snap to the nearest palette entry (for 16-colour images, within that area's palette bank).
- `{"op":"layout","dat":"_Data/<Folder>/<Name>.dat","index":i,"rect":[x0,y0,x1,y1]}` - the `.dat` beside a
  `*_TEX*` texture lists the rectangles (inclusive) the game cuts out of the texture to draw. If the English needs a
  wider area, draw it in free (transparent) texture space next to the original and widen that rect. Only widen to
  the right/down; keep x1,y1 <= 255.

## Which kind of spec
List a folder's files with `python -X utf8 -c "import sys; sys.path.insert(0,'tools'); import romfs; r,i=romfs.load(); print(sorted(p for p in i if p.startswith('_Data/<Folder>/')))"`.
- `<Name>.NCER` exists -> OBJ image: `"cells": "_Data/<Folder>/<Name>.NCER"` (+ `"cell": n` if the NCER has several
  cells; try 0, 1, ...). Works for NCGR and NCBR.
- else `<Name>.NSCR` exists -> background: `"screen": ...`.
- else -> plain bitmap.
- Palette = `<Name>.NCLR` by default. Exceptions: TomokiMonitor uses `Monitor_Pltt.NCLR` (Monitor_Load_* ->
  `Monitor_Load_Pltt.NCLR`, Monitor_Save_* -> `Monitor_Save_Pltt.NCLR`). If an image renders with wrong colours, look
  for a shared NCLR in the same folder.
- Many files carry identical text (e.g. 22 result banners). You may generate those spec files with a small Python
  script kept in your scratchpad (not in tools/), as long as you preview-check several of them.

## Pack entries
`_Data/EventList/EVENTLIST_PACK.bin`, `_Data/Gallery/ALBUM_PACK.bin`, `_Data/BackUp/BACKUP_PACK.bin` are archives:
address an entry as `"<pack path>#<index>"` in file/palette/screen/cells/dat fields. `python -X utf8 tools/pack.py list
<pack>` lists entries (RGCN = image, RLCN = palette, RCSN = screen, RECN = cells, other = texture .dat);
`tools/pack.py dump <pack>` renders each image to work/gfx/<PACKNAME>/<index>.png. An image is usually followed by its
palette and screen/cells/dat, e.g. EVENTLIST_PACK #15 image, #16 cells, #17 palette. Put pack specs under
gfx/edits/<PACKNAME>/.

## Known limits of gfxedit
- 8 bpp OBJ cells that pick one of several 256-colour palettes (OAM palette field, e.g. TomokiMonitor `*_Pltt`) are
  previewed/colour-matched against palette 0; pick colours accordingly and say so in `_note`.
- 512-wide screens (two 32x32 NSCR blocks) are read as one 64-wide map.
- TTF fonts are the Windows fonts of the build machine; a spec using a font missing elsewhere won't build there.

## Rules
- Translate faithfully but short; UI labels in Title Case; never abbreviate glossary names/terms unless the space
  truly can't fit them (report those).
- Keep the original's style: same text colour, same outline colour, similar size and weight. Erase every Japanese
  pixel you replace (no leftovers next to the English).
- Don't touch artwork outside the text areas. Don't edit any file except your spec files.
