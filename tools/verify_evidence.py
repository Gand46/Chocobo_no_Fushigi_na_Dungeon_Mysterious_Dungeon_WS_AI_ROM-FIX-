#!/usr/bin/env python3
"""Recheck recorded resource reads against privately rebuilt variants.
This verifies artifact consistency, not the truth of untested natural scenarios.
"""
import argparse,csv,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from build import build,replace_checked,load_json
p=argparse.ArgumentParser(description=__doc__);p.add_argument('japanese_rom',type=Path);a=p.parse_args()
try:
    jp=a.japanese_rom.read_bytes();hf,patch,report=build(jp)
    en=bytearray(jp);replace_checked(en,load_json('src/legacy_translation_ranges.json')['edits'])
    hf1=bytearray(en)
    replace_checked(hf1,[e for e in load_json('src/corrections.json')['edits'] if not e['id'].startswith(('PROPERTY_', 'ITEM_', 'LAFOSS_', 'WHISTLE_', 'SAVE_', 'LAFOSS_LAST_', 'TEXT_', 'FLOOR_','TITLE_', 'TEXT_', 'FLOOR_','TITLE_'))])
    hf1[-2:]=(sum(hf1[:-2])&65535).to_bytes(2,'little')
    hf2=bytearray(en)
    replace_checked(hf2,[e for e in load_json('src/corrections.json')['edits'] if not e['id'].startswith(('PROPERTY_', 'ITEM_', 'WHISTLE_', 'SAVE_', 'LAFOSS_LAST_', 'TEXT_', 'FLOOR_','TITLE_'))])
    hf2[-2:]=(sum(hf2[:-2])&65535).to_bytes(2,'little')
    hf3=bytearray(en)
    replace_checked(hf3,[e for e in load_json('src/corrections.json')['edits'] if not e['id'].startswith(('PROPERTY_', 'ITEM_', 'SAVE_', 'LAFOSS_LAST_', 'TEXT_', 'FLOOR_','TITLE_'))])
    hf3[-2:]=(sum(hf3[:-2])&65535).to_bytes(2,'little')
    variants={'JP':jp,'EN_v1.1':bytes(en),'HF1_TEST':bytes(hf1),'HF2_TEST':bytes(hf2),'HF3_TEST':bytes(hf3)}
    counts={}
    for variant,rom in variants.items():
        path=ROOT/'evidence/runs'/f'{variant}_resources'
        meta=json.loads((path/'run.json').read_text())
        if meta['rom_sha256']!=hashlib.sha256(rom).hexdigest():raise ValueError('Recorded ROM hash mismatch')
        rows=list(csv.DictReader((path/'resource_reads.csv').open()))
        for row in rows:
            start=int(row['target_rom'],16)
            if int.from_bytes(rom[start:start+2],'little')!=int(row['value'],16):
                raise ValueError(f'{variant}: trace value mismatch at {start:06X}')
        if len(set(r['case'] for r in rows))!=10:raise ValueError('Incomplete resource coverage')
        counts[variant]=len(rows)
    actual=(ROOT/'patches/Chocobo_EN_v1.1_HF9_TEST_JP_CCAA4853.bps').read_bytes()
    if actual!=patch:raise ValueError('Distributed patch differs from reproducible build')
    print(json.dumps({'resource_words_verified':counts,'distributed_patch_byte_identical':True,'build':report},indent=2))
except (OSError,ValueError,KeyError) as exc:p.exit(1,f'Verification failed: {exc}\n')
