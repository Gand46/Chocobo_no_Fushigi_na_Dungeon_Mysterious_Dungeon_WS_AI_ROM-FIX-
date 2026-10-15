#!/usr/bin/env python3
"""QA15/M1. Structural inventory; never equates a record with visual approval.

Usage: python3 inventory_layout.py --rom HF10.ws --jp original.ws --out census
No ROM or glyph bitmap is exported. Raw words are represented by counts/hashes.
"""
import argparse, collections, csv, hashlib, json, struct
from pathlib import Path

def u16(r, p): return struct.unpack_from('<H', r, p)[0]
def sha(b): return hashlib.sha256(b).hexdigest()
def csvout(path, rows):
    with path.open('w', newline='') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def words_until_end(r, start, cap=512):
    values=[]; p=start; end=min((start|0xffff)+1,len(r),start+cap*2)
    while p+1<end:
        v=u16(r,p);p+=2
        if v==0xffff:return values,p,True
        values.append(v)
    return values,p,False
def story_shape(words):
    # Controls with inline argument: numeric substitutions, palette and sound.
    # FFF2 pauses but does not itself reset column; FFFD clears the box.
    lines=[]; n=0; ctr=collections.Counter();args=[];dynamic=False;i=0
    while i<len(words):
        v=words[i];i+=1
        if v>=0xfff0:
            ctr[f'{v:04X}']+=1
            if v in (0xfffe,0xfffd):lines.append(n);n=0
            if v in (0xfff4,0xfff8,0xfffa,0xfffb):
                if i<len(words):args.append(f'{v:04X}:{words[i]:04X}');i+=1
                if v in (0xfff4,0xfff8):dynamic=True
        else:n+=1
    lines.append(n)
    return lines,ctr,args,dynamic

