#!/usr/bin/env python3
"""Assemble the HF4 save guard and emit checked edits against pinned HF3.
The regular cumulative build uses the emitted recipe and needs only Python.
Editing assembly requires GNU binutils with x86 16-bit support (as/ld/objcopy/nm).
"""
from pathlib import Path
import argparse, hashlib, json, struct, subprocess, tempfile

P=argparse.ArgumentParser(description=__doc__)
P.add_argument('hf3_rom',type=Path)
P.add_argument('--assembly',type=Path,default=Path(__file__).with_name('save_guard.s'))
P.add_argument('--out',type=Path,required=True)
a=P.parse_args();base=a.hf3_rom.read_bytes()
assert hashlib.sha256(base).hexdigest()=='85a8be61fdac2feb777ed1726235b46b36f8950265a1788e7d7c9a0bc90f4b11'
with tempfile.TemporaryDirectory() as td:
 t=Path(td);obj=t/'guard.o';elf=t/'guard.elf';raw=t/'guard.bin'
 subprocess.run(['as','--32','-o',str(obj),str(a.assembly)],check=True)
 subprocess.run(['ld','-m','elf_i386','-Ttext','0','-e','normal_save','-o',str(elf),str(obj)],check=True)
 subprocess.run(['objcopy','-O','binary','-j','.text',str(elf),str(raw)],check=True)
 symbols={}
 for line in subprocess.check_output(['nm','-n',str(elf)],text=True).splitlines():
  v,ty,name=line.split();symbols[name]=int(v,16)
 blob=raw.read_bytes()[0xfa80:symbols['guard_end']]
assert symbols['normal_save']==0xfa80 and symbols['guard_end']<=0x10000
image=bytearray(base);edits=[]
def edit(addr,old,new,name):
 assert len(old)==len(new) and image[addr:addr+len(old)]==old
 edits.append({'id':name,'offset':f'0x{addr:06X}','before':old.hex(),'after':new.hex(),
               'reason':'HF4 protected SRAM format: invalidate both shared-payload markers, CRC16 plus commit, legacy load compatibility.'})
 image[addr:addr+len(old)]=new
for addr,label,size,name in [(0x190367,'normal_save',5,'SAVE_NORMAL_GUARD'),(0x19038c,'alternate_save',3,'SAVE_ALTERNATE_GUARD'),(0x1903b8,'validate_save',5,'SAVE_VALIDATOR_GUARD')]:
 new=b'\xe9'+struct.pack('<H',(symbols[label]-(addr&65535)-3)&65535)+b'\x90'*(size-3)
 edit(addr,base[addr:addr+size],new,name)
edit(0x1903fd,b'1',b'4','SAVE_ALTERNATE_PROTECTED_SIGNATURE')
edit(0x190401,b'1',b'4','SAVE_NORMAL_PROTECTED_SIGNATURE')
edit(0x19fa80,b'\xff'*len(blob),blob,'SAVE_GUARD_CODE')
image[-2:]=struct.pack('<H',sum(image[:-2])&65535)
a.out.mkdir(parents=True,exist_ok=True)
(a.out/'guard_edits.json').write_text(json.dumps({'base_sha256':hashlib.sha256(base).hexdigest(),'edits':edits},indent=2)+'\n')
(a.out/'guard_symbols.json').write_text(json.dumps(symbols,indent=2)+'\n')
(a.out/'guard.bin').write_bytes(blob)
(a.out/'Chocobo_EN_v1.1_HF4_TEST.ws').write_bytes(image)
print(json.dumps({'bytes':len(blob),'sha256':hashlib.sha256(image).hexdigest(),'symbols':symbols},indent=2))
