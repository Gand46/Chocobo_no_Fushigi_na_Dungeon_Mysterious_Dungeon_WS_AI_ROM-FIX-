#!/usr/bin/env python3
"""Verify the data-first method against captured native operations and fault fixtures."""
from pathlib import Path
import argparse
import json
import hashlib
from validate_chocobo_save import inspect, read_save, LENGTH, LIVE, PAYLOAD, MARKERS

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--runs', type=Path, required=True)
p.add_argument('--fixtures', type=Path, required=True)
a = p.parse_args()
checks = []

def check(name, condition, evidence):
    if not condition:
        raise AssertionError(name)
    checks.append({'check': name, 'status': 'PASS', 'evidence': evidence})

baseline = read_save(a.fixtures/'baseline.sav')
marker_bad = read_save(a.fixtures/'marker_bad.sav')
payload_bad = read_save(a.fixtures/'payload_level2.sav')
r = inspect(marker_bad, baseline)
check('Marker damage is distinct from payload loss',
      not r['marker_check']['recognized_by_observed_marker_rule'] and
      r['reference_comparison']['payload_equal'] and not r['reference_comparison']['markers_equal'],
      'QA5 single-byte marker mutation')
r = inspect(payload_bad, baseline)
check('Plausible altered level is detected against trusted same-generation data',
      r['marker_check']['normal'] and r['reference_comparison']['payload_changed_bytes'] == 1,
      'QA5 level 1 to 2; native loader previously accepted it')

s = a.runs/'q6_save_overwrite'
old = read_save(s/'generation_A.sav')
new = read_save(s/'generation_B.sav')
cut = read_save(s/'cut_0200.sav')
before = read_save(s/'before_copy.sav')
after = read_save(s/'after_copy.sav')
check('Native save copies all 2516 live bytes exactly', before[LIVE:LIVE+LENGTH] == after[PAYLOAD],
      '9000:0373 source snapshot vs 9000:037F destination snapshot')
check('Captured write interruption is exactly new prefix plus old suffix',
      cut[PAYLOAD] == new[PAYLOAD][:200] + old[PAYLOAD][200:] and cut[PAYLOAD] not in (old[PAYLOAD], new[PAYLOAD]),
      'Snapshot on native payload write 200; remainder kept from generation A')
r = inspect(cut, old, new)
check('Mixed generation detected despite valid marker',
      r['marker_check']['normal'] and r['generation_comparison']['mixed'],
      r['generation_comparison'])
check('Complete old/new generations are not misclassified as mixtures',
      not inspect(old, old, new)['generation_comparison']['mixed'] and
      not inspect(new, old, new)['generation_comparison']['mixed'], 'Boundary controls')

run_names = ['q6_cold_complete', 'q6_cold_interrupted', 'q6_jp_cold_interrupted',
             'q6_d2_event_data', 'q6_d2_correct_flag']
copy_count = 0
for name in run_names:
    root = a.runs/name
    metadata = json.loads((root/'run.json').read_text())
    check(name + ': bounded run completed', metadata['completed'] and metadata['exit'] == 0, metadata['rom_sha256'])
    saved = read_save(root/'input_save.sav')
    copies = sorted(root.glob('load_*_copied.sav'))
    check(name + ': two native load copies observed', len(copies) == 2, [x.name for x in copies])
    for path in copies:
        copy = read_save(path)
        rr = inspect(saved, loaded_copy=copy)['native_load_copy']
        check(name + ': ' + path.name, rr['status'] == 'PASS' and rr['equal_bytes'] == LENGTH, rr)
        copy_count += 1
    final = read_save(root/'native_save_after.sav')
    rr = inspect(final, saved)['reference_comparison']
    check(name + ': stored data and markers survive load', rr['status'] == 'PASS',
          {'whole_sram_equal': rr['whole_sram_equal'], 'payload_equal': rr['payload_equal']})

complete = read_save(a.runs/'q6_cold_complete/native_save_after.sav')
r = inspect(complete, new)
check('Runtime SRAM changes do not produce a false payload-corruption result',
      r['reference_comparison']['status'] == 'PASS' and not r['reference_comparison']['whole_sram_equal'],
      '75B4 validity cache changes 0 to 1; working SRAM also changes')

bad_d2 = read_save(a.runs/'q6_d2_event_data/input_save.sav')
good_d2 = read_save(a.runs/'q6_d2_correct_flag/input_save.sav')
check('Data validator detects wrong dungeon progression bit',
      inspect(bad_d2)['resume_selector_check']['status'] == 'FAIL', 'QA5 fixture used 8000 instead of 0080 at 730A')
check('Corrected flag agrees with native script selection',
      inspect(good_d2)['resume_selector_check']['status'] == 'PASS' and
      read_save(a.runs/'q6_d2_correct_flag/sram.bin')[0x7301] == 2,
      'QA6 uses native branch E1:58F9; second-dungeon boss dialogue at floor 60')
try:
    inspect(b'bad')
except ValueError:
    malformed_rejected = True
else:
    malformed_rejected = False
check('Truncated data rejected before interpretation', malformed_rejected, 'Three-byte invalid input')

report = {
    'status': 'PASS', 'checks': checks, 'check_count': len(checks),
    'native_load_copies_checked': copy_count, 'bytes_per_copy': LENGTH,
    'scope': 'Exact native copies, recognition, baseline integrity and known selector bits; not all event semantics',
    'natural_forum_save_loss_trigger': 'NOT_VALIDATED',
    'rom_fix_added': False,
}
print(json.dumps(report, indent=2, ensure_ascii=False))
