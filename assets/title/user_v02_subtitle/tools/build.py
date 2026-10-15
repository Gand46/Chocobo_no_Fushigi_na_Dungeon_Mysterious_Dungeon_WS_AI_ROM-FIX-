"""Rebuild 91 native frames, animation, 2bpp resources and review evidence.

No ROM is read or modified. Tile maps are neutral export maps, not game offsets.
"""
from pathlib import Path
import base64, csv, hashlib, io, json, struct
import numpy as np
from PIL import Image, ImageDraw, GifImagePlugin
from prepare_assets import ROOT, indices, indexed, PAL
from subtitle_native import render_subtitle

def digest(data): return hashlib.sha256(data).hexdigest()

def tile_bytes(tile):
    out=bytearray()
    for row in tile:
        for bit in range(2):
            out.append(sum(((int(v)>>bit)&1)<<(7-x) for x,v in enumerate(row)))
    return bytes(out)

def decode_tile(raw):
    return np.array([[(raw[y*2]>>(7-x)&1)|((raw[y*2+1]>>(7-x)&1)<<1)
                     for x in range(8)] for y in range(8)], dtype='uint8')

def write_gif(path, frames, durations, scale=1):
    # Write each source frame explicitly, including held frames; do not merge.
    ims=[indexed(a) for a in frames]
    if scale!=1: ims=[im.resize((224*scale,144*scale),Image.Resampling.NEAREST) for im in ims]
    with path.open('wb') as f:
        header,_=GifImagePlugin.getheader(ims[0],info={'loop':0})
        for b in header: f.write(b)
        for im,ms in zip(ims,durations):
            for b in GifImagePlugin.getdata(im,duration=ms,disposal=1): f.write(b)
        f.write(b';')

