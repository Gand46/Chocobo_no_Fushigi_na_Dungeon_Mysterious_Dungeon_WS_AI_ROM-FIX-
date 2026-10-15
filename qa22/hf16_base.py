"""Reconstruct the pinned HF16 base from the same clean Japanese input."""
from pathlib import Path
import hashlib,json,os,struct,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from build import replace_checked

def input_path():
 return Path(os.environ.get('CONTINUITY_INPUT_JP',str(ROOT.parent/'jp_clean.ws')))

def reconstruct(japanese):
 m=json.loads((ROOT/'docs/history/qa21/manifest_hf16.json').read_text())
 assert hashlib.sha256(japanese).hexdigest()==m['original']['sha256']
 image=bytearray(japanese)
 replace_checked(image,json.loads((ROOT/'src/legacy_translation_ranges.json').read_text())['edits'])
 replace_checked(image,json.loads((ROOT/'docs/history/qa21/corrections_hf16.json').read_text())['edits'])
 image[-2:]=struct.pack('<H',sum(image[:-2])&65535)
 assert hashlib.sha256(image).hexdigest()==m['target']['sha256']
 return bytes(image)
