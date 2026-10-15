from pathlib import Path
import sys,hashlib
from reference_bps.bps import apply
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
from build import build
source=Path(sys.argv[1]).read_bytes();rom,patch,_=build(source)
actual=apply(source,patch)
assert actual==rom
print("Independent BPS PASS",hashlib.sha256(actual).hexdigest())
