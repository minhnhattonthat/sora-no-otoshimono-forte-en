"""Debug jumps for headless QA: run emu.py with tools/debug/jump.lua (+ autoplay.lua) on a fresh save.

    python -X utf8 tools/debug/dbg.py TARGET [--rom ROM] [--out DIR] [--frames N] [--sav F.dsv] [emu.py args..]

TARGET:
    ep1 .. ep6        start a New Game and replace the first story script with that episode's part 000, then autoplay
                      (Action Select, Event Select, communication scenes via Retry/Skip, next parts, Data Save).
    events1 .. events6  like epN with SKIP=1, but every side event of the episode plays in turn (EVENTS), then
                      the story goes on (170k frames; Ep4 = 18 events, ~90k frames)
    ending1 .. ending7  play ending N (Story/Chapter06/00N), the staff roll, then the Clear Data save screen.
    cleardata         ending7, then save Clear Data to slot 1: OUT/<rom>.dsv is a cleared save (use it with --sav;
                      Continue / Free Communication / New Game+ need it).
    title             title menu with Tomo-Colle (Album, Free Communication, Member Roster) and Options unlocked.
    album roster titles intimacy training events actions options help demo
                      open that screen instead of the title menu (scene ids in docs/re/debug.md), unlocks applied.
    scene:N           same, for raw scene id N.
Add --var SKIP=1 to give up every communication scene at its first GAME OVER, --var "EVENTS='3,10,1 ...'" to chain
side events (docs/re/debug.md).

Defaults: --rom work/run_final.nds, --out work/qa/dbg_<target>, --frames 60000 for ep/ending, 3000 for screens,
a blank battery save (the game initialises it), shots every 100 frames. Any other argument goes to emu.py as is
(e.g. --state-every 10000 --shot-every 50 --var SCRIPTLOG=1). The run's own save is left in OUT/<rom>.dsv: pass it
back with --sav to continue from what that run saved (e.g. Clear Data).
The ROM must not be rebuilt during a run (DeSmuME streams it): run from a copy, never from build/.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
EMU = os.path.join(ROOT, '.claude', 'skills', 'translate-retro-game', 'scripts', 'emu.py')
# Delusion Select (19) and the staff roll (11) opened this way show an empty screen: reach them in-game instead.
SCREENS = {'album': 13, 'roster': 14, 'titles': 23, 'intimacy': 22, 'training': 21, 'events': 20,
           'actions': 18, 'options': 12, 'help': 24, 'demo': 26}
# DeSmuME .dsv footer (after the 64 KB of raw backup data)
FOOTER = (b'|<--Snip above here to create a raw sav by excluding this DeSmuME savedata footer:'
          + bytes.fromhex('0000010000000100030000000200000000000100000000007c') + b'-DESMUME SAVE-|')


def blank_sav(path):
    with open(path, 'wb') as f:
        f.write(b'\xff' * 0x10000 + FOOTER)


def plan(target):
    """-> (lua vars, use autoplay, default frames)"""
    if target.startswith('ep') and target[2:].isdigit() and 1 <= int(target[2:]) <= 6:
        return {'STORY': "'%d,0'" % (int(target[2:]) - 1)}, True, 60000
    if target.startswith('ending') and target[6:].isdigit() and 1 <= int(target[6:]) <= 7:
        return {'STORY': "'6,%d'" % int(target[6:])}, True, 45000
    if target.startswith('events') and target[6:].isdigit() and 1 <= int(target[6:]) <= 6:
        ch = int(target[6:]) - 1  # every side event of the episode (text/en/chara/chCC_AA_BB_000.json), then story
        evs = sorted(f[2:10] for f in os.listdir(os.path.join(ROOT, 'text', 'en', 'chara'))
                     if f.startswith('ch%02d_' % ch))
        ids = ' '.join('%d,%d,%d' % tuple(int(p) for p in e.split('_')) for e in evs)
        return {'STORY': "'%d,0'" % ch, 'EVENTS': "'%s'" % ids, 'SKIP': '1'}, True, 170000
    if target == 'cleardata':
        return {'STORY': "'6,7'", 'SAVECLEAR': '1'}, True, 30000
    if target == 'title':
        return {'UNLOCK': '1'}, False, 2500
    if target.startswith('scene:'):
        return {'PROC': target[6:], 'UNLOCK': '1'}, False, 3000
    if target in SCREENS:
        return {'PROC': str(SCREENS[target]), 'UNLOCK': '1'}, False, 3000
    sys.exit('unknown target %r (see --help)' % target)


def main(argv):
    if not argv or argv[0] in ('-h', '--help'):
        print(__doc__)
        return 0
    target, rest = argv[0], argv[1:]
    opts = {'--rom': os.path.join(ROOT, 'work', 'run_final.nds'), '--out': None, '--frames': None, '--sav': None}
    extra = []
    i = 0
    while i < len(rest):
        if rest[i] in opts and i + 1 < len(rest):
            opts[rest[i]] = rest[i + 1]
            i += 2
        else:
            extra.append(rest[i])
            i += 1
    lua_vars, autoplay, frames = plan(target)
    out = opts['--out'] or os.path.join(ROOT, 'work', 'qa', 'dbg_' + target.replace(':', ''))
    os.makedirs(out, exist_ok=True)
    sav = opts['--sav']
    if not sav:
        sav = os.path.join(out, '_blank.dsv')
        blank_sav(sav)
    frames = int(opts['--frames'] or frames)
    # ~225 fps alone, ~40 fps with 4 runs in parallel; the timeout also catches the rare start-up hang
    # (DeSmuME stuck at frame ~40, no shots: just rerun)
    cmd = [sys.executable, '-X', 'utf8', EMU, opts['--rom'], '--out', out, '--sav', sav,
           '--frames', str(frames), '--timeout', str(300 + frames // 20)]
    if '--route-str' not in extra and '--route' not in extra:
        cmd += ['--route-str', '1 -']
    if '--shot-every' not in extra:
        cmd += ['--shot-every', '100']
    lua_vars.setdefault('SCENELOG', '1')
    if target == 'ep1':  # skip the tutorial menu; forcing choices elsewhere can pick a hidden option and soft-lock
        lua_vars.setdefault('CHOICE', "'last'")
    for k, v in lua_vars.items():
        cmd += ['--var', '%s=%s' % (k, v)]
    cmd += ['--script', os.path.join(HERE, 'jump.lua')]
    if autoplay:
        cmd += ['--script', os.path.join(HERE, 'autoplay.lua')]
    cmd += extra
    print(' '.join(cmd))
    return subprocess.call(cmd)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
