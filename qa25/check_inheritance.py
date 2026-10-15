#!/usr/bin/env python3
"""Confirm that historical QA25 review targets were not modified in HF19."""
import csv
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from qa15.inventory_layout import story_inventory
from qa24.rebuild_translation_edits import reconstruct


def main():
    japanese = Path(os.environ["CONTINUITY_INPUT_JP"]).read_bytes()
    hf18 = reconstruct(japanese)
    hf19 = (ROOT / "build/Chocobo_EN_v1.1_HF19_TEST.ws").read_bytes()
    old = {x["id"]: x for x in story_inventory(hf18, "HF18")[0]}
    new = {x["id"]: x for x in story_inventory(hf19, "HF19")[0]}
    with (ROOT / "qa25/results/story_layout.csv").open(encoding="utf-8") as f:
        ids = [x["id"] for x in csv.DictReader(f) if x["risk"] == "BALANCE_REVIEW"]
    changed = [x for x in ids if old[x]["stream_sha256"] != new[x]["stream_sha256"]]
    assert len(ids) == 99 and not changed, changed
    result = {"status": "PASS_EXACT_STREAM_EQUIVALENCE_HF18_TO_HF19",
              "japanese_sha256": hashlib.sha256(japanese).hexdigest(),
              "hf18_sha256": hashlib.sha256(hf18).hexdigest(),
              "hf19_sha256": hashlib.sha256(hf19).hexdigest(),
              "identical_story_streams": ids, "changed": changed,
              "limitation": "This does not prove equality to each older screenshot phase or natural consumer reachability."}
    (ROOT / "qa25/results/hf18_equivalence.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "count": len(ids), "changed": changed}))


if __name__ == "__main__":
    main()
