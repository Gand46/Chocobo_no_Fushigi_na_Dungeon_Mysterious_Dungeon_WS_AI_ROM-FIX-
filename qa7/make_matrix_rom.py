from pathlib import Path
import argparse,struct,json,hashlib
p=argparse.ArgumentParser();p.add_argument('rom',type=Path);p.add_argument('cases',type=int);p.add_argument('out',type=Path);a=p.parse_args()
b=bytearray(a.rom.read_bytes());parent=hashlib.sha256(b).hexdigest()
harness=bytes.fromhex('1e50b800108ed858b9')+struct.pack('<H',a.cases)+bytes.fromhex('9a72fb0090e2f91fcb')
assert b[0x19fc00:0x19fc00+len(harness)]==b'\xff'*len(harness)
assert b[0x1903b8:0x1903bd]==bytes.fromhex('e9b7f79090')
b[0x19fc00:0x19fc00+len(harness)]=harness;b[0x1903b8:0x1903bb]=b'\xe9'+struct.pack('<H',0xfc00-0x3bb)
b[-2:]=struct.pack('<H',sum(b[:-2])&65535);a.out.write_bytes(b)
a.out.with_suffix('.json').write_text(json.dumps({'purpose':'TEST HARNESS ONLY, not a playable release','parent_sha256':parent,'sha256':hashlib.sha256(b).hexdigest(),'cases':a.cases,'changes':['validator entry dispatches harness19FC00','harness saves DS, sets DS=1000 SRAM segment, calls release validator9000:FB72 for each case, restores DS','ROM checksum']},indent=2))