def getter_inventory(r, label):
    rows=[];families=[]
    for family in range(19):
        desc=0x18d930+family*4;off,seg=struct.unpack_from('<HH',r,desc)
        # Native segmented pointers map into a 2 MiB ROM via the high bank window.
        bank=(seg//0x1000+0x10)&0x1f;table=(bank<<16)+off
        first=u16(r,table);count=(first-off)//2
        if not (0<count<=512 and (first-off)%2==0):raise ValueError((family,off,first,count))
        ptrs=[(bank<<16)+u16(r,table+2*i) for i in range(count)]
        starts=set(ptrs);frows=[]
        for index,start in enumerate(ptrs):
            words,end,terminated=words_until_end(r,start)
            nextptr=min((x for x in starts if x>start),default=None)
            overlap=nextptr is not None and end>nextptr
            plain=[w for w in words if w<0xfff0 and not w&0x2000]
            nominal=sum(8 if w&0x8000 else 16 for w in plain)
            kind='icon' if family in (4,16) else ('numeric' if family in (9,18) else 'text_or_mixed')
            row=dict(rom=label,id=f'F{family:02d}:I{index:03d}',family=family,index=index,
                table=f'{table:06X}',pointer=f'{start:06X}',end=f'{end:06X}',
                words=len(words),terminated=terminated,nonempty=bool(words),
                shared_tail=overlap,kind=kind,common_copy_nominal_px=nominal,
                controls=' '.join(sorted({f'{w:04X}' for w in words if w>=0xfff0})),
                stream_sha256=sha(r[start:end]),status='STATIC_ONLY_NOT_VISUAL_PASS')
            rows.append(row);frows.append(row)
        families.append(dict(rom=label,family=family,table=f'{table:06X}',entries=count,
            nonempty=sum(x['nonempty'] for x in frows),terminated=sum(x['terminated'] for x in frows),
            shared_tail_entries=sum(x['shared_tail'] for x in frows),kind=frows[0]['kind']))
    return rows,families

def story_inventory(r,label):
    rows=[];groups=[]
    # 0..16 form the verified pointer-table domain. Beyond that, the root data
    # contain animation/resource tables; 32 bank bytes do NOT mean 32 text groups.
    for group in range(17):
        bank=r[0x150ed3+group]&0x1f;b=bank<<16;root=u16(r,b+2);off=u16(r,b+root+2*group)
        if off==0xffff:
            groups.append(dict(rom=label,group=group,bank=bank,table='',entries=0,status='UNASSIGNED_FFFF'));continue
        first=u16(r,b+off);count=(first-off)//2
        # The first resource has moved in G16 (QA19), G07 (QA21), and G09
        # (QA22). Their JP/HF16 tables are fixed 256-entry domains, so the
        # first pointer can no longer be used to infer table length.
        if bank==6 and ((group==16 and off==0xcb86) or (group==7 and off==0x6f40) or (group==9 and off==0x8a82)):
            count=256;first=off+2*count
        if not (0<count<=256 and (first-off)%2==0):raise ValueError((label,group,off,first,count))
        groups.append(dict(rom=label,group=group,bank=bank,table=f'{b+off:06X}',entries=count,status='POINTER_DOMAIN_STATIC'))
        starts=[b+u16(r,b+off+2*i) for i in range(count)]
        for index,start in enumerate(starts):
            words,end,term=words_until_end(r,start)
            lines,controls,args,dynamic=story_shape(words)
            rows.append(dict(rom=label,id=f'G{group:02d}:M{index:03d}',group=group,message=index,
                bank=bank,pointer=f'{start:06X}',end=f'{end:06X}',words=len(words),terminated=term,
                nonempty=bool(words),unique_pointer=starts.count(start)==1,
                stored_lines='|'.join(map(str,lines)),max_literal_cells=max(lines),
                exceeds_13_literal_cells=max(lines)>13,dynamic=dynamic,
                controls=' '.join(f'{k}x{v}' for k,v in sorted(controls.items())),
                arguments=' '.join(args),stream_sha256=sha(r[start:end]),
                status='STATIC_ONLY_RUNTIME_CONTEXT_PENDING'))
    return rows,groups

def window_inventory(r):
    rows=[]
    for wid in range(141):
        x,y,w,unknown,mode,h=r[0x183f70+6*wid:0x183f76+6*wid]
        init=u16(r,0x1842d0+wid*2);consumer=u16(r,0x186d46+wid*2)
        rows.append(dict(id=wid,id_hex=f'{wid:02X}',x_tiles=x,y_parameter=y,width_tiles=w,
            byte3_unknown=unknown,mode=mode,height_tiles=h,inner_width_px=max(0,w-2)*8,
            nominal_lines=(6 if wid==13 else 8 if wid in (25,27) else max(0,h-2)//2),
            initializer=f'18{init:04X}',row_consumer=f'18{consumer:04X}',
            anchor='MODE4_COORDINATES' if mode==4 else 'SPECIAL_ANCHOR_REQUIRES_TRACE',
            status='PRESET_NOT_VISUAL_APPROVAL'))
    return rows

def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--jp',required=True);p.add_argument('--out',required=True);p.add_argument('--label',default='HF10');a=p.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True);report={}
    for label,path in [(a.label,a.rom),('JP',a.jp)]:
        r=Path(path).read_bytes();gr,fa=getter_inventory(r,label);st,sg=story_inventory(r,label)
        csvout(out/f'{label}_getter.csv',gr);csvout(out/f'{label}_getter_families.csv',fa)
        csvout(out/f'{label}_dialogue.csv',st);csvout(out/f'{label}_dialogue_groups.csv',sg)
        report[label]={'sha256':sha(r),'getter_entries':len(gr),'getter_nonempty':sum(x['nonempty'] for x in gr),
            'getter_unterminated':sum(not x['terminated'] for x in gr),'getter_shared_tails':[x['id'] for x in gr if x['shared_tail']],
            'getter_words':sum(x['words'] for x in gr),'getter_words_with_terminators':sum(x['words']+int(x['terminated']) for x in gr),'story_groups':sum(x['entries']>0 for x in sg),
            'story_entries':len(st),'story_unique_pointers':len({x['pointer'] for x in st}),
            'story_nonempty':sum(x['nonempty'] for x in st),'story_unterminated':sum(not x['terminated'] for x in st),
            'story_entries_with_literal_cells':sum(x['max_literal_cells']>0 for x in st),
            'story_control_only_nonempty':sum(x['nonempty'] and x['max_literal_cells']==0 for x in st),
            'story_dynamic_entries':sum(x['dynamic'] for x in st),'story_literal_over_13':[x['id'] for x in st if x['exceeds_13_literal_cells']]}
        if label==a.label:csvout(out/'window_presets.csv',window_inventory(r))
    (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
