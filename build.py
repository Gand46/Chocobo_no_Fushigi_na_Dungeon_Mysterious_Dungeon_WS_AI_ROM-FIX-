#!/usr/bin/env python3
"""Rebuild the cumulative English + HF20 TEST image from the verified Japanese ROM.
This is a reconstructed editable patch source, not the original game source code.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import struct
from pathlib import Path
from tools.bps_codec import create, apply
ROOT = Path(__file__).resolve().parent
PATCH_NAME = 'Chocobo_EN_v1.1_HF20_TEST_JP_CCAA4853.bps'


def digest(data: bytes | bytearray) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: str):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def replace_checked(data: bytearray, edits: list[dict]) -> set[int]:
    allowed: set[int] = set()
    for entry in edits:
        start = int(entry['offset'], 0)
        old, new = bytes.fromhex(entry['before']), bytes.fromhex(entry['after'])
        end = start + len(old)
        if not old or len(old) != len(new) or start < 0 or end > len(data):
            raise ValueError(f'Invalid edit extent: {entry}')
        if any(pos in allowed for pos in range(start, end)):
            raise ValueError(f'Overlapping source edits at {start:06X}')
        if bytes(data[start:end]) != old:
            raise ValueError(f'Preimage mismatch at {start:06X}; refusing an unsafe edit')
        data[start:end] = new
        allowed.update(range(start, end))
    return allowed


def build(source: bytes, verify_release: bool = True) -> tuple[bytes, bytes, dict]:
    manifest = load_json('manifest.json')
    expected = manifest['original']
    if len(source) != expected['bytes'] or digest(source) != expected['sha256']:
        raise ValueError('Wrong base ROM. Expected Japanese CRC32 CCAA4853 and the SHA-256 in manifest.json.')
    legacy_recipe = load_json('src/legacy_translation_ranges.json')
    image = bytearray(source)
    replace_checked(image, legacy_recipe['edits'])
    if digest(image) != manifest['legacy_english_normalized']['sha256']:
        raise ValueError('Legacy recipe does not reconstruct the pinned English v1.1 image')
    legacy = bytes(image)
    allowed = replace_checked(image, load_json('src/corrections.json')['edits'])
    image[-2:] = struct.pack('<H', sum(image[:-2]) & 65535)
    allowed.update((len(image) - 2, len(image) - 1))
    changed = {i for i, (a, b) in enumerate(zip(legacy, image)) if a != b}
    if not changed <= allowed or len(image) != len(source):
        raise ValueError('Unexpected binary change or ROM size change')
    if verify_release and digest(image) != manifest['target']['sha256']:
        raise ValueError('HF20 release hash mismatch; use --development only for intentional source edits')
    metadata = b'Chocobo English v1.1 + HF20 TEST; JP CCAA4853; HF1 text fixes + Lafoss guard/projectile/native damage + Whistle repair + protected save CRC/commit + text terminator + scoped D3 floor cache + user-provided main English logo v0.1 with native animation; native-grid subtitle for legibility; HF11 G05:M002 repair; HF12 QA17 M3 eleven bounded dialogue/template repairs; HF13 QA18 M4 five bounded pagination and spacing repairs; HF14 QA19 V1 36 references corrected in same-bank verified free space; HF15 QA20 V2 74 bilingual and presentation repairs + TitanSaddle residual glyph + three fused equipment text repairs + Sleep Card name; HF16 QA21 V3 64 story repairs and two equipment property wording repairs; HF17 QA22 V4 43 G09 dialogue repairs; HF18 QA23 V5 65 G14 labels and two Chip name reconciliations; HF19 QA24 money selector, debug wording, temporal suffixes and two bestiary names; HF20 QA26 fourteen aesthetic spacing/reflow repairs, native font preserved; TEST limitations documented'
    patch = create(source, bytes(image), metadata)
    if apply(source, patch) != bytes(image):
        raise ValueError('BPS round-trip failure')
    report = {'source_sha256': digest(source), 'legacy_sha256': digest(legacy),
              'target_sha256': digest(image), 'bps_sha256': digest(patch),
              'changed_bytes_vs_legacy': len(changed), 'unexpected_changed_offsets': len(changed - allowed),
              'checksum': f'{sum(image[:-2]) & 65535:04X}', 'roundtrip': 'PASS',
              'release_hash_verified': verify_release}
    return bytes(image), patch, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('japanese_rom', type=Path)
    parser.add_argument('--out', type=Path, default=ROOT / 'build')
    parser.add_argument('--development', action='store_true', help='Allow intentional new correction edits; output is not the pinned HF20 release')
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    try:
        rom, bps, result = build(args.japanese_rom.read_bytes(), not args.development)
        destinations = {args.out / 'Chocobo_EN_v1.1_HF20_TEST.ws': rom,
                        args.out / PATCH_NAME: bps,
                        args.out / 'build_result.json': (json.dumps(result, indent=2) + '\n').encode()}
        for path in destinations:
            if path.resolve() == args.japanese_rom.resolve():
                raise ValueError('Never overwrite the source ROM')
            if path.exists() and not args.overwrite:
                raise ValueError(f'Output already exists: {path}; use a new folder or --overwrite')
        args.out.mkdir(parents=True, exist_ok=True)
        for path, payload in destinations.items():
            path.write_bytes(payload)
        print(json.dumps(result, indent=2))
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f'Build failed: {exc}\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
