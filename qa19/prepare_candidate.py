from pathlib import Path
import json,sys,struct,hashlib
sys.path.insert(0,str(Path(__file__).parent));from text_codec import pages,line
sys.path.insert(0,'delivery/Chocobo_EN_v1.1_HF13_TEST_Fuentes_QA18_M4_20261014/qa15');from inventory_layout import story_inventory,words_until_end
old=Path('qa18/private/hf13_release/Chocobo_EN_v1.1_HF13_TEST.ws').read_bytes();jp=Path('qa14/private/Chocobo no Fushigi na Dungeon (J) [M].ws').read_bytes();r=bytearray(old);rows,_=story_inventory(old,'HF13');rows={x['id']:x for x in rows};strings=json.loads(Path('qa19/translations.json').read_text());edits=[];alloc=[];cursor=0x6e000;pool={}
assert old[0x6e000:0x6ff00]==jp[0x6e000:0x6ff00]==b'\xff'*0x1f00
for id,ps in strings.items():
 row=rows[id];g=row['group'];n=row['message'];bank=old[0x150ed3+g]&31;b=bank<<16;root=struct.unpack_from('<H',old,b+2)[0];table=b+struct.unpack_from('<H',old,b+root+2*g)[0];ptr=table+2*n;assert bank==6
 words=pages(ps)
 if id in ['G16:M000','G16:M003','G16:M051','G16:M061']:words=words[:-2]+[0xffff]
 # Retain existing highlighted Chapter 3 while fixing its meaning.
 if id=='G06:M099':
  words=pages(ps[:1])[:-1]+[0xfffd]+line('Item trading normally')+[0xfffe]+line('starts in ')+[0xfffa,6]+line('Chapter 3')+[0xfffa,0]+line('!')+[0xfff2,0xffff]
 raw=struct.pack('<'+'H'*len(words),*words)
 if raw in pool:newptr=pool[raw]
 else:
  newptr=cursor;pool[raw]=cursor;cursor+=len(raw);assert cursor<=0x6ff00
  edits.append(dict(id=id+'_payload',offset=hex(newptr),before=old[newptr:cursor].hex(),after=raw.hex(),reason='Validated same-bank FF pool; new editable English message.'));r[newptr:cursor]=raw
 before=old[ptr:ptr+2];after=struct.pack('<H',newptr&65535);assert struct.unpack('<H',before)[0]==int(row['pointer'],16)&65535
 edits.append(dict(id=id+'_pointer',offset=hex(ptr),before=before.hex(),after=after.hex(),reason='Preserve bank and message ID; redirect verified group table entry to the translated message.'));r[ptr:ptr+2]=after
 alloc.append(dict(id=id,table_entry=f'{ptr:06X}',original_pointer=row['pointer'],new_pointer=f'{newptr:06X}',bytes=len(raw),pages=ps,words=words))
r[-2:]=struct.pack('<H',sum(r[:-2])&65535);Path('qa19/private/candidate.ws').write_bytes(r);Path('qa19/edits.json').write_text(json.dumps(edits,indent=2)+'\n');Path('qa19/allocations.json').write_text(json.dumps(alloc,indent=2)+'\n');print('resources',len(strings),'pool',cursor-0x6e000,'hash',hashlib.sha256(r).hexdigest())
