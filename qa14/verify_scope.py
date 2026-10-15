"""Recheck QA14's bounded native title evidence; optionally compare actual ROMs."""
from pathlib import Path
import argparse, hashlib, json, sys
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sha = lambda data: hashlib.sha256(data).hexdigest()


def verify(japanese_rom=None):
    manifest = json.loads((ROOT / 'docs/history/qa14/manifest.json').read_text())
    target = manifest['target']['sha256']
    runs = ROOT / 'evidence/qa14_runs'
    old = ROOT / 'evidence/qa11_runs/q11_animation'
    asset = ROOT / 'assets/title/user_v02_subtitle'
    for name in ['title_portable', 'title_menu']:
        meta = json.loads((runs / name / 'run.json').read_text())
        assert meta['completed'] and meta['exit'] == 0
        assert meta['rom_sha256'] == target and meta['state_sha256'] is None
        assert meta['mesen_sha256'] == manifest['mesen_sha256']
        assert sha((runs / name / 'plan.lua').read_bytes()) == meta['plan_sha256']
        assert sha((ROOT / 'qa11/driver.lua').read_bytes()) == meta['script_sha256']
    palette = np.array([[43,43,38],[152,149,139],[171,167,156],[224,219,205]], dtype=np.uint8)
    source = np.array(Image.open(asset / 'build/frames/frame_000.png'))
    expected = palette[source]
    mask = np.ones((144,224), dtype=bool)
    mask[109:121,65:159] = False
    frames = sorted((runs / 'title_portable').glob('anim*.png'))
    assert len(frames) == 1001
    for path in frames:
        actual = np.array(Image.open(path).convert('RGB'))[:144]
        baseline = np.array(Image.open(old / path.name).convert('RGB'))[:144]
        assert np.array_equal(actual[mask], baseline[mask]), path.name
        assert np.array_equal(actual[109:121,65:159], expected[109:121,65:159]), path.name
    for relative in ['authoring/wordmark_master.png', 'assets/wordmark_native.png',
                     'assets/wordmark_indices.png', 'assets/wordmark_mask.png']:
        assert (asset / relative).read_bytes() == (ROOT / 'assets/title/user_v01' / relative).read_bytes()
    readings = json.loads((ROOT / 'qa14/hf10_visible_transcription.json').read_text())['literal_readings']
    geometry = json.loads((ROOT / 'qa14/hf10_subtitle_geometry.json').read_text())
    cfg = json.loads((asset / 'assets/subtitle_font_v02.json').read_text())
    assert len(geometry) == 13
    for entry in geometry:
        assert readings[entry['id']] == cfg['text'][entry['source_position']]
    main = json.loads((ROOT / 'qa14/glyph_review.json').read_text())
    main_records=[entry for entry in main['records'] if entry['band']<2]
    assert len(main_records)==23 and all(entry['status']=='PASS' for entry in main_records)
    # This verifies the record, not human legibility; observations are preserved.
    image = Image.open(runs / 'title_portable/anim01000.png').convert('RGB')
    layout = json.loads((asset / 'build/subtitle_layout_v02.json').read_text())['glyphs']
    repeated = {}
    for char in ['o', 'r', 'n']:
        crops=[]
        for entry in layout:
            if entry['character'] == char:
                a,b,c,d=entry['ink_box']
                crops.append(image.crop((65+a-1,109+b-1,65+c+1,109+d+1)).tobytes())
        assert len(crops)==2 and crops[0]==crops[1]
        repeated[char]='TWO_INSTANCES_PIXEL_IDENTICAL'
    result = {'status':'PASS_BOUNDED_TITLE_EVIDENCE','target_sha256':target,
              'runtime_frames':len(frames),'pixels_outside_subtitle':'IDENTICAL_TO_QA11',
              'subtitle_source_pixels':'EXACT_NATIVE_RUNTIME','user_main_art':'UNCHANGED',
              'subtitle_glyph_readings':'13_OF_13_CONTEXT_MASKED','repeated_glyphs':repeated,
              'second_independent_reviewer':False,'global_layout':'NOT_APPROVED',
              'global_linguistic':'NOT_APPROVED','binary_comparison':'NOT_RUN_WITHOUT_JP_ARGUMENT'}
    if japanese_rom:
        sys.path.insert(0,str(ROOT))
        from tools.bps_codec import apply
        from build import build
        source_rom=japanese_rom.read_bytes()
        hf9=apply(source_rom,(ROOT/'patches/historical/Chocobo_EN_v1.1_HF9_TEST_JP_CCAA4853.bps').read_bytes())
        patch=(ROOT/'patches/historical/Chocobo_EN_v1.1_HF10_TEST_JP_CCAA4853.bps').read_bytes()
        hf10=apply(source_rom,patch)
        assert sha(hf9)==manifest['previous_hf9']['sha256']
        changed=[i for i,(a,b) in enumerate(zip(hf9,hf10)) if a!=b]
        allowed=lambda i: 0x155155<=i<0x156b05 or 0x15fd58<=i<0x15ffc9 or i>=len(hf10)-2
        assert len(changed)==370 and all(allowed(i) for i in changed)
        assert hf9[0x15fd00:0x15fd58]==hf10[0x15fd00:0x15fd58]
        lo=0x155155+328*16; hi=0x155155+392*16
        assert hf9[lo:hi]==hf10[lo:hi]
        assert patch==(ROOT/'patches/historical/Chocobo_EN_v1.1_HF10_TEST_JP_CCAA4853.bps').read_bytes()
        result.update(binary_comparison='PASS_TITLE_RESOURCES_AND_CHECKSUM_ONLY',changed_bytes_vs_hf9=len(changed))
    return result


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--japanese-rom',type=Path)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args(); result=verify(args.japanese_rom)
    text=json.dumps(result,indent=2)+'\n'
    if args.out: args.out.write_text(text)
    print(text)
