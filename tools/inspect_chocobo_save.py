#!/usr/bin/env python3
"""Read-only inspection of the observed Rev 2 Chocobo WS save layout.
A marker match does not prove that all event data are coherent or recoverable.
"""
from pathlib import Path
import argparse,hashlib,json,struct
P=argparse.ArgumentParser(description=__doc__);P.add_argument('save',type=Path);P.add_argument('--compare',type=Path);a=P.parse_args()
b=a.save.read_bytes()
if len(b)!=32768:P.error('Expected a 32768-byte raw SRAM image; do not pass a savestate or ROM.')
markers={'normal':b[0x75b0:0x75b4]==b'n_c1','alternate':b[0x75ac:0x75b0]==b'A_C1'}
o={'file':a.save.name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'markers':markers,'any_known_marker':any(markers.values()),'normal_marker_hex':b[0x75b0:0x75b4].hex(),'alternate_marker_hex':b[0x75ac:0x75b0].hex(),'payload_range':'75B6..7F89 inclusive','payload_sha256':hashlib.sha256(b[0x75b6:0x7f8a]).hexdigest(),'saved_fields_observed':{'level':b[0x765b],'dungeon':b[0x7cdf],'floor_7303':struct.unpack_from('<H',b,0x7ce1)[0],'destination_7305':struct.unpack_from('<H',b,0x7ce3)[0]},'validation_scope':'Signature and byte comparison only; no global integrity or recovery guarantee','writes_to_input':False}
if a.compare:
 c=a.compare.read_bytes()
 if len(c)!=32768:P.error('Comparison must also be a 32768-byte SRAM image')
 o['comparison']={'sha256':hashlib.sha256(c).hexdigest(),'changed_bytes':sum(x!=y for x,y in zip(b,c)),'marker_offsets_changed':[f'{i:04X}'for i in range(0x75ac,0x75b4)if b[i]!=c[i]],'payload_changed_bytes':sum(x!=y for x,y in zip(b[0x75b6:0x7f8a],c[0x75b6:0x7f8a]))}
print(json.dumps(o,indent=2))
