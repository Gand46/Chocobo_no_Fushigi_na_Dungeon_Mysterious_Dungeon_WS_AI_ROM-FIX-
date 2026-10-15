#!/usr/bin/env python3
"""Read-only, data-first validation of Chocobo WS Rev 2 raw SRAM.

Markers establish recognition, not integrity. Exact reference comparisons must
refer to the SAME save generation; a later legitimate save can differ.
No recovery or mutation of input files is performed. Python standard library.
"""
from pathlib import Path
import argparse
import hashlib
import json
import struct

SRAM_SIZE = 0x8000
LIVE = 0x6BD8
STORED = 0x75B6
LENGTH = 0x9D4
DELTA = STORED - LIVE
MARKERS = slice(0x75AC, 0x75B4)
PAYLOAD = slice(STORED, STORED + LENGTH)


def read_save(path):
    data = Path(path).read_bytes()
    if len(data) != SRAM_SIZE:
        raise ValueError(f'{path}: expected 32768-byte raw SRAM, got {len(data)}; not a ROM or savestate')
    return data


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fields(data, live=False):
    delta = 0 if live else DELTA
    def u8(a): return data[a + delta]
    def u16(a): return struct.unpack_from('<H', data, a + delta)[0]
    return {
        'level': u8(0x6C7D), 'hp': u16(0x6C7E), 'max_hp': u16(0x6C80),
        'inventory_capacity_observed': u8(0x6C9E), 'dungeon': u8(0x7301),
        'current_floor': u16(0x7303), 'resume_destination': u16(0x7305),
        'story_flags_730A': f'{u16(0x730A):04X}',
        'story_flags_730C': f'{u16(0x730C):04X}',
        'captured_counter_7530': u16(0x7530),
    }


def changed_ranges(a, b, base=0):
    """Inclusive ranges, preserving all actual differences without ellipsis."""
    ranges = []
    for i, (x, y) in enumerate(zip(a, b)):
        if x == y:
            continue
        address = base + i
        if ranges and address == ranges[-1][1] + 1:
            ranges[-1][1] = address
        else:
            ranges.append([address, address])
    return [{'start': f'{lo:04X}', 'end': f'{hi:04X}', 'bytes': hi-lo+1}
            for lo, hi in ranges]


def compare(data, reference):
    marker_equal = data[MARKERS] == reference[MARKERS]
    payload_equal = data[PAYLOAD] == reference[PAYLOAD]
    return {
        'scope': 'Markers and stored payload of the same save generation',
        'status': 'PASS' if marker_equal and payload_equal else 'FAIL',
        'markers_equal': marker_equal, 'payload_equal': payload_equal,
        'payload_changed_bytes': sum(a != b for a, b in zip(data[PAYLOAD], reference[PAYLOAD])),
        'payload_changed_ranges': changed_ranges(reference[PAYLOAD], data[PAYLOAD], STORED),
        'marker_changed_ranges': changed_ranges(reference[MARKERS], data[MARKERS], MARKERS.start),
        'whole_sram_equal': data == reference,
        'excluded': 'Live/work SRAM and 75B4..75B5: runtime validity cache/padding, not the stored payload',
        'interpretation': 'A difference is not by itself proof of accidental corruption; verify generation provenance',
    }


def generation_check(data, old, new):
    a, b, c = old[PAYLOAD], new[PAYLOAD], data[PAYLOAD]
    if a == b:
        return {'status': 'REFERENCES_IDENTICAL', 'mixed': False}
    if c == a:
        return {'status': 'EXACT_OLD_GENERATION', 'mixed': False}
    if c == b:
        return {'status': 'EXACT_NEW_GENERATION', 'mixed': False}
    low, high = 0, LENGTH
    for i, (av, bv, cv) in enumerate(zip(a, b, c)):
        if cv != av and cv != bv:
            return {'status': 'OTHER_CHANGE', 'mixed': False}
        if av != bv:
            if cv == bv:
                low = max(low, i + 1)
            else:
                high = min(high, i)
    mixed = low <= high
    return {
        'status': 'CONSISTENT_WITH_INTERRUPTED_PREFIX_COPY' if mixed else 'NON_PREFIX_MIX',
        'mixed': mixed,
        'possible_copied_byte_count': [low, high] if mixed else None,
        'interpretation': 'New prefix and old suffix; causal proof requires a native write trace',
    }


