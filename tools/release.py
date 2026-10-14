"""Release package: build, xdelta patch, verify by re-applying to the clean ROM, README with hashes, zip.

python -X utf8 tools/release.py VERSION     -> release/SoraOtoForte_DreamySeason_EN_<VERSION>.zip
Local only: publishing is the user's call.
"""
import hashlib
import os
import subprocess
import sys
import zipfile
import zlib

sys.path.insert(0, os.path.dirname(__file__))
import build  # noqa: E402
import romfs  # noqa: E402

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
NAME = 'SoraOtoForte_DreamySeason_EN'


def hashes(path):
    d = open(path, 'rb').read()
    return {'size': len(d), 'crc32': '%08X' % (zlib.crc32(d) & 0xFFFFFFFF), 'md5': hashlib.md5(d).hexdigest(),
            'sha1': hashlib.sha1(d).hexdigest()}


README = """Sora no Otoshimono Forte: Dreamy Season - English translation patch {version}
(Heaven's Lost Property Forte: Dreamy Season, Nintendo DS, Kadokawa Shoten)

Unofficial fan translation. No ROMs are distributed; you need your own dump of the Japanese game.

HOW TO APPLY
Use xdelta3 (or Delta Patcher / xdelta UI) to apply {patch} to the original ROM:
  xdelta3 -d -s "original.nds" {patch} "Sora no Otoshimono Forte (English).nds"

Original ROM (must match):
  Japanese release, game code TFLJ
  Size:  {o[size]} bytes
  CRC32: {o[crc32]}
  MD5:   {o[md5]}
  SHA-1: {o[sha1]}
Patched ROM:
  CRC32: {p[crc32]}
  SHA-1: {p[sha1]}

WHAT'S TRANSLATED
- All story, character-event and touch-mode dialogue (about 20,000 lines), choices and speaker names.
- Menus, help pages, tutorial boards, status screens, titles/emblems, event and location names, save/load
  screens, character profiles (attract mode), staff roll, system messages.
- New variable-width font rendering for the dialogue box.

NOTES
- Names follow the official English anime (Funimation's Heaven's Lost Property); honorifics are kept.
- Start a new game or load your existing save; savestates made with the Japanese ROM will not carry the new text.
- Tested in DeSmuME. Voice acting is unchanged (Japanese).

KNOWN ISSUES
- The title-screen logo is the original Japanese logo.
- Some staff-roll name readings are best guesses.
- Play-tested through the start of Episode 4; later episodes, endings and Tomoki Training were checked
  as text and images but not played. Please report problems.

Credits: translation and hacking produced with AI assistance (Claude) under the direction of the project owner.
Thanks to Suu Minazuki, Kadokawa and seventh chord for the original game.
"""


def main(version):
    out_dir = os.path.join(ROOT, 'release')
    os.makedirs(out_dir, exist_ok=True)
    built = build.build(os.path.join(ROOT, 'build', 'sora-en.nds'))
    patch = f'{NAME}_{version}.xdelta'
    ppath = os.path.join(out_dir, patch)
    if os.path.exists(ppath):
        os.remove(ppath)
    subprocess.check_call(['xdelta3', '-e', '-9', '-S', 'djw', '-s', romfs.ROM, built, ppath])
    check = os.path.join(ROOT, 'work', 'release_check.nds')
    subprocess.check_call(['xdelta3', '-d', '-f', '-s', romfs.ROM, ppath, check])
    if open(check, 'rb').read() != open(built, 'rb').read():
        sys.exit('re-applied patch does not reproduce the build')
    o, p = hashes(romfs.ROM), hashes(built)
    readme = README.format(version=version, patch=patch, o=o, p=p)
    rpath = os.path.join(out_dir, 'README.txt')
    with open(rpath, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(readme)
    zpath = os.path.join(out_dir, f'{NAME}_{version}.zip')
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_STORED) as z:
        z.write(ppath, patch)
        z.write(rpath, 'README.txt')
    print(zpath, os.path.getsize(zpath), 'bytes; patched CRC32', p['crc32'])


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'v1.0')
