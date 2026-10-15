from pathlib import Path
import shutil,json,hashlib,zlib
base=Path('delivery/Chocobo_EN_v1.1_HF2_TEST_Fuentes_QA_20261013');out=Path('delivery/Chocobo_EN_v1.1_HF3_TEST_Fuentes_QA_20261013')
shutil.copytree(base,out)
m=json.loads((out/'manifest.json').read_text());r=Path('private_roms/PROBE_WHISTLE.ws').read_bytes();hf2=Path('private_roms/hf2_build/Chocobo_EN_v1.1_HF2_TEST.ws').read_bytes()
m['version']='1.1-HF3-TEST';m['previous_hf2']=m['target'];m['target']={'bytes':len(r),'sha256':hashlib.sha256(r).hexdigest(),'crc32':f'{zlib.crc32(r):08X}','ws_checksum':r[-2:][::-1].hex().upper()};m.pop('bps_sha256')
for key,file in [('english','EN.ws'),('japanese','JP.ws'),('hf1','Chocobo_EN_v1.1_HF1_TEST.ws')]:m['changed_bytes_vs_'+key]=sum(x!=y for x,y in zip(r,Path('private_roms',file).read_bytes()))
m['changed_bytes_vs_hf2']=sum(x!=y for x,y in zip(r,hf2));m['intentional_near_pointer_edits']=5;m['whistle_visual']='PASS_SYNTHETIC_MESEN';m['whistle_resource_pointer_edits']=2;m['whistle_resource_blocks']=2;m['physical_cartridge_incident']='ELECTRICAL_CAUSE_ESTABLISHED_BY_USER_OUT_OF_ROM_SCOPE';m['native_save_load']='PENDING_HF3_RERUN'
(out/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
c=json.loads((out/'src/corrections.json').read_text());c['edits']+=json.loads(Path('qa4/whistle_edits.json').read_text());(out/'src/corrections.json').write_text(json.dumps(c,indent=2)+'\n')
s=(out/'build.py').read_text().replace('HF2','HF3').replace('HF1 text fixes + invalid model guard; absent Lafoss animation not reconstructed','HF1 text fixes + Lafoss guard + Whistle resource repair; full Lafoss semantics pending');(out/'build.py').write_text(s)
for file in ['BUILD.bat','BUILD.command']:
 p=out/file;p.write_text(p.read_text().replace('HF2','HF3'))
# Keep prior phase reports as history, not current authority.
h=out/'docs/history/hf2';h.mkdir(parents=True,exist_ok=True)
for file in ['README.md','INFORME_ES.md','CONTEXTO_CONTINUACION.md','CHANGELOG.md']:
 shutil.copy2(out/file,h/file)
shutil.copy2(base/'manifest.json',h/'manifest.json');shutil.copy2(base/'docs/quality_gates.json',h/'quality_gates.json')
shutil.copytree('qa4',out/'qa4',ignore=shutil.ignore_patterns('__pycache__','*.bin'))
print(out,m['target'],m['changed_bytes_vs_hf2'])
