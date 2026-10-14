"""Generate the English game logo (Heaven's Lost Property / FORTE) as RGBA PNGs pasted by the logo specs.

python -X utf8 gfx/edits/MainTitle/logo_en.py   (needs rom/sora-forte.nds and the fonts named below)
-> gfx/edits/MainTitle/logo_en.png      224x136, replaces Title_Second_TEX00 rect 0 (same size/place as the JP logo)
   logo_en_fin.png   the same recoloured for StaffFin_Up
   logo_jp_mask.png  footprint of the Japanese logo (erased from the backgrounds before pasting)
   kana_mask.png     footprint of ドリーミーシーズン under "Dreamy Season"; dreamy.png = "Dreamy Season" alone
Lettering modelled on Funimation's "Heaven's Lost Property Forte" logo (tall hand-lettered white title with a blue
outline, small "SORA NO OTOSHIMONO", blue italic "FORTE"); the wing swoosh is the game's own art.
"""
import json
import os
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import gfxedit  # noqa: E402

W, H = 224, 136
SS = 4  # supersampling for the lettering
FONT = os.path.expanduser('~/AppData/Local/Microsoft/Windows/Fonts/UVNBanTay.TTF')
WHITE, BLUE, FRINGE = (255, 255, 255), (24, 115, 180), (90, 164, 238)


def original(full=False):
    """The Japanese logo (TEX00 rect 0) as RGBA; full=True: the whole 256x256 texture."""
    spec = {'file': '_Data/MainTitle/Title_Second_TEX00_LZ.NCBR', 'ops': []}
    cv = gfxedit.Canvas(spec, gfxedit.rom_files())
    im = cv.rgb().convert('RGBA')
    px = im.load()
    for y in range(cv.h):
        for x in range(cv.w):
            if cv.idx[y][x] == 0:
                px[x, y] = (0, 0, 0, 0)
    return im if full else im.crop((0, 0, W, H))


def swoosh(orig):
    """The game's wing swoosh without the Japanese lettering."""
    out = Image.new('RGBA', (W, H))
    op, px = orig.load(), out.load()
    for y in range(H):
        for x in range(W):
            wing = y < 62 and x >= 88
            band = y >= 101 and 34 <= x <= 182 and not (  # minus the tail of そ
                x < 45 and y < 103 or x < 40 and y < 108 or x < 36 and y < 115)
            if wing or band:
                px[x, y] = op[x, y]
    d = ImageDraw.Draw(out)
    # middle of the diagonal stroke (under the old と/し): cyan body with white edges
    body = [(113, 61), (127, 61), (122, 72), (116, 86), (110, 101), (88, 101), (95, 87), (103, 73)]
    d.polygon(body, fill=(16, 189, 246, 255))
    d.line([(112, 61), (102, 73), (94, 87), (87, 101)], fill=WHITE + (255,), width=2)
    d.line([(127, 61), (121, 72), (115, 86), (110, 101)], fill=WHITE + (255,), width=2)
    # band right of OTOSHIMONO: only the thin grey-blue line (rows 101-103) stays; FORTE sits on the sky
    d.rectangle((130, 104, 184, 121), fill=(0, 0, 0, 0))
    d.rectangle((128, 115, 129, 121), fill=(0, 0, 0, 0))
    return out


def outline_layers(mask, widths):
    """mask (L, supersampled) -> list of dilated masks, one per width (in 1x pixels)."""
    return [mask.filter(ImageFilter.MaxFilter(2 * round(w * SS) + 1)) if w else mask for w in widths]