def inspect(data, reference=None, next_reference=None, loaded_copy=None):
    if len(data) != SRAM_SIZE:
        raise ValueError('Expected 32768-byte raw SRAM')
    normal = data[0x75B0:0x75B4] == b'n_c1'
    alternate = data[0x75AC:0x75B0] == b'A_C1'
    result = {
        'schema': 'chocobo-ws-save-data-v1', 'read_only': True,
        'raw_bytes': len(data), 'raw_sha256': sha(data),
        'marker_check': {'normal': normal, 'alternate': alternate,
                         'recognized_by_observed_marker_rule': normal or alternate,
                         'raw_hex': data[MARKERS].hex()},
        'payload': {'start': '75B6', 'end_inclusive': '7F89',
                    'bytes': LENGTH, 'sha256': sha(data[PAYLOAD])},
        'saved_fields_observed': fields(data),
        'semantic_warnings': [],
        'integrity_without_reference': 'NOT_VALIDATED',
        'event_and_gameplay_coherence': 'NOT_VALIDATED',
        'notes': [
            'Known markers are not a checksum or a backup.',
            'Two marker locations refer to one shared payload.',
            'Fields are decoded from observed code/runtime. No complete legal-value schema is claimed.',
            'Current floor and resume destination may legitimately differ or change during load.',
        ],
    }
    f = result['saved_fields_observed']
    # Branch E1:58E2..5906 and native writer 18C88E agree on these bits.
    # These are necessary selectors, not a complete story/event schema.
    flag_a = int(f['story_flags_730A'], 16)
    flag_c = int(f['story_flags_730C'], 16)
    selected = 3 if flag_c & 4 else (2 if flag_a & 0x80 else 1)
    if f['dungeon'] in (1, 2, 3):
        result['resume_selector_check'] = {
            'status': 'PASS' if selected == f['dungeon'] else 'FAIL',
            'stored_dungeon': f['dungeon'], 'script_selected_dungeon': selected,
            'scope': 'Selection branch E1:58E2..5906 only; natural event progression NOT_VALIDATED',
        }
        if selected != f['dungeon']:
            result['semantic_warnings'].append('Dungeon ID disagrees with the observed resume script flags')
        if f['dungeon'] == 3 and not flag_a & 0x80:
            result['semantic_warnings'].append('Dungeon 3 lacks bit0080 written by native progress routine; selector can still choose 3')
    else:
        result['resume_selector_check'] = {'status': 'N/A', 'reason': 'Town or unmodeled dungeon value'}
    if f['hp'] > f['max_hp']:
        result['semantic_warnings'].append('HP exceeds max HP; investigate context, do not auto-repair')
    if f['max_hp'] == 0:
        result['semantic_warnings'].append('Zero max HP; incomplete/empty data is possible')
    if not any(data[PAYLOAD]) or set(data[PAYLOAD]) == {255}:
        result['semantic_warnings'].append('Uniform empty/erased payload')
    if reference is not None:
        result['reference_sha256'] = sha(reference)
        result['reference_comparison'] = compare(data, reference)
    if next_reference is not None:
        if reference is None:
            raise ValueError('--next-reference requires --reference (older generation)')
        result['next_reference_sha256'] = sha(next_reference)
        result['generation_comparison'] = generation_check(data, reference, next_reference)
    if loaded_copy is not None:
        actual = loaded_copy[LIVE:LIVE+LENGTH]
        result['native_load_copy'] = {
            'scope': 'Snapshot at 9000:033F, immediately after native copy; before post-load changes',
            'status': 'PASS' if actual == data[PAYLOAD] else 'FAIL',
            'expected_bytes': LENGTH,
            'equal_bytes': sum(a == b for a, b in zip(actual, data[PAYLOAD])),
            'changed_ranges_live': changed_ranges(data[PAYLOAD], actual, LIVE),
            'live_fields': fields(loaded_copy, live=True),
        }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('save', type=Path)
    parser.add_argument('--reference', type=Path, help='Trusted raw SRAM of the same save, or older generation with --next-reference')
    parser.add_argument('--next-reference', type=Path, help='Known complete newer generation to diagnose a mixture')
    parser.add_argument('--loaded-copy', type=Path, help='Raw SRAM captured exactly at native copy exit 9000:033F')
    args = parser.parse_args()
    try:
        result = inspect(read_save(args.save),
                         read_save(args.reference) if args.reference else None,
                         read_save(args.next_reference) if args.next_reference else None,
                         read_save(args.loaded_copy) if args.loaded_copy else None)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    result['file'] = args.save.name
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
