"""Revalidate the frozen HF16 V3 release from the cumulative source tree."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument("--japanese-rom", type=Path, required=True)
p.add_argument("--out", type=Path, required=True)
a = p.parse_args()
out = a.out.resolve()
out.mkdir(parents=True, exist_ok=True)
jp = a.japanese_rom.resolve()
manifest = json.loads((ROOT / "manifest.json").read_text())
assert hashlib.sha256(jp.read_bytes()).hexdigest() == manifest["original"]["sha256"]

def run(name, argv, env=None):
    process = subprocess.run(argv, cwd=ROOT, env=env, text=True,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (out / (name + ".log")).write_text(process.stdout)
    if process.returncode:
        raise RuntimeError(f"{name} failed; see {out / (name + '.log')}")

env = os.environ.copy()
env["CONTINUITY_INPUT_JP"] = str(jp)
run("release_build", [sys.executable, "qa21/release_build.py"], env)
run("scope", [sys.executable, "qa21/verify_scope.py", "--japanese-rom",
              str(jp), "--out", str(out / "scope.json")])
run("supplemental", [sys.executable, "qa21/verify_supplemental.py",
                     "--out", str(out / "supplemental.json")])
run("tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])
scope = json.loads((out / "scope.json").read_text())
supplemental = json.loads((out / "supplemental.json").read_text())
assert scope["context_pending"] == ["G06:M100", "G11:M011"]
assert scope["scoped_pass"] == 205 and not scope["global_visual_approved"]
assert supplemental["native_readings"] == 100 and supplemental["archived_result_unchanged"]
summary = {
    "status": "PASS_HF16_V3_SCOPED_REVALIDATION",
    "japanese_sha256": manifest["original"]["sha256"],
    "hf16_sha256": manifest["target"]["sha256"],
    "bps_sha256": manifest["bps_sha256"],
    "scope_checks": scope["checks"],
    "supplemental_revalidation_checks": supplemental["revalidation_checks"],
    "references_reviewed": scope["references_reviewed"],
    "scoped_pass": scope["scoped_pass"],
    "context_pending": scope["context_pending"],
    "global_visual_approved": False,
    "global_linguistic_approved": False,
}
(out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
