"""NitroFS access for the original ROM: path -> bytes, and a tiny CLI to extract one file."""
import sys
import ndspy.rom

ROM = 'rom/sora-forte.nds'


def walk(folder, prefix=''):
    for i, f in enumerate(folder.files):
        yield prefix + f, folder.firstID + i
    for name, sub in folder.folders:
        yield from walk(sub, prefix + name + '/')


def load(path=ROM):
    rom = ndspy.rom.NintendoDSRom.fromFile(path)
    return rom, dict(walk(rom.filenames))


if __name__ == '__main__':
    rom, ids = load()
    for p in sys.argv[1:]:
        sys.stdout.buffer.write(rom.files[ids[p]])
