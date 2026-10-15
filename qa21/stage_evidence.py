from pathlib import Path
import shutil
Q=Path('qa21');R=Path('work/Chocobo_QA20_V2');(R/'qa21').mkdir(exist_ok=True)
for p in Q.iterdir():
 if p.is_file()and not p.name.startswith('library_'):shutil.copy2(p,R/'qa21'/p.name)
for sub in ['plans','supplemental_plans','fused_suite']:shutil.copytree(Q/sub,R/'qa21'/sub,dirs_exist_ok=True)
shutil.copytree(Q/'runs',R/'evidence/qa21_runs',dirs_exist_ok=True)
print('Evidence staged; no private ROM directories copied.')
