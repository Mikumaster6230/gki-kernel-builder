#!/usr/bin/env python3
"""Android boot.img repacker - replace kernel in boot.img"""
import struct, sys, os

def repack(boot_path, kernel_path, out_path):
    with open(boot_path, 'rb') as f:
        data = f.read()
    with open(kernel_path, 'rb') as f:
        new_kernel = f.read()

    assert data[:8] == b'ANDROID!', "Not a valid boot.img"

    hdr_ver = struct.unpack_from('<I', data, 40)[0]
    old_ksz = struct.unpack_from('<I', data, 8)[0]
    new_ksz = len(new_kernel)

    print(f"Bootimg v{hdr_ver}, old kernel={old_ksz} bytes, new kernel={new_ksz} bytes")

    if hdr_ver >= 3:
        hdr_sz = struct.unpack_from('<I', data, 20)[0] or 4096
        # Everything after kernel (ramdisk + any vendor extras)
        tail = data[hdr_sz + old_ksz:]
        hdr = bytearray(data[:hdr_sz])
        struct.pack_into('<I', hdr, 8, new_ksz)
        out = bytes(hdr) + new_kernel + tail
    else:
        pg = struct.unpack_from('<I', data, 36)[0] or 2048
        rd_sz = struct.unpack_from('<I', data, 16)[0]
        koff = pg
        rd_off = ((koff + old_ksz + pg - 1) // pg) * pg
        ramdisk = data[rd_off:rd_off + rd_sz]
        rest = data[rd_off + rd_sz:]
        hdr = bytearray(data[:pg])
        struct.pack_into('<I', hdr, 8, new_ksz)
        out = bytes(hdr) + b'\x00' * (pg - len(hdr))
        out += new_kernel
        kpad = ((new_ksz + pg - 1) // pg) * pg - new_ksz
        if kpad: out += b'\x00' * kpad
        out += ramdisk + rest

    with open(out_path, 'wb') as f:
        f.write(out)
    print(f"Done! {out_path} ({len(out)} bytes)")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: py repack_boot.py <boot.img> <new_kernel> [output]")
        sys.exit(1)
    repack(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 'new-boot.img')
