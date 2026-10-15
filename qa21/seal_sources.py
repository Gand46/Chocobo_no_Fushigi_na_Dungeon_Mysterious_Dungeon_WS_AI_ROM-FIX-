from pathlib import Path
import hashlib,json
R=Path('work/Chocobo_QA20_V2');lines=[];bad=[]
for p in sorted(R.rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(R)
 if rel.parts[0]in ['build','dist','.continuity'] or '__pycache__'in rel.parts or p.suffix=='.pyc' or str(rel)=='SHA256SUMS.txt':continue
 if p.suffix.lower()in ['.ws','.wsc','.gba','.gb','.gbc']:bad.append(str(rel))
 lines.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+rel.as_posix())
assert not bad,bad
(R/'SHA256SUMS.txt').write_text('\n'.join(lines)+'\n');print({'files':len(lines),'commercial_rom_files':len(bad)})
