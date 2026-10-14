"""Stack the dialogue box (and name plate) of distinct frames into tall PNG pages for reading English in QA.

python -X utf8 tools/boxes.py work/qa/run [--from N --to M] [--per 10] [--zoom 2]
Writes <run>/boxes_NN.png; a frame is kept when its box differs from the previous kept one.
"""
import argparse
import glob
import os
import re

from PIL import Image, ImageChops, ImageStat

BOX = (0, 312, 256, 384)  # name plate + 3-line box on the bottom screen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('run')
    ap.add_argument('--from', dest='lo', type=int, default=0)
    ap.add_argument('--to', dest='hi', type=int, default=10 ** 9)
    ap.add_argument('--per', type=int, default=10)
    ap.add_argument('--zoom', type=int, default=2)
    ap.add_argument('--diff', type=float, default=6.0)
    a = ap.parse_args()
    frames = []
    for p in sorted(glob.glob(os.path.join(a.run, 'f[0-9]*.png'))):
        n = int(re.search(r'f(\d+)', os.path.basename(p)).group(1))
        if a.lo <= n <= a.hi:
            frames.append((n, p))
    kept, prev = [], None
    for n, p in frames:
        im = Image.open(p).convert('RGB').crop(BOX)
        if prev is None or sum(ImageStat.Stat(ImageChops.difference(im, prev)).mean) > a.diff:
            kept.append((n, im))
        prev = im
    w, h = (BOX[2] - BOX[0]) * a.zoom, (BOX[3] - BOX[1]) * a.zoom
    for page in range(0, len(kept), a.per):
        chunk = kept[page:page + a.per]
        sheet = Image.new('RGB', (w, h * len(chunk)))
        for i, (n, im) in enumerate(chunk):
            sheet.paste(im.resize((w, h), Image.NEAREST), (0, i * h))
        out = os.path.join(a.run, f'boxes_{page // a.per:02d}.png')
        sheet.save(out)
        print(out, ' '.join(str(n) for n, _ in chunk))


if __name__ == '__main__':
    main()
