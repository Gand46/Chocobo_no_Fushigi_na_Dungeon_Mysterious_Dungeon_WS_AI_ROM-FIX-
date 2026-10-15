from pathlib import Path
import json,hashlib,struct,shutil
base=Path('qa5/save_fixtures/baseline.sav').read_bytes();live=Path('runs/q3_dungeon/sram.bin').read_bytes()
for floor in [1,29]:
 b=bytearray(base);b[0x75b6:0x7f8a]=live[0x6bd8:0x75ac]
 for a in [0x7303,0x7305]:struct.pack_into('<H',b,a+0x9de,floor)
 path=Path(f'qa5/save_fixtures/dungeon1_before_{floor+1}.sav');path.write_bytes(b)
 (path.with_suffix('.json')).write_text(json.dumps({'method':'SYNTHETIC_SAVE_FROM_NATIVE_DUNGEON_PAYLOAD','runtime_source':'runs/q3_dungeon/sram.bin','runtime_sha256':hashlib.sha256(live).hexdigest(),'copy':'6BD8..75AB -> 75B6..7F89','mutations':{'7303':floor,'7305':floor},'warning':'Does not establish natural late-game event flags or the exact forum path','sha256':hashlib.sha256(b).hexdigest()},indent=2))
profile=['q5_marker','q5_payload']
for pr,fl in zip(profile,[1,29]):shutil.copy2(f'qa5/save_fixtures/dungeon1_before_{fl+1}.sav',f'profiles/{pr}/Saves/Chocobo_EN_v1.1_HF3_TEST.sav')
