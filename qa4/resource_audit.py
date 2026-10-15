from pathlib import Path
import struct,json
r=Path('private_roms/JP.ws').read_bytes()
def dec(start):
 n=struct.unpack_from('<H',r,start)[0];p=start+2;b=bytearray()
 while len(b)<n:
  flags=r[p];p+=1
  for bit in range(8):
   if len(b)>=n:break
   if flags>>bit&1:b.append(r[p]);p+=1
   else:
    v=struct.unpack_from('<H',r,p)[0];p+=2;num=(v&15)+3;src=len(b)-(v>>4)
    for _ in range(num):
     b.append(b[src] if src>=0 else 0);src+=1
 return b,p
for off in (0x105b76,0x130c48):
 b,end=dec(off);Path(f'qa4/resource_{off:06X}.bin').write_bytes(b);print(hex(off),len(b),'end',hex(end),'next',r[end:end+24].hex())
b,_=dec(0x130c48)
for y in range(32):print(' '.join(f'{struct.unpack_from("<H",b,(y*32+x)*2)[0]:04X}' for x in range(32)))
