"""Verify bounded HF20 changes, exact inheritance and native trace provenance."""
from pathlib import Path
import csv,hashlib,json,os,struct,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from build import build,PATCH_NAME
from qa26.rebuild_edits import baseline,repair
from qa15.inventory_layout import story_inventory,getter_inventory,window_inventory
from tools.reference_bps.bps import apply
sha=lambda b:hashlib.sha256(b).hexdigest()
def main():
    checks=0
    def ck(v,label):
        nonlocal checks
        assert v,label;checks+=1
    jp=Path(os.environ['CONTINUITY_INPUT_JP']).read_bytes();old=baseline(jp);rom,bps,result=build(jp)
    regenerated,edits,review=repair(old)
    ck(regenerated==rom,'semantic regeneration')
    ck(edits==json.loads((ROOT/'qa26/edits.json').read_text()),'editable edits')
    ids={r['id'] for r in review};allowed={len(rom)-2,len(rom)-1}
    for e in edits:
        off=int(e['offset'],16);before=bytes.fromhex(e['before']);after=bytes.fromhex(e['after'])
        ck(old[off:off+len(before)]==before and rom[off:off+len(after)]==after,e['id'])
        allowed.update(range(off,off+len(after)))
    diff={i for i,(a,b) in enumerate(zip(old,rom)) if a!=b}
    ck(diff<=allowed and len(diff)==352,'352 bounded changed bytes')
    ck(apply(jp,bps)==rom,'independent BPS application')
    ck(bps==(ROOT/'patches'/PATCH_NAME).read_bytes(),'delivered BPS')
    ck(struct.unpack_from('<H',rom,len(rom)-2)[0]==sum(rom[:-2])&65535,'checksum')
    ck(old[0x140000:0x190000]==rom[0x140000:0x190000],'code and font banks unchanged')
    a={x['id']:x for x in story_inventory(old,'HF19')[0]};b={x['id']:x for x in story_inventory(rom,'HF20')[0]}
    ck(len(a)==len(b)==3488,'story count')
    ck({i for i in a if a[i]['stream_sha256']!=b[i]['stream_sha256']}==ids,'exactly fourteen story streams changed')
    ck(all(a[i]['pointer']==b[i]['pointer'] for i in a),'all story pointers unchanged')
    a={x['id']:x for x in getter_inventory(old,'HF19')[0]};b={x['id']:x for x in getter_inventory(rom,'HF20')[0]}
    ck(len(a)==len(b)==2333,'getter count')
    ck(all(a[i]['stream_sha256']==b[i]['stream_sha256'] and a[i]['pointer']==b[i]['pointer'] for i in a),'all getter streams and pointers unchanged')
    ck(window_inventory(old)==window_inventory(rom),'all window presets unchanged')
    m=json.loads((ROOT/'manifest.json').read_text());frames=0;sessions=0;blank=0
    for ident in sorted(ids):
        for prefix,expected in [('baseline',sha(old)),('candidate',sha(rom))]:
            r=ROOT/'evidence/qa26_runs'/(prefix+'_'+ident.replace(':','_'));meta=json.loads((r/'run.json').read_text())
            ck(meta['completed']and meta['exit']==0,r.name+' completion')
            ck(meta['rom_sha256']==expected and meta['mesen_sha256']==m['mesen_sha256'],r.name+' provenance')
            ck(meta['plan_sha256']==sha((r/'plan.lua').read_bytes()),r.name+' plan')
            ck((r/'target_completed.txt').read_text().strip()=='true',r.name+' completed text')
            with (r/'story.csv').open() as f:trace=list(csv.DictReader(f))
            ck(not any(x['event']=='auto_line'and x['value']!='0000'for x in trace),r.name+' no lost characters')
            ck(any(x['event']=='read'and x['value']=='FFFF'for x in trace),r.name+' terminator')
            blank+=sum(x['event']=='auto_line'and x['value']=='0000'for x in trace)
            frames+=int((r/'completed.txt').read_text().split('=')[1]);sessions+=1
    pairs=json.loads((ROOT/'qa26/native_pairs.json').read_text())
    for p in pairs:
        for k in ['before','after']:ck(sha((ROOT/p[k]).read_bytes())==p[k+'_sha256'],p['id']+' image '+k)
    result.update(status='PASS_SCOPED_QA26_BINARY_AND_NATIVE',checks=checks,changed_resources=len(ids),changed_bytes_vs_hf19=len(diff),native_sessions=sessions,native_frames=frames,paired_pages=len(pairs),nonblank_dropped=0,blank_padding_drops=blank,independent_bps='PASS_EXACT_BYTES',global_visual_approved=False,natural_reachability='NOT_VALIDATED')
    (ROOT/'qa26/verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
