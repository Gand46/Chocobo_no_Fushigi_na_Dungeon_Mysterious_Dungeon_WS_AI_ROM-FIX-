from pathlib import Path
import shutil,json,hashlib,zlib,struct
BASE=Path('delivery/Chocobo_EN_v1.1_HF10_TEST_Fuentes_QA14_20261014')
OUT=Path('delivery/Chocobo_EN_v1.1_HF11_TEST_Fuentes_QA15_M1_20261014')
OLD=Path('qa14/private/hf10_final/Chocobo_EN_v1.1_HF10_TEST.ws').read_bytes()
assert hashlib.sha256(OLD).hexdigest()=='aacb4fc13587eda56923548f8fad9f8dac83ff24d4ddb1a0372cddcb3475f39f'
assert OLD[0x65220:0x65226].hex()=='06010000feff'
NEW=bytearray(OLD);NEW[0x65220:0x65226]=bytes.fromhex('feff06010000');NEW[-2:]=struct.pack('<H',sum(NEW[:-2])&65535)
assert sum(a!=b for a,b in zip(OLD,NEW))==6
before=struct.unpack_from('<29H',OLD,0x65206);after=struct.unpack_from('<29H',NEW,0x65206)
assert [x for x in before if x<0xfff0]==[x for x in after if x<0xfff0]
assert after[13]==0xfffe and after[27:]==(0xfff2,0xffff)
assert OLD[:0x65220]==NEW[:0x65220] and OLD[0x65226:]==NEW[0x65226:]
shutil.copytree(BASE,OUT)
hist=OUT/'docs/history/qa14';hist.mkdir(parents=True,exist_ok=True)
for n in ('README.md','INFORME_ES.md','CONTEXTO_CONTINUACION.md','manifest.json'):
 shutil.copy2(OUT/n,hist/n)
p=OUT/'src/corrections.json';d=json.loads(p.read_text());d['edits'].append({'id':'DIALOG_G05_M002_REFLOW','offset':'0x065220','before':'06010000feff','after':'feff06010000','reason':'HF11 QA15 M1: move explicit newline before go; preserve every glyph and stream length. Native 13-cell consumer otherwise drops go and prematurely scrolls first line.'});p.write_text(json.dumps(d,indent=2)+'\n')
p=OUT/'build.py';s=p.read_text().replace('HF10','HF11');s=s.replace('HF11 native-grid subtitle for legibility','native-grid subtitle for legibility; HF11 scoped G05:M002 line break repair');p.write_text(s)
p=OUT/'manifest.json';m=json.loads(p.read_text());m['previous_hf10']=dict(m['target']);m['version']='1.1-HF11-TEST';m['audit_revision']='QA15_GLOBAL_LAYOUT_M1';m['target']={'bytes':len(NEW),'sha256':hashlib.sha256(NEW).hexdigest(),'crc32':f'{zlib.crc32(NEW)&0xffffffff:08X}','ws_checksum':f'{sum(NEW[:-2])&65535:04X}'}
m['rom_changes_in_QA15']=6;m['changed_bytes_vs_hf10']=6;m['new_bps_required']=True;m['corrected_resources']+=1
m['changed_bytes_vs_english']+=6
m['changed_bytes_vs_japanese']=sum(a!=b for a,b in zip(Path('qa14/private/Chocobo no Fushigi na Dungeon (J) [M].ws').read_bytes(),NEW))
m['layout_iteration']={'completed':1,'planned':4,'remaining_base':3,'global_approval':False}
p.write_text(json.dumps(m,indent=2)+'\n')
Path('qa15/hf11_expected.json').write_text(json.dumps(m['target'],indent=2)+'\n')
print(m['target'])
