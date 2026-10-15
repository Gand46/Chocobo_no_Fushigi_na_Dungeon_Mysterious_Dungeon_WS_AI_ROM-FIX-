from pathlib import Path
import json,hashlib,shutil
ROOT=Path('work/Chocobo_QA20_V2');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['release_build.py','verify_scope.py','build_portable_generator.py','rebuild_translation_edits.py']:
 shutil.copy2(Path('qa20')/name,ROOT/'qa20'/name)
c=json.loads((ROOT/'CONTINUITY.json').read_text())
c['required_paths']=['AGENTS.md','tools/continuity.py','build.py','manifest.json','src/legacy_translation_ranges.json','src/corrections.json','qa20/translations.json','qa20/text_codec.py','qa20/rebuild_translation_edits.py','qa20/release_build.py','qa20/verify_scope.py','qa20/linguistic_review.json','qa20/visual_readings.json','PROJECT_CONTEXT.md']
c['external_inputs']=[{'id':'japanese_rom','env':'CONTINUITY_INPUT_JP','kind':'file','sha256':'38fd168a8cefa4ed80db42eed9f720e42da5b8f71d551c707520b24060c14728','size':2097152}]
c['build']={'argv':['{python}','qa20/release_build.py'],'timeout_seconds':60,'artifacts':[{'path':'build/Chocobo_EN_v1.1_HF15_TEST_JP_CCAA4853.bps','sha256':sha(ROOT/'patches/Chocobo_EN_v1.1_HF15_TEST_JP_CCAA4853.bps')},{'path':'build/release_build_result.json','sha256':sha(ROOT/'build/release_build_result.json')}]}
c['bps_roundtrip']={'base_input':'japanese_rom','patch_path':'build/Chocobo_EN_v1.1_HF15_TEST_JP_CCAA4853.bps','target_path':'build/Chocobo_EN_v1.1_HF15_TEST.ws'}
(ROOT/'CONTINUITY.json').write_text(json.dumps(c,indent=2)+'\n')
name='Chocobo_EN_v1.1_HF14_TEST_JP_CCAA4853.bps'
(ROOT/'CONTINUITY_MIGRATIONS.json').write_text(json.dumps([{'path':'patches/'+name,'old_sha256':sha(ROOT/'patches/historical'/name),'action':'move','to':'patches/historical/'+name,'reason':'Conservar intacto HF14 como evidencia histórica; HF15 es el parche acumulativo activo.'}],indent=2)+'\n')
