#!/usr/bin/env python3
"""Independent CRC oracle vs actual HF4 CPU validator, every recorded write prefix."""
import argparse, csv, hashlib, json
from pathlib import Path
from chocobo_save import inspect, PAYLOAD

def verify(root):
    results = {}
    for kind, source in [('new','q7_save_new'),('rewrite','q7_save_rewrite'),('alternate','q7_alternate_save')]:
        p = root/source
        old = (p/'generation_A.sav').read_bytes()
        new = (p/'generation_B.sav').read_bytes()
        data = bytearray(old)
        events = list(csv.DictReader((p/'writes.csv').open()))
        rows = list(csv.DictReader((root/f'q7_matrix2_{kind}'/'native_results.csv').open()))
        assert len(rows) == len(events)+1
        accepted = []
        for i, row in enumerate(rows):
            if i:
                event = events[i-1]
                address = int(event['address'],16)-0x10000
                value = int(event['value'],16)
                assert 0 <= value <= 255
                data[address] = value
            expected = inspect(data)['native_valid_mask']
            assert int(row['write_prefix']) == i and int(row['valid_mask']) == expected, (kind,i,row,expected)
            if expected:
                assert data[PAYLOAD] in (old[PAYLOAD],new[PAYLOAD]), (kind,i,'MIXED ACCEPTED')
                accepted.append(i)
        assert data[0x75AC:0x7F90] == new[0x75AC:0x7F90]
        results[kind] = dict(cases=len(rows), accepted_prefixes=accepted, mixed_accepted=0)
    rows = list(csv.DictReader((root/'q7_matrix2_crc_complete'/'native_results.csv').open()))
    assert len(rows) == 145 and int(rows[0]['valid_mask']) == 1
    assert all(int(row['valid_mask']) == 0 for row in rows[1:])
    results['crc_mutations'] = dict(valid_control=1,rejected=144,total=145)
    return {'status':'PASS_SYNTHETIC', 'interruption_cases':sum(r['cases'] for k,r in results.items() if k!='crc_mutations'),
            'results':results,'scope':'Native CPU validator with DS=1000 harness; exact write prefixes; CRC oracle is Python binascii.crc_hqx. No natural power-loss claim.'}

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('runs',type=Path);a=p.parse_args()
    print(json.dumps(verify(a.runs),indent=2))
