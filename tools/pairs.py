"""Reviewer input: JP/EN pairs with context.

python -X utf8 tools/pairs.py sample N SEED OUT.txt   -> N random runs of 12 consecutive lines from all scripts
python -X utf8 tools/pairs.py key story/ch00_000 OUT.txt -> one whole script
Format: '>> key#id [speaker] | JP' then '   EN' (line breaks shown as ' / ').
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
import batches  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')


def load(key):
    p = os.path.join(ROOT, 'text', 'en', key + '.json')
    if not os.path.exists(p):  # scripts without strings have no English file
        return {}
    with open(p, encoding='utf-8') as f:
        return {int(k): v for k, v in json.load(f).items()}


def fmt(key, ln, en):
    j = ln['ja'].replace('\n', ' / ')
    e = en.get(ln['id'], '(missing)').replace('\n', ' / ')
    return f'>> {key}#{ln["id"]} [{ln["spk"] or "-"}] | {j}\n   {e}\n'


def main():
    ja = dict(batches.ja_files())
    out = []
    if sys.argv[1] == 'sample':
        n, seed, path = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        rnd = random.Random(seed)
        keys = sorted(ja)
        for _ in range(n):
            key = rnd.choice(keys)
            lines = ja[key]
            s = rnd.randrange(max(1, len(lines) - 12))
            en = load(key)
            out.append(f'--- {key} lines {s}-{s + 11}\n' + ''.join(fmt(key, ln, en) for ln in lines[s:s + 12]))
    else:
        key, path = sys.argv[2], sys.argv[3]
        en = load(key)
        out = [fmt(key, ln, en) for ln in ja[key]]
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(out))
    print(path)


if __name__ == '__main__':
    main()
