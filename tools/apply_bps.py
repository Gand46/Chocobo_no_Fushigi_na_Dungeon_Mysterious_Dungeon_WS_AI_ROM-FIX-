#!/usr/bin/env python3
"""Apply a BPS with CRC checks. Never overwrite an existing file."""
import argparse
from pathlib import Path
from bps_codec import apply
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('base',type=Path);p.add_argument('patch',type=Path);p.add_argument('output',type=Path)
a=p.parse_args()
try:
    if a.output.exists(): raise ValueError('Output already exists; choose a new filename')
    data=apply(a.base.read_bytes(),a.patch.read_bytes())
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_bytes(data)
    print(f'Created {a.output}: {len(data)} bytes')
except (ValueError,OSError) as e:p.exit(1,f'Patch failed: {e}\n')
