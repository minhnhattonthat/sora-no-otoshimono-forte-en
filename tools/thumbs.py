"""Labelled thumbnail contact sheets of work/gfx/<folder>/*.png for the graphics survey.

python -X utf8 tools/thumbs.py [--size 160] [--per 24] -> work/gfx/_sheets/<folder>_NN.png
"""
import glob
import os
import sys

from PIL import Image, ImageDraw


def main(size=160, per=24, cols=6):
    out = os.path.join('work', 'gfx', '_sheets')
    os.makedirs(out, exist_ok=True)
    for d in sorted(glob.glob(os.path.join('work', 'gfx', '*'))):
        if d.endswith('_sheets') or not os.path.isdir(d):
            continue
        files = sorted(glob.glob(os.path.join(d, '*.png')))
        for page in range(0, len(files), per):
            chunk = files[page:page + per]
            rows = -(-len(chunk) // cols)
            sheet = Image.new('RGB', (cols * size, rows * (size + 12)), (40, 40, 40))
            dr = ImageDraw.Draw(sheet)
            for i, f in enumerate(chunk):
                im = Image.open(f).convert('RGB')
                im.thumbnail((size, size))
                x, y = i % cols * size, i // cols * (size + 12)
                sheet.paste(im, (x, y + 12))
                dr.text((x + 2, y), os.path.basename(f)[:-4][:26], fill=(255, 255, 0))
            sheet.save(os.path.join(out, f'{os.path.basename(d)}_{page // per:02d}.png'))
    print('\n'.join(sorted(os.listdir(out))))


if __name__ == '__main__':
    main()
