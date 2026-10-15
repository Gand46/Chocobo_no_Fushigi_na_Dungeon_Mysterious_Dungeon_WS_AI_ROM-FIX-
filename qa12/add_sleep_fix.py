from pathlib import Path
import json,struct
root=Path('delivery/Chocobo_EN_v1.1_HF9_TEST_Fuentes_QA12_20261014')
b=Path('private_roms/EN.ws').read_bytes();a=0x16ea1c
c=json.loads((root/'src/corrections.json').read_text());c['edits']=[e for e in c['edits'] if e['id']!='ITEM_SLEEP_CARD_NAME']
new=struct.pack('<8H',0xd1,0x19c,0x91,0xc1,0x13,0x61,0xffff,0xffff)
c['edits'].append({'id':'ITEM_SLEEP_CARD_NAME','offset':f'0x{a:06X}','before':b[a:a+16].hex(),'after':new.hex(),'reason':'Remove the stray el glyph between Sleep and Card. Reuse the existing native Sleep glyph sequence; preserve the original 16-byte slot and all pointers.'})
(root/'src/corrections.json').write_text(json.dumps(c,indent=2)+'\n')
p=root/'build.py';p.write_text(p.read_text().replace('three fused equipment text repairs','three fused equipment text repairs + Sleep Card name'))
