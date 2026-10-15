from pathlib import Path
import csv,json,re,sys
R=Path('delivery/Chocobo_EN_v1.1_HF13_TEST_Fuentes_QA18_M4_20261014');sys.path.insert(0,str(R/'qa15'));from inventory_layout import story_inventory,words_until_end
rom=Path('qa18/private/hf13_release/Chocobo_EN_v1.1_HF13_TEST.ws').read_bytes();st,_=story_inventory(rom,'HF13');byid={x['id']:x for x in st};targets={};menus=set();bindings=set();counts={}
for qa in ['qa16','qa17','qa18']:
 idx=json.loads((R/f'docs/{qa.upper()}_RUN_INDEX.json').read_text());good=[x for x in idx if x['status']=='PASS_SYNTHETIC_SCOPED'];counts[qa]=len(good)
 for x in good:
  name=x['run'];match=re.search(r'(G\d\d)_M(\d\d\d)',name)
  if match:
   ident=f'{match[1]}:M{match[2]}';targets.setdefault(ident,[]).append(f'{qa}/{name}')
  if qa=='qa18'and name=='final_slot_native':targets.setdefault('G16:M064',[]).append('qa18/final_slot_native')
  p=R/f'evidence/{qa}_runs'/name/'getters.csv'
  if p.exists():
   for z in csv.DictReader(p.open()):menus.add(int(z['window']));bindings.add((int(z['window']),int(z['family']),int(z['index'])))
passed_ptrs={byid[x]['pointer']for x in targets};covered=[x for x in st if x['pointer']in passed_ptrs];dynamic=[x for x in st if x['dynamic']];rows=[]
for x in st:
 target=x['id']in targets;alias=x['pointer']in passed_ptrs
 rows.append({'id':x['id'],'pointer':x['pointer'],'literal_cells_present':x['max_literal_cells']>0,'dynamic':x['dynamic'],'runtime_scope':'DIRECT_TARGET_PASS_SYNTHETIC'if target else'SHARED_POINTER_BYTES_INHERITED_NOT_SEPARATE_CALLER_TEST'if alias else'NOT_VISUALLY_APPROVED_BY_M2_M4_TARGET_MATRIX','evidence':';'.join(targets.get(x['id'],[]))})
with Path('qa18/story_coverage.csv').open('w',newline='')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary={'scope':'M2/M3/M4 approved target cases only; incidental reads never become visual approvals','approved_runs_per_iteration':counts,'direct_target_story_references':len(targets),'unique_target_story_pointers':len(passed_ptrs),'references_sharing_target_pointers':len(covered),'dynamic_references':len(dynamic),'dynamic_references_sharing_tested_pointers':sum(x['pointer']in passed_ptrs for x in dynamic),'getter_window_ids_observed':sorted(menus),'getter_windows_observed':len(menus),'getter_bindings_observed':len(bindings),'getter_total_entries':2333,'window_total_presets':141,'story_literal_reference_denominator':886,'global_visual_approval':False,'inheritance_rule':'HF12 -> HF13 changes restricted to five enumerated non-dynamic message spans and checksum; all getter streams, pointer bindings, code, font/title graphics unchanged. Historical approvals retain original access and scope.'}
Path('qa18/coverage_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