def sticker(mask, fill, line, line_w, rim, rim_w, fringe):
    """White letters, blue outline, white rim, soft blue fringe (the style of the original logo lettering)."""
    f, l, r, e = outline_layers(mask, [0, line_w, line_w + rim_w, line_w + rim_w + 0.75])
    img = Image.new('RGBA', mask.size, (0, 0, 0, 0))
    for m, c in ((e, fringe), (r, rim), (l, line), (f, fill)):
        layer = Image.new('RGBA', mask.size, c + (255,))
        layer.putalpha(m)
        img.alpha_composite(layer)
    return img.resize((mask.width // SS, mask.height // SS), Image.LANCZOS)


def title_mask():
    """'Heaven's Lost Property' hand lettering, bouncy baseline, big capitals (as in the official logo)."""
    big = ImageFont.truetype(FONT, 60 * SS)
    small = ImageFont.truetype(FONT, 44 * SS)
    text = "Heaven's Lost Property"
    bounce = [0, 1, -1, 1, 0, -1, 1, 0, 0, 0, 1, -1, 0, 0, 0, -1, 1, 0, -1, 1, 0, 0]
    m = Image.new('L', (W * SS * 2, H * SS), 0)
    d = ImageDraw.Draw(m)
    x, base = 4 * SS, 52 * SS
    for ch, b in zip(text, bounce):
        f = big if ch.isupper() else small
        d.text((x, base + b * SS * 2), ch, font=f, fill=255, anchor='ls', stroke_width=SS // 2, stroke_fill=255)
        x +=f.getlength(ch) + (3 * SS if ch != ' ' else -2 * SS)
    return m.crop(m.getbbox())


def main():
    orig = original()
    out = swoosh(orig)
    t = title_mask()
    tw, th = 210, 40  # 1x box of the title (letters only, before the outline)
    t = t.resize((tw * SS, th * SS), Image.LANCZOS)
    pad = 4 * SS
    canvas = Image.new('L', (t.width + 2 * pad, t.height + 2 * pad))
    canvas.paste(t, (pad, pad))
    title = sticker(canvas, WHITE, BLUE, 1.25, WHITE, 1.5, FRINGE)
    out.alpha_composite(title, (5 - 4, 53 - 4))
    # FORTE: blue italic capitals on the band
    ff = ImageFont.truetype(FONT, 17 * SS)
    fm = Image.new('L', (60 * SS, 24 * SS))
    ImageDraw.Draw(fm).text((4 * SS, 18 * SS), 'FORTE', font=ff, fill=255, anchor='ls')
    fm = fm.transform(fm.size, Image.AFFINE, (1, 0.25, -5 * SS, 0, 1, 0), Image.BICUBIC)
    fm = fm.crop(fm.getbbox()).resize((43 * SS, 13 * SS), Image.LANCZOS)  # fill the band where フォルテ was
    canvas = Image.new('L', (fm.width + 4 * SS, fm.height + 4 * SS))
    canvas.paste(fm, (2 * SS, 2 * SS))
    forte = sticker(canvas, BLUE, BLUE, 0, WHITE, 1, WHITE)
    out.alpha_composite(forte, (133 - 2, 105 - 2))
    out.save(os.path.join(HERE, 'logo_en.png'))
    fin_tint(out).save(os.path.join(HERE, 'logo_en_fin.png'))

    def mask(img, grow):
        a = img.getchannel('A').point(lambda v: 255 if v else 0)
        a = a.filter(ImageFilter.MaxFilter(2 * grow + 1)) if grow else a
        return Image.merge('LA', (a, a))
    tex = original(full=True)
    kana = tex.crop((0, 151, 96, 160))  # ドリーミーシーズン under "Dreamy Season" (TEX00 rect 1, rows 15-23)
    dreamy = tex.crop((0, 136, 96, 151))  # "Dreamy Season" alone
    dreamy.save(os.path.join(HERE, 'dreamy.png'))
    mask(kana, 1).save(os.path.join(HERE, 'kana_mask.png'))
    # JP logo footprint (+1 px of baked edge blending in the backgrounds); backgrounds draw "Dreamy Season" at
    # logo + (95, 120) over it, so that part is left alone
    jp = mask(orig, 1)
    jp.paste((0, 0), (95, 120), mask(dreamy, 0).getchannel('A'))
    jp.save(os.path.join(HERE, 'logo_jp_mask.png'))


def fin_tint(img):
    """Recolour like StaffFin_Up, which is StaffRoll_Up through one affine RGB map (fitted on the two screens)."""
    import numpy as np
    f = gfxedit.rom_files()
    rgb = []
    for n in ('StaffRoll_Up', 'StaffFin_Up'):
        spec = {'file': f'_Data/StaffRoll/{n}_LZ.NCGR', 'screen': f'_Data/StaffRoll/{n}.NSCR', 'ops': []}
        rgb.append(np.asarray(gfxedit.Canvas(spec, f).rgb()).reshape(-1, 3).astype(float))
    m = np.linalg.lstsq(np.c_[rgb[0], np.ones(len(rgb[0]))], rgb[1], rcond=None)[0]
    a = np.asarray(img).astype(float)
    a[..., :3] = np.clip(np.c_[a[..., :3].reshape(-1, 3), np.ones(a.shape[0] * a.shape[1])] @ m, 0, 255).reshape(
        a.shape[0], a.shape[1], 3)
    return Image.fromarray(a.round().astype('uint8'))


if __name__ == '__main__':
    main()
