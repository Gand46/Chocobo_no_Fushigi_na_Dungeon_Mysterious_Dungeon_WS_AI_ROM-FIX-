#!/usr/bin/env python3
"""Produce HF18-relative getter edits; never mutates canonical sources or input ROM.
F17:I007 already encodes Wither Hit exactly and is intentionally retained.
"""
from pathlib import Path
import argparse, hashlib, json, struct, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from qa15.inventory_layout import getter_inventory, words_until_end
from qa20.text_codec import encode
BASE_SHA='6b7b0d79c4d60e6a6bbb5ae062b4255e75eda716f83bfbbd972cad65f3e05c24'
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--base-rom',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    base=args.base_rom.read_bytes()
    assert hashlib.sha256(base).hexdigest()==BASE_SHA, 'Requires verified HF18 base'
    rows={x['id']:x for x in getter_inventory(base,'HF18')[0]}
    retained=rows['F17:I007']
    words,_,_=words_until_end(base,int(retained['pointer'],16))
    assert words==list(encode('Wither Hit'))
    cursor=0x19ff00; limit=0x19ff20
    assert base[cursor:limit]==b'\xff'*(limit-cursor)
    edits=[]; allocations=[]; rom=bytearray(base)
    for ident,data in json.loads((ROOT/'qa24/getter_translations.json').read_text()).items():
        row=rows[ident]; table=int(row['table'],16); old=int(row['pointer'],16)
        assert table==0x19bfc4 and old>>16==cursor>>16==0x19
        words=list(encode(data['text']))
        assert len(words)<=8, 'Native preset 81 interior is 128px / eight 16px cells'
        payload=struct.pack('<'+'H'*(len(words)+1),*words,0xffff)
        start=cursor; cursor+=len(payload); assert cursor<=limit
        ptr=table+2*row['index']
        assert struct.unpack_from('<H',base,ptr)[0]==old&0xffff
        for suffix,off,raw in [('payload',start,payload),('pointer',ptr,struct.pack('<H',start&0xffff))]:
            edits.append({'id':ident+'_getter_'+suffix,'offset':hex(off),'before':base[off:off+len(raw)].hex(),'after':raw.hex(),'reason':data['reason']})
            rom[off:off+len(raw)]=raw
        allocations.append({'id':ident,'text':data['text'],'old_pointer':hex(old),'pointer_entry':hex(ptr),'pointer':hex(start),'bytes':len(payload),'words':words,'native_window':'81','interior_px':128,'nominal_width_px':16*len(words),'reason':data['reason']})
    assert cursor==limit
    rom[-2:]=struct.pack('<H',sum(rom[:-2])&65535)
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'getter_edits.json').write_text(json.dumps(edits,indent=2)+'\n')
    (args.out/'getter_allocations.json').write_text(json.dumps(allocations,indent=2)+'\n')
    (args.out/'getter_candidate.ws').write_bytes(rom)
    print(json.dumps({'base_sha256':BASE_SHA,'candidate_sha256':hashlib.sha256(rom).hexdigest(),'changed_references':len(allocations),'retained_exact':'F17:I007 / Wither Hit','reserved_range':'19FF00..19FF20','status':'BUILT_STATIC_ONLY_RUNTIME_PENDING'}))
if __name__=='__main__':main()
