#!/usr/bin/env python3
"""Explicit synthetic alternate-save entry harness. Never distribute as playable ROM."""
import argparse, hashlib, json, struct
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('hf4_rom',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
b=bytearray(a.hf4_rom.read_bytes());parent=hashlib.sha256(b).hexdigest()
assert parent=='1ec449933e812c8e4f5e83b882db17b4c5f1ce3b5ea85527d9a1dd2a0891060d'
assert b[0x190367:0x19036c]==bytes.fromhex('e916f79090')
b[0x190367:0x19036c]=b'\xe9'+struct.pack('<H',(0xfa9b-0x36a)&65535)+b'\x90\x90'
b[-2:]=(sum(b[:-2])&65535).to_bytes(2,'little')
a.output.write_bytes(b)
a.output.with_suffix('.json').write_text(json.dumps({'parent_sha256':parent,'sha256':hashlib.sha256(b).hexdigest(),'purpose':'SYNTHETIC TEST ONLY: normal menu Save entry redirects to alternate wrapper, not native alternate event acquisition'},indent=2)+'\n')
