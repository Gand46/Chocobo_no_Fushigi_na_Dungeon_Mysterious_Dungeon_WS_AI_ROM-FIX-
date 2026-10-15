#!/usr/bin/env python3
"""Check six editorial reflow ideas without changing any ROM or source translation."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from qa15.inventory_layout import story_inventory, words_until_end
from qa21.text_codec import encode

EXPECTED_ROM = "f27e69f65e134b161c1f3ce263c3ed78a8ae247997c95d7383c43c4a78c8962f"
PROPOSALS = {
    "G00:M044": (20, ["Put the pot in", "a sunny spot."]),
    "G06:M054": (21, ["The Professor has", "the fourth book."]),
    "G06:M063": (21, ["The Professor", "has the book."]),
    "G07:M003": (21, ["A few more things", "will change."]),
    "G08:M004": (21, ["Could he have", "found a dungeon?"]),
    "G09:M141": (22, ["So he really", "is a good guy."]),
}


def main():
    data = (ROOT / "build/Chocobo_EN_v1.1_HF19_TEST.ws").read_bytes()
    assert hashlib.sha256(data).hexdigest() == EXPECTED_ROM
    rows = {x["id"]: x for x in story_inventory(data, "HF19")[0]}
    result = []
    for ident, (phase, lines) in PROPOSALS.items():
        old = rows[ident]
        source = json.loads((ROOT / f"qa{phase}/translations.json").read_text())[ident]["text"]
        assert " ".join(lines) == source, ident
        words, _, terminated = words_until_end(data, int(old["pointer"], 16))
        assert terminated and old["unique_pointer"] and not old["dynamic"]
        controls = [w for w in words if w >= 0xfff0]
        assert controls == [0xfffe, 0xfff2], (ident, controls)
        before = [len(x) for x in (words[:words.index(0xfffe)], words[words.index(0xfffe) + 1:-1])]
        encoded = [encode(s) for s in lines]
        assert all(x is not None and len(x) <= 13 for x in encoded)
        after = [len(x) for x in encoded]
        assert sum(after) <= sum(before), ident
        result.append({"id": ident, "status": "UNAPPLIED_EDITORIAL_REVIEW_CANDIDATE",
                       "source_phase": phase, "source_text": source, "before_cells": before,
                       "proposed_lines": lines, "proposed_cells": after,
                       "encoded_byte_delta": 2 * (sum(after) - sum(before)),
                       "same_wording": True, "width_limit_13": "PASS",
                       "existing_controls": [f"{w:04X}" for w in controls],
                       "runtime_status": "NOT_TESTED_AS_REFLOW"})
    target = ROOT / "qa25/results/candidate_reflows.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"candidates": len(result), "all_width_and_byte_fit": True,
                      "rom_modified": False}))


if __name__ == "__main__":
    main()
