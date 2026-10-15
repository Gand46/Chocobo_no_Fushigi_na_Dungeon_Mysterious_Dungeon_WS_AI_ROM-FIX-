from pathlib import Path
import json,shutil
R=Path('delivery/Chocobo_EN_v1.1_HF14_TEST_Fuentes_QA19_V1_20261014');B=Path('qa19/private/hf14_release');p=R/'manifest.json';m=json.loads(p.read_text());b=json.loads((B/'build_result.json').read_text());m['changed_bytes_vs_english']=b['changed_bytes_vs_legacy'];m['bps_sha256']=b['bps_sha256'];p.write_text(json.dumps(m,indent=2)+'\n')
for dest in [R/'patches',Path('delivery')]:shutil.copy2(B/'Chocobo_EN_v1.1_HF14_TEST_JP_CCAA4853.bps',dest/'Chocobo_EN_v1.1_HF14_TEST_JP_CCAA4853.bps')
p=R/'tests/test_project.py';s=p.read_text().replace("m['changed_bytes_vs_english'],4660",f"m['changed_bytes_vs_english'],{b['changed_bytes_vs_legacy']}");p.write_text(s)
p=R/'qa15/inventory_layout.py';s=p.read_text().replace('first=u16(r,b+off);count=(first-off)//2', '''first=u16(r,b+off);count=(first-off)//2
        # QA19: G16 M000 is relocated. Resource address is no longer a table boundary.
        # Verified JP/HF13 table 06:CB86..06:CD86 contains exactly 256 entries.
        if group==16 and bank==6 and off==0xcb86:
            count=256;first=off+2*count''');p.write_text(s)
print(b)
