"""Clean-extraction HF17: cumulative builder and editable G09 regeneration."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build import build, PATCH_NAME

jp = Path(os.environ["CONTINUITY_INPUT_JP"])
output = ROOT / "build"
output.mkdir(exist_ok=True)
rom, bps, result = build(jp.read_bytes())
(output / "Chocobo_EN_v1.1_HF17_TEST.ws").write_bytes(rom)
(output / PATCH_NAME).write_bytes(bps)
semantic = output / "semantic"
subprocess.run([sys.executable, str(ROOT / "qa22/rebuild_translation_edits.py"),
                "--japanese-rom", str(jp), "--out", str(semantic)], check=True)
assert (semantic / "candidate.ws").read_bytes() == rom
assert json.loads((semantic / "edits.json").read_text()) == json.loads(
    (ROOT / "qa22/edits.json").read_text())
assert hashlib.sha256((ROOT / "patches/Chocobo_EN_v1.1_HF17_TEST_JP_CCAA4853.bps").read_bytes()).hexdigest() == result["bps_sha256"]
result["editable_regeneration"] = "PASS_EXACT_ROM_AND_EDITS"
(output / "release_build_result.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
