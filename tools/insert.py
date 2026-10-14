"""Insert text/en into the ROM (called by build.py), plus the VWF font/code patch.

text/en/<group>/<name>.json = {"<id>": "English"}; ids missing there keep the original Japanese bytes.
MARKER=1 in the environment replaces every msg with its id instead (marker build), e.g. "[c00_31_01_000#6]".
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import ndspy.rom  # noqa: E402
import arm9text  # noqa: E402
import extract  # noqa: E402
import gfxedit  # noqa: E402
import misctext  # noqa: E402
import romfs  # noqa: E402
import script  # noqa: E402
import textfmt  # noqa: E402
import vwf  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..')


def load_en(key):
    p = os.path.join(ROOT, 'text', 'en', key + '.json')
    if not os.path.exists(p):
        return {}
    with open(p, encoding='utf-8') as f:
        return {int(k): v for k, v in json.load(f).items()}


def rewrite(path, data, repl):
    """repl(i, kind, old_bytes) -> new bytes, or for a msg a list of bytes = several boxes.
    Walks strings in extract.strings order. Extra boxes become '06 05 <clone of the 03/a9>' after the original
    (06 = wait for the player, 05 = clear; the game's own pattern after almost every message)."""
    n = [0]

    def walk(cmds):
        out = []
        for c in cmds:
            out.append(c)
            tup = [i for i, p in enumerate(c.parts) if isinstance(p, tuple)]
            if c.op in (0x03, 0xa9):
                kinds = ['name', 'msg'] if len(tup) == 2 else ['msg']
            else:
                kinds = ['choice'] * len(tup)
            more = []
            for i, k in zip(tup, kinds):
                new = repl(n[0], k, c.parts[i][1])
                n[0] += 1
                if isinstance(new, list):
                    new, more = new[0], new[1:]
                c.parts[i] = ('s', new)
            for chunk in more:
                parts = list(c.parts)
                parts[tup[-1]] = ('s', chunk)
                out += [script.Cmd(0x06, []), script.Cmd(0x05, []), script.Cmd(c.op, parts)]
        return out

    if path.startswith('_Data/Script/Trial/'):
        blocks, tail = script.parse_pack(data)
        return script.build_pack([(h, walk(cmds)) for h, cmds in blocks], tail)
    sid, unk, cmds, tail = script.parse(data)
    return script.build(sid, unk, walk(cmds), tail)


SFX = re.compile(r'^\{1F\}\{[0-9A-F]{2}\}')


def center_sfx(line):
    """'{1F}{xx}' indents a line by (xx - 0x0B) * 6 px (callback 0x0208F0EC); the Japanese values center Japanese
    text, so recompute xx to center the English."""
    m = SFX.match(line)
    if not m:
        return line
    w = textfmt.width(line[m.end():], ADV)
    xx = 0x0B + max(0, round((textfmt.LINE_PX - w) / 2 / 6))
    return '{1F}{%02X}' % xx + line[m.end():]


def boxes(en, kind):
    """English msg -> bytes, or a list of bytes when it needs more than one 3-line box."""
    if kind != 'msg':
        return textfmt.encode_en(en)
    lines = [center_sfx(ln) for ln in textfmt.wrap(en, ADV).split('\n')]
    if len(lines) <= textfmt.MAX_LINES:
        return textfmt.encode_en('\n'.join(lines))
    nbox = -(-len(lines) // textfmt.MAX_LINES)
    cuts = [round(len(lines) * k / nbox) for k in range(nbox + 1)]  # balanced: 4 lines -> 2+2, 5 -> 3+2
    return [textfmt.encode_en('\n'.join(lines[cuts[k]:cuts[k + 1]])) for k in range(nbox)]


def marker_text(key, i):
    return f'[{key.split("/")[1]}#{i}]'


ADV = None  # VWF advance table, set by apply()


def load_names():
    with open(os.path.join(ROOT, 'text', 'en', 'names.json'), encoding='utf-8') as f:
        return {int(k): v for k, v in json.load(f).items() if not k.startswith('_')}


def chara_names(data, names):
    """Rebuild CharaName.dat with English names (records are length-prefixed; nothing points into the file)."""
    recs = extract.chara_names(data)
    out = bytearray(data[:1])
    for i, (pos, old) in enumerate(recs):
        end = recs[i + 1][0] if i + 1 < len(recs) else len(data)
        new = names[i].encode('ascii') if i in names else old
        out += bytes([len(new)]) + new + data[pos + 1 + len(old):end]
    return bytes(out)


def apply(rom, ids, marker=None):
    global ADV
    marker = os.environ.get('MARKER') == '1' if marker is None else marker
    fid = ids['_Data/font/Font1212.NFTR']
    font, table = vwf.font_widths(rom.read(fid))
    rom.replace(fid, font)
    ADV = table

    for path, fid in sorted(ids.items()):
        key = extract.key_of(path)
        if not key:
            continue
        en = load_en(key)

        def repl(i, kind, old):
            if marker and kind == 'msg':
                return textfmt.encode_en(marker_text(key, i))
            return boxes(en[i], kind) if i in en else old

        rom.replace(fid, rewrite(path, rom.read(fid), repl))

    fid = ids['_Data/AdvTalk/CharaName.dat']
    rom.replace(fid, chara_names(rom.read(fid), load_names()))
    misctext.apply(rom, ids)
    gfxedit.apply(rom, ids)

    r = ndspy.rom.NintendoDSRom.fromFile(romfs.ROM)
    rom.set_arm9(vwf.patch_arm9(r.arm9, r.arm9RamAddress, r.arm9CodeSettingsPointerAddress, table,
                                arm9text.patch))
