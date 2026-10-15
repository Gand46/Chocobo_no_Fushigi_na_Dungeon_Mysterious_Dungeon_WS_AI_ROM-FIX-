from pathlib import Path
import os,shutil,json,hashlib
root=Path('qa5/save_fixtures');root.mkdir(exist_ok=True)
b=Path('runs/q4_hf3_save_verified/native_save/Chocobo_EN_v1.1_HF3_TEST.sav').read_bytes()
assert b[0x75b0:0x75b4]==b'n_c1'
cases={ 'baseline':b, 'marker_bad':b[:0x75b0]+b'\0'+b[0x75b1:], 'payload_level2':b[:0x765b]+bytes([2])+b[0x765c:] }
for name,data in cases.items():
 p=root/(name+'.sav');p.write_bytes(data)
 (root/(name+'.json')).write_text(json.dumps({'method':'SYNTHETIC_SAVE_MUTATION'if name!='baseline'else'UNMODIFIED_NATIVE_SAVE','source_sha256':hashlib.sha256(b).hexdigest(),'sha256':hashlib.sha256(data).hexdigest(),'changed_offsets':[hex(i)for i,(x,y)in enumerate(zip(b,data))if x!=y]},indent=2))
for profile in ['q5_marker','q5_payload','q5_jp','q5_en']:
 p=Path('profiles')/profile;p.mkdir()
 for n in ['Mesen','MesenCore.so','libSkiaSharp.so','libHarfBuzzSharp.so','MesenNesDB.txt']:os.link(Path('emulator')/n,p/n)
 (p/'settings.json').write_text('{}');(p/'Saves').mkdir()
shutil.copy2(root/'marker_bad.sav','profiles/q5_marker/Saves/Chocobo_EN_v1.1_HF3_TEST.sav')
shutil.copy2(root/'payload_level2.sav','profiles/q5_payload/Saves/Chocobo_EN_v1.1_HF3_TEST.sav')
