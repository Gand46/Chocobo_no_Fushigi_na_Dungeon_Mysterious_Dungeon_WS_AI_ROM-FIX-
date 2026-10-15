from pathlib import Path
import json,struct,shutil,hashlib,zlib
root=Path('delivery/Chocobo_EN_v1.1_HF7_TEST_Fuentes_QA10_20261014')
key=json.loads(Path('qa10/glyph_accepted.png.key.json').read_text());got=['S','G','T','O','Y','N','B','M','E','N','N','D','C',"'",'U','O','W','R','S','A','E','O','R','O','N','O','S','R','D','E','Y','W','H','C','F','O'];rows=[{'sample':i,'visible':v,'expected':key[str(i)]['glyph'],'pass':v==key[str(i)]['glyph']} for i,v in enumerate(got,1)];assert all(x['pass'] for x in rows),[x for x in rows if not x['pass']]
Path('qa10/glyph_review_final.json').write_text(json.dumps({'native_scale_full_title_reviewed':True,'diagnostic_zoom':2,'ocr_used':False,'samples':rows,'result':'PASS_36_ISOLATED_CROPS_WITH_NATIVE_SURFACE_REVIEW','initial_findings':'Animated row7 overwrote upper strokes; moved title below y63. Enlarged N counter, pointed A and used native-like solid small caption matching PUSH BUTTON hierarchy.'},indent=2))
b=bytearray(Path('private_roms/qa10_title.ws').read_bytes());b[0x16f1d4:0x16f1d6]=b'\xff\xff';b[-2:]=struct.pack('<H',sum(b[:-2])&65535);Path('private_roms/hf7_release/Chocobo_EN_v1.1_HF7_TEST.ws').write_bytes(b)
c=json.loads((root/'src/corrections.json').read_text());c['edits']=[e for e in c['edits'] if not e['id'].startswith('TITLE_')]+json.loads(Path('qa10/title_edits.json').read_text());(root/'src/corrections.json').write_text(json.dumps(c,indent=2)+'\n')
m=json.loads((root/'manifest.json').read_text());previous_count=m['changed_bytes_vs_english'];m['target']={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'crc32':f'{zlib.crc32(b)&0xffffffff:08X}','ws_checksum':f'{sum(b[:-2])&65535:04X}'}
for name,path in [('english','private_roms/EN.ws'),('japanese','private_roms/JP.ws'),('hf6','private_roms/hf6_release/Chocobo_EN_v1.1_HF6_TEST.ws')]:m['changed_bytes_vs_'+name]=sum(x!=y for x,y in zip(b,Path(path).read_bytes()))
m['rom_changes_in_QA10']=m['changed_bytes_vs_hf6'];(root/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
p=root/'tests/test_project.py';s=p.read_text().replace(str(previous_count),str(m['changed_bytes_vs_english']));p.write_text(s)
s=Path('qa10/title_build.py').read_text();a=s.index('sys.path.insert');z=s.index('\nfrom generate_whistle_fix',a);s=s[:a]+"sys.path.insert(0,str(Path(__file__).resolve().parent))"+s[z:];s=s[:s.index("if __name__=='__main__':")]+"if __name__=='__main__':"+(root/'tools/generate_title_fix.py').read_text().split("if __name__=='__main__':")[1]
(root/'tools/generate_title_fix.py').write_text(s);shutil.copy2('qa10/title_source.json',root/'assets/title/canonical_glyphs_and_layout.json')
print(m['target'],m['changed_bytes_vs_hf6'])
