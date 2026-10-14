"""Global term replacement in text/en, re-wrapping any message whose lines no longer fit.

python -X utf8 tools/retext.py "old=>new" ["old2=>new2" ..] [--dry]
Matches are literal and case-sensitive. A message whose wrapped lines exceed 216 px after the change is re-wrapped
from scratch (its line breaks are joined with spaces first).
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import batches  # noqa: E402
import textfmt  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')


def main(pairs, dry):
    adv = batches.adv_table()
    total = 0
    for p in sorted(glob.glob(os.path.join(ROOT, 'text', 'en', '*', '*.json'))):
        with open(p, encoding='utf-8') as f:
            d = json.load(f)
        changed = False
        for k, v in d.items():
            new = v
            for a, b in pairs:
                new = new.replace(a, b)
            if new == v:
                continue
            if any(textfmt.width(ln, adv) > textfmt.LINE_PX for ln in new.split('\n')):
                head = ''
                if new.startswith('　\n'):
                    head, new = '　\n', new[2:]
                new = head + textfmt.wrap(new.replace('\n', ' '), adv)
            print(f'{os.path.relpath(p, ROOT)}#{k}: {new!r}')
            d[k] = new
            changed = True
            total += 1
        if changed and not dry:
            with open(p, 'w', encoding='utf-8', newline='\n') as f:
                f.write('{\n' + ',\n'.join(f'"{k}": {json.dumps(v)}' for k, v in d.items()) + '\n}\n')
    print(total, 'strings changed' + (' (dry run)' if dry else ''))


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--dry']
    main([tuple(a.split('=>', 1)) for a in args], '--dry' in sys.argv)
