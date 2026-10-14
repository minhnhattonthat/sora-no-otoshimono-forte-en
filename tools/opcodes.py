"""Static analysis of the script command classes in arm9: opcode -> parse() reads.

The interpreter (0x2091B6C) reads u8 opcode, the factory at 0x208FCEC news a command object per opcode, then
calls vtable[3] = parse(), which pulls its arguments with read(this->ctx, dst, n) at 0x2091A54.
Prints, per opcode, the parse function and the sequence of read sizes ('?' = non-constant size).
Needs work/arm9.bin (decompressed; see docs/re/script.md).
"""
import struct
import sys
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

BASE = 0x2000000
SWITCH = 0x208FD0C  # case 0 of the factory's addls-pc table (0x208FD08 is the default branch)
NOPS = 0xE6
READ = 0x2091A54
ALLOC = 0x202E2A0

d = open('work/arm9.bin', 'rb').read()
md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
md.detail = False


def u32(a):
    return struct.unpack_from('<I', d, a - BASE)[0]


def insns(a, n=200):
    return list(md.disasm(d[a - BASE:a - BASE + n * 4], a))


def target(i):
    return int(i.op_str.lstrip('#'), 16)


def lit(i):
    # ldr rX, [pc, #imm]
    imm = int(i.op_str.split('#')[1].rstrip(']'), 16)
    return u32(i.address + 8 + imm)


def ctor_of(case):
    br = insns(case, 1)[0]
    if br.mnemonic != 'b':
        return None
    seen_alloc = False
    for i in insns(target(br), 20):
        if i.mnemonic == 'bl':
            if target(i) == ALLOC:
                seen_alloc = True
            elif seen_alloc:
                return target(i)
        if i.mnemonic in ('pop', 'b'):  # popeq after a failed alloc is not the end
            break
    return None


def vtable_of(ctor):
    vt = None
    for i in insns(ctor, 40):
        if i.mnemonic == 'ldr' and '[pc' in i.op_str:
            v = lit(i)
            if 0x20C0000 <= v < 0x20D8000:
                vt = v
        if i.mnemonic == 'pop' or (i.mnemonic == 'bx' and i.op_str == 'lr'):
            break
    return vt


def reads(fn):
    """Constant read sizes in order; walks straight-line code, follows tail-call b/bx ip to READ."""
    out, regs, branches, ip = [], {}, 0, None
    for i in insns(fn, 120):
        m, ops = i.mnemonic, i.op_str
        a = [x.strip() for x in ops.split(',')]
        if m == 'mov' and len(a) == 2:
            regs[a[0]] = int(a[1][1:], 0) if a[1].startswith('#') else regs.get(a[1])
        elif m == 'ldr' and ops.startswith('ip, [pc'):
            ip = lit(i)
        elif m == 'bx' and ops == 'ip' and ip == READ:
            out.append(regs.get('r2', '?'))
            return out, branches, 'tail'
        elif m == 'bl':
            t = target(i)
            if t == READ:
                out.append(regs.get('r2') if regs.get('r2') is not None else '?')
            else:
                out.append(f'call{t:07x}')
            for r in ('r0', 'r1', 'r2', 'r3', 'ip'):
                regs.pop(r, None)
        elif a and a[0] in regs and m not in ('str', 'strb', 'strh', 'cmp', 'tst', 'push') and not m.startswith('b'):
            regs[a[0]] = None  # any other write (incl. conditional movne) makes it unknown
        elif m.startswith('b') and m not in ('bl', 'bx', 'blx', 'bic', 'bics'):
            branches += 1
        if m.startswith('pop') and 'pc' in ops or (m == 'bx' and ops == 'lr'):
            if not m.startswith('pop') or m == 'pop':
                return out, branches, 'ret'
    return out, branches, 'long'


def table():
    rows = []
    for op in range(NOPS):
        c = ctor_of(SWITCH + 4 * op)
        vt = vtable_of(c) if c else None
        p = u32(vt + 0xC) if vt else None
        r = reads(p) if p else ([], 0, '-')
        rows.append((op, c, vt, p) + r)
    return rows


if __name__ == '__main__':
    for op, c, vt, p, rd, br, how in table():
        f = lambda x: f'{x:07x}' if x else '-------'
        print(f'{op:02x} ctor {f(c)} vt {f(vt)} parse {f(p)} br{br} {how:4} {rd}')
