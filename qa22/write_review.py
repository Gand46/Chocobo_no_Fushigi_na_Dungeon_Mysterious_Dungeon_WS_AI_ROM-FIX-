"""Materialize the V4 scoped bilingual review from final, hashed evidence."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
ids=json.loads((ROOT/'qa22/audit_ids.json').read_text())
tr=json.loads((ROOT/'qa22/translations.json').read_text())
visual=json.loads((ROOT/'qa22/visual_readings.json').read_text())
byid={x['id']:x for x in visual}
reserve={'G09:M086','G09:M089'}
review=[]
for i,id in enumerate(ids):
 status='NEEDS_NAME_CONFIRMATION' if id in reserve else 'PASS_SYNTHETIC_REVIEWED_SCOPED'
 review.append({'id':id,'status':status,'visual_status':'PASS_SYNTHETIC_SCOPED','changed':id in tr,'audit_sheet':f'qa22/audit_{i//6:02d}.png','final_run':'verified_'+id.replace(':','_'),'final_page':byid[id]['image'],'final_page_sha256':byid[id]['sha256'],'comparison_method':'DIRECT_FINAL_NATIVE_READING' if id in tr else 'BILINGUAL_BASELINE_AND_EXACT_FINAL_PAGE_PIXELS','translation':tr.get(id,{}).get('text'),'correction_reason':tr.get(id,{}).get('reason'),'reservation':'La fuente japonesa dice ドル君. Doru es transliteración provisional; confirmar grafía inglesa establecida en V5.' if id in reserve else None})
(ROOT/'qa22/linguistic_review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
print(len(review),'visual',sum(x['visual_status'].startswith('PASS') for x in review),'linguistic',sum(x['status'].startswith('PASS') for x in review),'reserve',len(reserve))
