"""In-place NDS file replacement: keeps the original layout, so an unedited ROM rebuilds byte-identical.

A replaced file goes back into its own slot when it fits, else it is appended after the last used byte (the
original image is padded with 0xFF to 128 MiB). The FAT entry, header 0x80 (used ROM size) and header CRC follow.
"""
import struct

ALIGN = 0x200


def crc16(data):
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
    return crc


class Rom:
    def __init__(self, path):
        self.data = bytearray(open(path, 'rb').read())
        self.fat = struct.unpack_from('<I', self.data, 0x48)[0]
        self.used = struct.unpack_from('<I', self.data, 0x80)[0]

    def span(self, fid):
        return struct.unpack_from('<II', self.data, self.fat + 8 * fid)

    def read(self, fid):
        s, e = self.span(fid)
        return bytes(self.data[s:e])

    def replace(self, fid, new):
        s, e = self.span(fid)
        if bytes(self.data[s:e]) == new:
            return
        if len(new) > e - s:
            s = (self.used + ALIGN - 1) // ALIGN * ALIGN
            if s + len(new) > len(self.data):
                raise ValueError(f'ROM full: file {fid} ({len(new)} bytes) does not fit')
            self.used = s + len(new)
            struct.pack_into('<I', self.data, 0x80, self.used)
        else:
            self.data[s:e] = b'\xff' * (e - s)
        self.data[s:s + len(new)] = new
        struct.pack_into('<II', self.data, self.fat + 8 * fid, s, s + len(new))
        struct.pack_into('<H', self.data, 0x15E, crc16(self.data[:0x15E]))

    def set_arm9(self, new):
        """Replace the (compressed) arm9 in place; the 12-byte nitrocode footer moves to stay right after it."""
        off, size = struct.unpack_from('<II', self.data, 0x20)[0], struct.unpack_from('<I', self.data, 0x2C)[0]
        footer = bytes(self.data[off + size:off + size + 12])
        limit = struct.unpack_from('<I', self.data, 0x50)[0]  # arm9 overlay table follows
        if off + len(new) + 12 > limit:
            raise ValueError(f'arm9 grew past the overlay table by {off + len(new) + 12 - limit} bytes')
        self.data[off:limit] = b'\xff' * (limit - off)
        self.data[off:off + len(new) + 12] = new + footer
        struct.pack_into('<I', self.data, 0x2C, len(new))
        struct.pack_into('<H', self.data, 0x15E, crc16(self.data[:0x15E]))

    def save(self, path):
        open(path, 'wb').write(self.data)


if __name__ == '__main__':
    assert crc16(b'123456789') == 0x4B37  # CRC-16/MODBUS check value
    print('ok')
