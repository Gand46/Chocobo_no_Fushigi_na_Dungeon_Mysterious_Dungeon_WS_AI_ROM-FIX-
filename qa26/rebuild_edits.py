"""HF19 -> HF20: bounded aesthetic spacing and six source-equivalent reflows."""
from pathlib import Path
import argparse, hashlib, json, struct, sys
from functools import lru_cache
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from build import replace_checked
from qa15.inventory_layout import story_inventory,words_until_end,story_shape
from qa21.text_codec import encode
BASE_SHA='f27e69f65e134b161c1f3ce263c3ed78a8ae247997c95d7383c43c4a78c8962f'

def baseline(jp):
    m=json.loads((ROOT/'docs/history/qa25/manifest_hf19.json').read_text())
    assert hashlib.sha256(jp).hexdigest()==m['original']['sha256']
    r=bytearray(jp)
    replace_checked(r,json.loads((ROOT/'src/legacy_translation_ranges.json').read_text())['edits'])
    replace_checked(r,json.loads((ROOT/'docs/history/qa25/corrections_hf19.json').read_text())['edits'])
    r[-2:]=struct.pack('<H',sum(r[:-2])&65535)
    assert hashlib.sha256(r).hexdigest()==BASE_SHA
    return bytes(r)

def make_bounds(rom):
    @lru_cache(None)
    def bounds(v):
        if not 0<v<0x1000:return None
        a=0x160760+(v-1)*64;xs=[]
        for x in range(16):
            for y in range(16):
                p=a+((x//8)*2+y//8)*16+(y%8)*2
                lo,hi=rom[p:p+2]
                if ((lo>>(7-x%8))&1)+2*((hi>>(7-x%8))&1)!=3:
                    xs.append(x);break
        return (min(xs),max(xs)) if xs else None
    return bounds

def compact(words,bounds):
    out=[];events=[]
    for i,v in enumerate(words):
        if v==0 and 0<i<len(words)-1:
            left,right=bounds(words[i-1]),bounds(words[i+1])
            if left and right:
                gap=15-left[1]+right[0]
                if 8<=gap<=16:
                    events.append(dict(word_index=i,left_glyph=words[i-1],right_glyph=words[i+1],before_gap_px=gap+16,after_gap_px=gap));continue
        out.append(v)
    assert [x for x in out if x]!=[ ]
    assert [x for x in out if x]==[x for x in words if x]
    return out,events

def repair(base):
    assert hashlib.sha256(base).hexdigest()==BASE_SHA
    config=json.loads((ROOT/'qa26/adjustments.json').read_text())
    rows=story_inventory(base,'HF19')[0];by={x['id']:x for x in rows}
    ids=sorted(set(config['spacing_ids'])|set(config['reflows']))
    bounds=make_bounds(base);out=bytearray(base);edits=[];review=[]
    for ident in ids:
        row=by[ident];start=int(row['pointer'],16);end=int(row['end'],16)
        assert [x['id']for x in rows if x['pointer']==row['pointer']]==[ident]
        words,_,term=words_until_end(base,start);assert term and not row['dynamic']
        working=list(words)
        if ident in config['reflows']:
            source=json.loads((ROOT/('qa20'if ident.startswith('G00:')else'qa22'if ident.startswith('G09:')else'qa21')/'translations.json').read_text())[ident]['text']
            lines=config['reflows'][ident];assert ' '.join(lines)==source
            assert [x for x in words if x>=0xfff0]==[0xfffe,0xfff2]
            encoded=[encode(line)for line in lines];assert all(x and len(x)<=13 for x in encoded)
            working=list(encoded[0])+[0xfffe]+list(encoded[1])+[0xfff2]
        compacted,events=compact(working,bounds)
        assert [x for x in compacted if x>=0xfff0]==[x for x in words if x>=0xfff0]
        assert max(story_shape(compacted)[0])<=13
        raw=struct.pack('<'+'H'*(len(compacted)+1),*compacted,0xffff)
        assert len(raw)<=end-start,(ident,len(raw),end-start)
        replacement=raw+bytes(end-start-len(raw))
        if replacement==base[start:end]:continue
        edit=dict(id=ident+'_aesthetic',offset=hex(start),before=base[start:end].hex(),after=replacement.hex(),reason='QA26: native-font spacing and balanced line distribution; wording and controls preserved')
        edits.append(edit);out[start:end]=replacement
        review.append(dict(id=ident,original_lines=story_shape(words)[0],new_lines=story_shape(compacted)[0],reflow=ident in config['reflows'],proposed_lines=config['reflows'].get(ident),spacing_events=events,bytes_before=end-start,bytes_used=len(raw),pointer=start))
    out[-2:]=struct.pack('<H',sum(out[:-2])&65535)
    return bytes(out),edits,review

def main():
    p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    base=baseline(a.jp.read_bytes());candidate,edits,review=repair(base);a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'candidate.ws').write_bytes(candidate)
    (a.out/'edits.json').write_text(json.dumps(edits,indent=2)+'\n')
    (a.out/'layout_review.json').write_text(json.dumps(review,indent=2)+'\n')
    print(json.dumps({'resources':len(edits),'reflows':sum(x['reflow']for x in review),'gaps_removed':sum(len(x['spacing_events'])for x in review),'rom_sha256':hashlib.sha256(candidate).hexdigest(),'changed_bytes':sum(a!=b for a,b in zip(base,candidate))}))
if __name__=='__main__':main()
