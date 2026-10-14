"""gfxedit image paste and mask erase on a tiny fake canvas (no ROM needed)."""
import os
import sys
from types import SimpleNamespace

from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))
import gfxedit  # noqa: E402


def canvas(rows):
    cv = gfxedit.Canvas.__new__(gfxedit.Canvas)
    cv.char = SimpleNamespace(bpp=8)
    cv.pal = [(0, 255, 0), (255, 255, 255), (0, 0, 255), (128, 128, 255)] + [(0, 0, 0)] * 252
    cv.bank = None
    cv.idx = [list(r) for r in rows]
    cv.h, cv.w = len(rows), len(rows[0])
    return cv


def test_image_and_mask_erase(tmp_path):
    img = Image.new('RGBA', (3, 1))
    img.putpixel((0, 0), (250, 250, 250, 255))  # opaque -> nearest white
    img.putpixel((1, 0), (255, 255, 255, 128))  # half white over blue -> blend
    img.putpixel((2, 0), (0, 0, 255, 100))  # faint over transparent -> skipped
    img.save(tmp_path / 'p.png')
    cv = canvas([[2, 2, 0, 2]])
    gfxedit.op_image(cv, {'src': str(tmp_path / 'p.png'), 'to': [0, 0]})
    assert cv.idx == [[1, 3, 0, 2]]

    m = Image.new('LA', (2, 1))
    m.putpixel((0, 0), (255, 255))
    m.save(tmp_path / 'm.png')
    cv = canvas([[2, 1, 1, 3]])
    gfxedit.op_erase(cv, {'mask': str(tmp_path / 'm.png'), 'to': [1, 0]})
    assert cv.idx == [[2, 2, 1, 3]]  # x=1 (masked) takes its nearest unmasked row neighbour