def main():
    out=ROOT/'build';out.mkdir(exist_ok=True)
    for s in ['frames','unique','tiles']: (out/s).mkdir(exist_ok=True)
    cfg=json.loads((ROOT/'assets/layout.json').read_text())
    src=Image.open(ROOT/'references/title_original.gif')
    original=[];durations=[]
    for i in range(src.n_frames):
        src.seek(i);original.append(indices(src));durations.append(src.info['duration'])
    original=np.stack(original)
    moving=np.any(original!=original[0],axis=0); moving[121:]=False
    Image.fromarray((moving*255).astype('uint8')).save(out/'original_motion_mask.png')
    background=np.array(Image.open(ROOT/'assets/backplate_native.png'))
    logo=np.array(Image.open(ROOT/'assets/wordmark_indices.png'))
    alpha=np.array(Image.open(ROOT/'assets/wordmark_mask.png'))>127
    subtitle,subtitle_layout=render_subtitle(ROOT/'assets/subtitle_font_v02.json')
    indexed(subtitle).save(out/'subtitle_native_v02.png',bits=2)
    (out/'subtitle_layout_v02.json').write_text(json.dumps(subtitle_layout,indent=2)+'\n')
    static=original[0].copy()
    ya,yb=cfg['backplate_rows'];static[ya:yb]=background[ya:yb]
    ya,yb=cfg['clear_rows'];static[ya:yb]=3
    # Clear generated portrait remnants from the native animation corridor.
    # Restore unchanged exposed parts from the original under the moving stencil.
    static[56:64,86:142]=0
    static[56:61,87:114]=original[0,56:61,87:114]
    x,y=cfg['wordmark_xy'];h,w=logo.shape
    assert x>=0 and x+w<=224 and y+h<=121
    static[y:y+h,x:x+w][alpha]=logo[alpha]
    x,y=cfg['subtitle_xy'];h,w=subtitle.shape
    static[y:y+h,x:x+w]=subtitle
    # Preserve the original trademark as pixels; move alongside the wider logo.
    static[100:106,193:202]=original[0,92:98,174:183]
    frames=[];unique=[];unique_lookup={};pose_lookup={};records=[];t=0
    for i,(srcframe,ms) in enumerate(zip(original,durations)):
        f=static.copy();f[:56]=srcframe[:56];f[moving]=srcframe[moving];f[121:]=srcframe[121:]
        frames.append(f)
        k=f.tobytes()
        if k not in unique_lookup: unique_lookup[k]=len(unique);unique.append(f)
        uk=unique_lookup[k]
        pk=srcframe[:121].tobytes()
        if pk not in pose_lookup:pose_lookup[pk]=len(pose_lookup)
        records.append({'frame':i,'start_ms':t,'duration_ms':ms,'pose':pose_lookup[pk],
                        'prompt_on':int(np.any(srcframe[121:]!=3)), 'unique':uk,'sha256_indices':digest(k)})
        indexed(f).save(out/'frames'/f'frame_{i:03}.png',bits=2)
        t+=ms
    for n,f in enumerate(unique):indexed(f).save(out/'unique'/f'state_{n:02}.png',bits=2)
    with (out/'timeline.csv').open('w',newline='') as fp:
        w=csv.DictWriter(fp,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    write_gif(out/'Chocobo_WS_Logo_EN_224x144.gif',frames,durations)
    write_gif(out/'Chocobo_WS_Logo_EN_4x.gif',frames,durations,4)
    indexed(frames[0]).save(out/'Chocobo_WS_Logo_EN_224x144.png',bits=2)
    indexed(frames[0]).resize((896,576),Image.Resampling.NEAREST).save(out/'Chocobo_WS_Logo_EN_4x.png')
    # Pool all states with a single pattern dictionary, no flip deduplication.
    pool=[];lookup={};maps=[]
    for f in unique:
        tilemap=[]
        for ty in range(18):
            for tx in range(28):
                raw=tile_bytes(f[ty*8:ty*8+8,tx*8:tx*8+8])
                if raw not in lookup:lookup[raw]=len(pool);pool.append(raw)
                tilemap.append(lookup[raw])
        maps.append(tilemap)
    assert len(pool)<=512,'Generic tile bank capacity exceeded'
    (out/'tiles/title_patterns.2bpp').write_bytes(b''.join(pool))
    for n,tm in enumerate(maps):
        (out/'tiles'/f'state_{n:02}.map16le').write_bytes(struct.pack('<504H',*tm))
        rebuilt=np.zeros((144,224),dtype='uint8')
        for cell,idx in enumerate(tm):
            ty,tx=divmod(cell,28);rebuilt[ty*8:ty*8+8,tx*8:tx*8+8]=decode_tile(pool[idx])
        assert np.array_equal(rebuilt,unique[n]),'2bpp roundtrip mismatch'
    atlas=np.full((((len(pool)+15)//16)*8,128),3,dtype='uint8')
    for n,tile in enumerate(pool):
        ty,tx=divmod(n,16);atlas[ty*8:ty*8+8,tx*8:tx*8+8]=decode_tile(tile)
    indexed(atlas).save(out/'tiles/pattern_atlas.png',bits=2)
    # Per-state tilemap deltas; VRAM allocation/timing in the game is not claimed.
    deltas={}
    for prev,nxt in zip(records,records[1:]):
        a,b=prev['unique'],nxt['unique']
        if a!=b:deltas[f'{a}->{b}']=[[i,v] for i,v in enumerate(maps[b]) if v!=maps[a][i]]
    (out/'tiles/map_deltas.json').write_text(json.dumps(deltas,indent=2)+'\n')
    # Review all distinct states at native size plus exact 3x enlargement.
    sheet=Image.new('RGB',(3*704,2*612),(245,245,239));d=ImageDraw.Draw(sheet)
    for n,f in enumerate(unique):
        x=(n%3)*704;y=(n//3)*612
        d.text((x+16,y+12),f'State {n:02} / native 224 x 144',fill=(25,25,25))
        sheet.paste(indexed(f).convert('RGB'),(x+16,y+34))
        sheet.paste(indexed(f).resize((672,432),Image.Resampling.NEAREST).convert('RGB'),(x+16,y+180))
    sheet.save(out/'Chocobo_WS_Logo_EN_All_States.png')
    # Compare original + localized within the exact same source timeline.
    small=Image.new('RGB',(952,678),(245,245,239));d=ImageDraw.Draw(small)
    d.text((20,12),'ORIGINAL / 2x',fill=(25,25,25));d.text((488,12),'LOCALIZED ART / 2x',fill=(25,25,25))
    for row,i in enumerate([0,36]):
        for col,a in enumerate([original[i],frames[i]]):small.paste(indexed(a).resize((448,288),Image.Resampling.NEAREST).convert('RGB'),(20+468*col,42+314*row))
    small.save(out/'Chocobo_WS_Logo_EN_Comparison.png')
    rendered=Image.open(out/'Chocobo_WS_Logo_EN_224x144.gif')
    assert rendered.n_frames==len(frames)
    for i in range(rendered.n_frames):
        rendered.seek(i)
        assert rendered.info['duration']==durations[i]
        assert np.array_equal(indices(rendered),frames[i])
    current=np.stack(frames)
    assert np.array_equal(current[:,:56],original[:,:56])
    assert np.array_equal(current[:,moving],original[:,moving])
    assert np.array_equal(current[:,121:],original[:,121:])
    assert np.array_equal(np.any(current!=current[0],axis=0),np.any(original!=original[0],axis=0))
    edited=np.any(current[0]!=original[0],axis=0)
    Image.fromarray((edited*255).astype('uint8')).save(out/'edit_mask.png')
    report={'version':cfg['version'],'method':'OFFLINE_ASSET_COMPOSITION','rom_modified':False,
      'original_gif_sha256':digest((ROOT/'references/title_original.gif').read_bytes()),
      'native_size':[224,144],'frames':len(frames),'unique_states':len(unique),'poses':len(pose_lookup),
      'duration_ms':sum(durations),'colors':PAL.tolist(),'unique_tiles':len(pool),'pattern_bytes':len(pool)*16,
      'tilemap_bytes_per_state':1008,'tile_count_limit_check':'PASS - standalone 512-pattern pool only',
      'same_timeline':'PASS','gif_roundtrip':'PASS','2bpp_roundtrip':'PASS',
      'original_upper_56_rows':'PASS - pixel identical', 'original_motion_pixels':'PASS - all frames pixel identical',
      'original_prompt_and_footer':'PASS - rows 121..143 pixel identical',
      'temporal_change_mask':'PASS - identical to input GIF','added_motion':'none',
      'lower_arch':'reconstructed from generated backplate, not recovered original hidden pixels',
      'integrated':'NOT_VALIDATED','runtime_confirmed':'NOT_VALIDATED','visual_approved_in_game':'NOT_VALIDATED',
      'functional_approved':'NOT_VALIDATED','final_approved':False,
      'frame_scope':'91 frames of supplied 6070ms GIF only; not all ROM title/boot/copyright states'}
    (out/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    # A self-contained inspection file; original and localised frames share one clock.
    def data(im):
        b=io.BytesIO();im.save(b,format='PNG');return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
    js={'en':[data(indexed(f)) for f in unique], 'jp':[data(indexed(original[next(i for i,r in enumerate(records) if r['unique']==n)])) for n in range(len(unique))], 'timeline':records}
    template=(ROOT/'tools/review_template.html').read_text()
    (out/'Chocobo_WS_Logo_EN_Frame_Viewer.html').write_text(template.replace('__DATA__',json.dumps(js)))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
