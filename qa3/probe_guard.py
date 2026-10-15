from pathlib import Path
import struct,json
p=Path('private_roms/Chocobo_EN_v1.1_HF1_TEST.ws');b=bytearray(p.read_bytes());ed=[]
def jmp(src,dst):return b'\xe9'+struct.pack('<H',(dst-src-3)&65535)
def put(off,old,new):
 assert b[off:off+len(old)]==old;assert len(old)==len(new)
 ed.append(dict(offset=hex(off),before=old.hex(),after=new.hex()));b[off:off+len(new)]=new
stub=b'\x83\xf9\xff\x75\x03'+jmp(0xfd45,0x44cc)+b'\xbf\x90\x01\xc1\xe1\x02'+jmp(0xfd4e,0x4398)
put(0x154392,bytes.fromhex('bf9001c1e102'),jmp(0x4392,0xfd40)+b'\x90'*3)
put(0x15fd40,b'\xff'*len(stub),stub)
b[-2:]=struct.pack('<H',sum(b[:-2])&65535)
Path('private_roms/PROBE_GUARD.ws').write_bytes(b);Path('qa3/probe_guard_edits.json').write_text(json.dumps(ed,indent=2))
