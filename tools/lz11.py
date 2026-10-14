"""Nintendo LZ11 (header 0x11) decompress / compress (greedy, window 4096)."""


def decompress(d):
    assert d[0] == 0x11
    n = d[1] | d[2] << 8 | d[3] << 16
    pos = 4
    if n == 0:
        n = int.from_bytes(d[4:8], 'little')
        pos = 8
    out = bytearray()
    while len(out) < n:
        flags = d[pos]
        pos += 1
        for bit in range(8):
            if len(out) >= n:
                break
            if not flags & (0x80 >> bit):
                out.append(d[pos])
                pos += 1
                continue
            b = d[pos]
            ind = b >> 4
            if ind == 0:
                length = ((b & 0xF) << 4 | d[pos + 1] >> 4) + 0x11
                disp = ((d[pos + 1] & 0xF) << 8 | d[pos + 2]) + 1
                pos += 3
            elif ind == 1:
                length = ((b & 0xF) << 12 | d[pos + 1] << 4 | d[pos + 2] >> 4) + 0x111
                disp = ((d[pos + 2] & 0xF) << 8 | d[pos + 3]) + 1
                pos += 4
            else:
                length = ind + 1
                disp = ((b & 0xF) << 8 | d[pos + 1]) + 1
                pos += 2
            for _ in range(length):
                out.append(out[-disp])
    return bytes(out)


def compress(src):
    n = len(src)
    out = bytearray([0x11, n & 0xFF, n >> 8 & 0xFF, n >> 16 & 0xFF])
    i = 0
    index = {}
    while i < n:
        flag_pos = len(out)
        out.append(0)
        flags = 0
        for bit in range(8):
            if i >= n:
                break
            best_len, best_disp = 0, 0
            key = src[i:i + 3]
            if len(key) == 3:
                for j in reversed(index.get(key, [])[-64:]):
                    disp = i - j
                    if disp > 4096:
                        break
                    ln = 3
                    while ln < 0x10110 and i + ln < n and src[j + ln] == src[i + ln]:
                        ln += 1
                    if ln > best_len:
                        best_len, best_disp = ln, disp
            if best_len >= 3:
                flags |= 0x80 >> bit
                L, D = best_len, best_disp - 1
                if L <= 0x10:
                    out += bytes([(L - 1) << 4 | D >> 8, D & 0xFF])
                elif L <= 0x110:
                    L -= 0x11
                    out += bytes([L >> 4, (L & 0xF) << 4 | D >> 8, D & 0xFF])
                else:
                    L -= 0x111
                    out += bytes([0x10 | L >> 12, L >> 4 & 0xFF, (L & 0xF) << 4 | D >> 8, D & 0xFF])
                step = best_len
            else:
                out.append(src[i])
                step = 1
            for k in range(i, i + step):
                if k + 3 <= n:
                    index.setdefault(src[k:k + 3], []).append(k)
            i += step
        out[flag_pos] = flags
    while len(out) % 4:
        out.append(0)
    return bytes(out)


if __name__ == '__main__':
    import os
    for t in (b'', b'a', b'abcabcabcabc' * 50, os.urandom(3000), bytes(70000)):
        assert decompress(compress(t)) == t
    print('ok')
