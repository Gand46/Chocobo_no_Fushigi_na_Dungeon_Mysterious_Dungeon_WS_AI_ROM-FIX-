from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,csv
import argparse
p=argparse.ArgumentParser();p.add_argument('--runs',type=Path,default=Path(__file__).resolve().parents[1]/'evidence/qa11_runs');p.add_argument('--assets',type=Path,default=Path(__file__).resolve().parents[1]/'assets/title/user_v01');p.add_argument('--out',type=Path,default=Path(__file__).resolve().parent);args=p.parse_args()
root=args.out;root.mkdir(parents=True,exist_ok=True);d=args.runs/'q11_animation';ref=args.runs/'q11_animation_hf7_control'
source=np.array(Image.open(args.assets/'build/frames/frame_000.png'))
pal=np.array([[43,43,38],[152,149,139],[171,167,156],[224,219,205]],dtype=np.uint8)
expected=pal[source[64:121]]
r={'frames_compared':0,'top_56_mismatches':[],'footer_121_143_mismatches':[],'logo_64_120_mismatches':[],'all_animation_map_frames_equal':(d/'animation_map.csv').read_bytes()==(ref/'animation_map.csv').read_bytes()}
poses={};states={};prompt={}
for f in sorted(d.glob('anim*.png')):
 a=np.array(Image.open(f))[:144];b=np.array(Image.open(ref/f.name))[:144];r['frames_compared']+=1
 if not np.array_equal(a[:56],b[:56]):r['top_56_mismatches'].append(f.name)
 if not np.array_equal(a[121:],b[121:]):r['footer_121_143_mismatches'].append(f.name)
 if not np.array_equal(a[64:121],expected):r['logo_64_120_mismatches'].append(f.name)
 k=hashlib.sha256(a[:56].tobytes()).hexdigest();poses.setdefault(k,f.name)
 k=hashlib.sha256(a.tobytes()).hexdigest();states.setdefault(k,f.name)
 k=hashlib.sha256(a[121:].tobytes()).hexdigest();prompt.setdefault(k,f.name)
r.update(unique_top_states=len(poses),unique_full_states=len(states),unique_footer_states=len(prompt),pose_representatives=poses,footer_representatives=prompt)
r['all_animation_map_frames_equal_explanation']='BG1 contains intentionally replaced static artwork; comparison is diagnostic only. Animation checks use visible top/footer equality plus asset/code byte identity.'
(root/'animation_validation.json').write_text(json.dumps(r,indent=2))
print(json.dumps({k:v for k,v in r.items() if not isinstance(v,dict)},indent=2))
# Store native uncropped proof images, with original LCD indicators retained.
for i,f in enumerate(poses.values()):Image.open(d/f).save(root/f'pose_{i:02}.png')
