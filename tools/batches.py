"""Translation batches: split text/ja into work/tl/<batch>.tsv, check an agent's output, merge into text/en.

python -X utf8 tools/batches.py split            # writes work/tl/bNNN.tsv + build/terms_bNNN.txt + work/tl/index.json
python -X utf8 tools/batches.py check b007       # validates work/tl/b007.out.tsv; prints OK or the problems
python -X utf8 tools/batches.py merge b007 [..]  # check, then write into text/en/<group>/<name>.json
python -X utf8 tools/batches.py fit "English text" [--form dlg|choice|name]   # dry-run wrap + widths
python -X utf8 tools/batches.py status           # translated / total

TSV in:  id<TAB>speaker<TAB>form<TAB>limit<TAB>Japanese   (' / ' = line break inside one box)
TSV out: id<TAB>English   (no manual breaks needed: insert word-wraps dialogue to 216 px x 3 lines;
         write '\\n' only to force one)
SFX boxes ("　\\n{1F}{xx}..." in Japanese) are shown without that prefix; merge puts it back.
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import textfmt  # noqa: E402

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
TL = os.path.join(ROOT, 'work', 'tl')
MAX_ENTRIES, MAX_CHARS = 150, 4500
SFX = re.compile(r'^　\n(\{1F\}\{[0-9A-F]{2}\})')
# Box limits (px) per form; dialogue from the width gate (docs/re/script.md). choice/name: see LIMITS notes there.
# dlg/narration: 3 lines per box; insert.py spills lines 4-6 into a second box, so 6 is the hard cap.
LIMITS = {'dlg': (textfmt.LINE_PX, 6), 'narration': (textfmt.LINE_PX, 6), 'choice': (200, 1), 'name': (72, 1)}
ALLOWED = set(chr(c) for c in range(0x20, 0x7f)) | {'\n', '♪', '☆', '♥'}


def adv_table():
    import romfs
    import vwf
    rom, ids = romfs.load()
    return vwf.font_widths(bytes(rom.files[ids['_Data/font/Font1212.NFTR']]))[1]


def ja_files():
    for p in sorted(glob.glob(os.path.join(ROOT, 'text', 'ja', '*', '*.json'))):
        key = os.path.relpath(p, os.path.join(ROOT, 'text', 'ja'))[:-5].replace('\\', '/')
        with open(p, encoding='utf-8') as f:
            yield key, json.load(f)['lines']


def form_of(line):
    if line['kind'] == 'msg':
        return 'dlg' if line['spk'] else 'narration'
    return line['kind']


def split():
    os.makedirs(TL, exist_ok=True)
    glossary = open(os.path.join(ROOT, 'glossary.md'), encoding='utf-8').read()
    rows = [r for r in glossary.splitlines() if r.startswith('| ') and not r.startswith('| JP') and '---' not in r]
    order = sorted(ja_files(), key=lambda kv: (kv[0].split('/')[0] != 'story', kv[0]))
    batches, cur, chars = [], [], 0
    for key, lines in order:
        for ln in lines:
            if cur and (len(cur) >= MAX_ENTRIES or chars + len(ln['ja']) > MAX_CHARS):
                batches.append(cur)
                cur, chars = [], 0
            cur.append((key, ln))
            chars += len(ln['ja'])
    batches.append(cur)
    index = {}
    for n, b in enumerate(batches):
        name = f'b{n:03d}'
        out = []
        for key, ln in b:
            ja = SFX.sub('', ln['ja'])
            px, rows_ = LIMITS[form_of(ln)]
            lim = '3 lines (max 6)' if rows_ == 6 else f'{px}px'
            out.append('\t'.join([f'{key}#{ln["id"]}', ln['spk'] or '-', form_of(ln), lim,
                                  ja.replace('\n', ' / ')]))
        with open(os.path.join(TL, name + '.tsv'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(out) + '\n')
        text = ''.join(ln['ja'] + ln['spk'] for _, ln in b)
        terms = [r for r in rows if any(t.strip() and t.strip() in text for t in r.split('|')[1].split('/'))]
        os.makedirs(os.path.join(ROOT, 'build'), exist_ok=True)
        with open(os.path.join(ROOT, 'build', f'terms_{name}.txt'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('| JP | EN | max | notes | Avoid |\n' + '\n'.join(terms) + '\n')
        index[name] = sorted({k for k, _ in b})
    with open(os.path.join(TL, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=0)
    print(len(batches), 'batches')


def read_in(name):
    rows = []
    with open(os.path.join(TL, name + '.tsv'), encoding='utf-8') as f:
        for line in f:
            if line.strip():
                rows.append(line.rstrip('\n').split('\t'))
    return rows


def read_out(name):
    p = os.path.join(TL, name + '.out.tsv')
    got = {}
    dup = []
    with open(p, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\r\n')
            if not line.strip():
                continue
            if '\t' not in line:
                dup.append(f'no tab: {line[:60]}')
                continue
            i, en = line.split('\t', 1)
            if i in got:
                dup.append(f'duplicate id {i}')
            got[i] = en.replace('\\n', '\n')
    return got, dup


def fit(en, form, adv):
    """-> (wrapped text, problems)"""
    px, maxl = LIMITS[form]
    probs = []
    if form in ('dlg', 'narration'):
        w = textfmt.wrap(en, adv, px)
        lines = w.split('\n')
        if len(lines) > maxl:
            probs.append(f'{len(lines)} lines > {maxl} (shorten)')
        for ln in lines:
            if textfmt.width(ln, adv) > px:
                probs.append(f'word too wide: {ln!r}')
        return w, probs
    if '\n' in en:
        probs.append('no line breaks in ' + form)
    if textfmt.width(en, adv) > px:
        probs.append(f'{textfmt.width(en, adv)}px > {px}px')
    return en, probs


def check(name, adv, quiet=False):
    rows = read_in(name)
    got, errs = read_out(name)
    want = [r[0] for r in rows]
    missing = [i for i in want if i not in got]
    extra = [i for i in got if i not in want]
    errs += [f'missing {i}' for i in missing] + [f'extra {i}' for i in extra]
    for i, spk, form, limit, ja in rows:
        if i not in got:
            continue
        en = got[i]
        bad = sorted({c for c in en if c not in ALLOWED})
        if bad:
            errs.append(f'{i}: non-ASCII {bad}')
            continue
        if not en.strip():
            errs.append(f'{i}: empty')
        if sorted(re.findall(r'\{[0-9A-F]{2}\}', ja)) != sorted(re.findall(r'\{[0-9A-F]{2}\}', en)):
            errs.append(f'{i}: control codes differ from JP {re.findall(r"{[0-9A-F]{2}}", ja)}')
        if re.search(r'\]\s?(st|nd|rd|th)\b', en):
            errs.append(f'{i}: ordinal suffix after a code')
        for p in fit(en, form, adv)[1]:
            errs.append(f'{i}: {p}')
    if not quiet:
        print('OK' if not errs else '\n'.join(errs))
    return errs


def merge(names, adv):
    by_key = {}
    for name in names:
        if check(name, adv, quiet=True):
            sys.exit(f'{name}: check fails; run: python -X utf8 tools/batches.py check {name}')
        got, _ = read_out(name)
        for i, en in got.items():
            key, n = i.rsplit('#', 1)
            by_key.setdefault(key, {})[int(n)] = en
    ja = dict(ja_files())
    for key, items in by_key.items():
        lines = {ln['id']: ln for ln in ja[key]}
        p = os.path.join(ROOT, 'text', 'en', key + '.json')
        cur = {}
        if os.path.exists(p):
            with open(p, encoding='utf-8') as f:
                cur = {int(k): v for k, v in json.load(f).items()}
        for n, en in items.items():
            ln = lines[n]
            en, _ = fit(en, form_of(ln), adv)
            m = SFX.match(ln['ja'])
            cur[n] = ('　\n' + m.group(1) + en) if m else en
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8', newline='\n') as f:
            f.write('{\n' + ',\n'.join(f'"{k}": {json.dumps(v)}' for k, v in sorted(cur.items())) + '\n}\n')
    print('merged', ', '.join(names))


def status():
    tot = done = 0
    for key, lines in ja_files():
        tot += len(lines)
        p = os.path.join(ROOT, 'text', 'en', key + '.json')
        if os.path.exists(p):
            with open(p, encoding='utf-8') as f:
                done += len(json.load(f))
    print(f'{done}/{tot} translated')


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'split':
        split()
    elif cmd == 'check':
        sys.exit(1 if check(sys.argv[2], adv_table()) else 0)
    elif cmd == 'merge':
        merge(sys.argv[2:], adv_table())
    elif cmd == 'fit':
        form = sys.argv[sys.argv.index('--form') + 1] if '--form' in sys.argv else 'dlg'
        w, probs = fit(sys.argv[2].replace('\\n', '\n'), form, adv_table())
        a = adv_table()
        for ln in w.split('\n'):
            print(f'{textfmt.width(ln, a):4d}px  {ln}')
        print('OK' if not probs else '\n'.join(probs))
    elif cmd == 'status':
        status()
