"""Verify/re-emit the project-owned guard without requiring an assembler."""
import json,struct
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def jmp(src,dst):return b"\xe9"+struct.pack("<H",(dst-src-3)&65535)
hook=jmp(0x4392,0xfd40)+b"\x90"*3
stub=bytes.fromhex("83f9ff7503")+jmp(0xfd45,0x44cc)+bytes.fromhex("bf9001c1e102")+jmp(0xfd4e,0x4398)
edits={int(e["offset"],0):e for e in json.loads((root/"src/corrections.json").read_text())["edits"]}
assert bytes.fromhex(edits[0x154392]["after"])==hook
assert bytes.fromhex(edits[0x15fd40]["after"])==stub
print(json.dumps({"hook_hex":hook.hex(),"stub_hex":stub.hex(),"source_matches_recipe":True},indent=2))
