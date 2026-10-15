#!/usr/bin/env python3
"""Inspect raw 32 KiB Chocobo SRAM, or export a verified HF4 save to legacy.
CRC consistency is not proof of gameplay validity. Export always creates a copy.
"""
import argparse, binascii, hashlib, json
from pathlib import Path

PAYLOAD = slice(0x75B6, 0x7F8A)

def inspect(data):
    if len(data) != 32768:
        raise ValueError('Expected exactly 32768 bytes of raw SRAM, not a savestate')
    legacy = protected = 0
    for address, prefix, bit in [(0x75B0, b'n_c', 1), (0x75AC, b'A_C', 2)]:
        if data[address:address+3] == prefix:
            if data[address+3] == ord('1'): legacy |= bit
            if data[address+3] == ord('4'): protected |= bit
    mask, commit = data[0x7F8A:0x7F8C]
    stored = int.from_bytes(data[0x7F8C:0x7F8E], 'little')
    complement = int.from_bytes(data[0x7F8E:0x7F90], 'little')
    calculated = binascii.crc_hqx(data[0x75B6:0x7F8B], 0xFFFF)
    crc_ok = stored == calculated and complement == (stored ^ 0xFFFF)
    protected_ok = bool(protected) and commit == 0xA5 and protected & mask == protected and crc_ok
    valid = legacy | (protected if protected_ok else 0)
    return dict(sha256=hashlib.sha256(data).hexdigest(), legacy_mask=legacy,
                protected_mask=protected, committed_mask=mask, commit=commit,
                crc_stored=f'{stored:04X}', crc_calculated=f'{calculated:04X}',
                crc_and_complement_match=crc_ok, protected_valid=protected_ok,
                native_valid_mask=valid, integrity='HF4_CRC_VALID' if protected_ok else
                ('LEGACY_NOT_INTEGRITY_CHECKED' if legacy else 'NOT_VALID'),
                warning='No recovery of overwritten data; CRC is not a gameplay or security guarantee.')

def export_legacy(data):
    result = inspect(data)
    if not result['protected_valid'] or result['legacy_mask']:
        raise ValueError('Export requires a valid HF4 protected save without mixed legacy markers')
    out = bytearray(data)
    for address, bit in [(0x75B3, 1), (0x75AF, 2)]:
        if result['protected_mask'] & bit: out[address] = ord('1')
    out[0x7F8A:0x7F90] = bytes(6)
    return bytes(out)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('save', type=Path)
    parser.add_argument('--export-legacy', type=Path, metavar='NEW_COPY.sav')
    args = parser.parse_args()
    try:
        data = args.save.read_bytes()
        result = inspect(data)
        if args.export_legacy:
            if args.save.resolve() == args.export_legacy.resolve():
                raise ValueError('Never overwrite the input save')
            converted = export_legacy(data)
            with args.export_legacy.open('xb') as target: target.write(converted)
            result['exported_copy'] = str(args.export_legacy)
            result['export_sha256'] = hashlib.sha256(converted).hexdigest()
        print(json.dumps(result, indent=2))
        return 0 if result['native_valid_mask'] else 2
    except (ValueError, OSError) as error:
        parser.exit(1, str(error)+'\n')

if __name__ == '__main__': raise SystemExit(main())
