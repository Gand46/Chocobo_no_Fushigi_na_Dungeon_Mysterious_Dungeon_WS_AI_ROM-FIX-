from pathlib import Path
import json,shutil,struct
w=Path.cwd();old=w/'delivery/Chocobo_EN_v1.1_HF8_TEST_Fuentes_QA11_20261014';root=w/'delivery/Chocobo_EN_v1.1_HF9_TEST_Fuentes_QA12_20261014'
shutil.copytree(old,root,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
history=root/'docs/history/hf8_qa11';history.mkdir(parents=True,exist_ok=True)
for name in ['README.md','INFORME_ES.md','CONTEXTO_CONTINUACION.md','CONTEXTO_PROYECTO.md','manifest.json','CHANGELOG.md','docs/approval_matrix.json','docs/quality_gates.json','docs/issue_register.json','docs/issue_register.csv']:
 if (root/name).is_file():shutil.copy2(root/name,history/Path(name).name)
legacy=(w/'private_roms/EN.ws').read_bytes();hf8=(w/'private_roms/hf8_release/Chocobo_EN_v1.1_HF8_TEST.ws').read_bytes()
words=[0x00D1,0x0180,0x01A3]+list(struct.unpack('<10H',hf8[0x15b874:0x15b888]))+[0xffff]
assert len(words)==14
changes=[('PROPERTY_UNDEAD_TEXT',0x15caee,struct.pack('<14H',*words),'Replace malformed undead ability wording with existing native English Strong to Undead! glyphs; retains Skill prefix and slot.'),('PROPERTY_THREE_WAY_END',0x15cba6,b'\xff\xff','End after Skill3pronged hit; suppress stray o,af suffix without altering the neighboring resource.'),('PROPERTY_FIRE_SADDLE_TAIL',0x15cfb0,b'\x00\x00','Replace stray af glyph with the same blank as the parallel talon Fire type resource.')]
c=json.loads((root/'src/corrections.json').read_text());c['edits']=[e for e in c['edits'] if not e['id'].startswith('PROPERTY_')]
for name,a,new,reason in changes:
 assert legacy[a:a+len(new)]==hf8[a:a+len(new)]
 c['edits'].append({'id':name,'offset':f'0x{a:06X}','before':legacy[a:a+len(new)].hex(),'after':new.hex(),'reason':reason})
(root/'src/corrections.json').write_text(json.dumps(c,indent=2)+'\n')
s=(root/'build.py').read_text().replace('HF8','HF9').replace('TitanSaddle residual glyph;','TitanSaddle residual glyph + three fused equipment text repairs;');(root/'build.py').write_text(s)
for p in (root/'patches').glob('*.bps'):p.unlink()
print(root)
