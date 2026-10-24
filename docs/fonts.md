# Fonts

Every font or glyph sheet the build reads ends up inside the released patch, so its licence must allow that. One row
per file; a font with no known licence doesn't go into a release.

All TTFs are read from `C:/Windows/Fonts` by `tools/gfxedit.py` (font files never shipped, only rendered pixels).

| File | Source (URL, version) | Licence | Redistributable in a patch | Used for | Changes made |
|---|---|---|---|---|---|
| `_Data/font/Font1212.NFTR`, `Font1010.NFTR` (spec font `f12`, `f10`) | the game | the publisher's | already in the game | dialogue VWF (tools/vwf.py), graphics specs | VWF widths; ☆ ♪ ♥ in ASCII slots ^ ` \| |
| `arialbd`, `arialbi`, `arialn`, `arialnb`, `ARIALNB`, `ARIALNBI`, `ARIALNI`, `comicbd`, `comicz`, `tahoma`, `tahomabd`, `trebucbi`, `segoeuib`, `seguisym` `.ttf` | Windows | Microsoft font EULA | as rendered glyphs only | gfx/edits specs: menus, titles, help, staff roll | - |
| `GILC____.TTF`, `HATTEN.TTF`, `AGENCYR.TTF`, `ARLRDBD.TTF` | Microsoft Office | Microsoft font EULA | as rendered glyphs only | gfx/edits specs | - |
| `CabinCondensed-Bold.ttf`, `CabinCondensed-SemiBold.ttf` | Google Fonts (Cabin Condensed), user-installed | OFL 1.1 | yes | gfx/edits specs | - |
| `UVNBanTay.TTF` (`~/AppData/Local/Microsoft/Windows/Fonts`) | UVN font pack, user-installed | unknown | unknown: check before publishing | English logo (gfx/edits/MainTitle/logo_en.py) | - |
