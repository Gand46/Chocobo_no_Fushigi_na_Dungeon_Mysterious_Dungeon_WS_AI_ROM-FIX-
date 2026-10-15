from pathlib import Path
import csv,json
out=[]
for name in ['release_menu_empty','release_menu_saved','release_save_native','release_load_saved']:
 r=Path('qa20/runs')/name
 rows=list(csv.DictReader((r/'getters.csv').open()));story=list(csv.DictReader((r/'story.csv').open()))
 out.append({'run':name,'getter_bindings':sorted({f'W{int(x["window"]):02X}/F{int(x["family"]):02d}:I{int(x["index"]):03d}'for x in rows}),'story_bindings':sorted({f'G{int(x["group"]):02d}:M{int(x["message"]):03d}'for x in story}),'scope':'Native consumer trace, no assumed link to G16 labels'})
Path('qa20/consumer_bindings.json').write_text(json.dumps(out,indent=2))
