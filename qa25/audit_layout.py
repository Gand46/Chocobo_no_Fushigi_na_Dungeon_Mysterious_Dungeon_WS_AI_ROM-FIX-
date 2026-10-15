#!/usr/bin/env python3
"""Read-only HF19 layout triage. Heuristics are review queues, not visual PASS.

Usage: python3 qa25/audit_layout.py --rom build/Chocobo_EN_v1.1_HF19_TEST.ws
"""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from qa15.inventory_layout import getter_inventory, story_inventory, window_inventory, words_until_end

EXPECTED_ROM_SHA256 = "f27e69f65e134b161c1f3ce263c3ed78a8ae247997c95d7383c43c4a78c8962f"
ARGUMENT_CONTROLS = {0xfff4, 0xfff8, 0xfffa, 0xfffb}


def pages(words):
    """Count literal cells per authored line and screen segment, skipping arguments.

    FFF2 can pause without clearing the box. Treat the segment as a review unit,
    not an assertion about the native page or its runtime window.
    """
    segments = []
    lines = []
    line = []
    dynamic = False
    controls = []
    i = 0
    while i < len(words):
        v = words[i]
        i += 1
        if v in ARGUMENT_CONTROLS:
            controls.append(f"{v:04X}")
            dynamic |= v in (0xfff4, 0xfff8)
            i += 1
        elif v == 0xfffe:
            lines.append(line)
            line = []
        elif v in (0xfff2, 0xfffc, 0xfffd):
            if line or lines:
                lines.append(line)
                segments.append(lines)
            lines = []
            line = []
            controls.append(f"{v:04X}")
        elif v >= 0xfff0:
            controls.append(f"{v:04X}")
        else:
            line.append(v)
    if line or lines:
        lines.append(line)
        segments.append(lines)
    return segments, dynamic, controls


def line_info(line):
    tail = len(line) - len(list_trimmed(line))
    return len(line), len(line) - tail, tail


def list_trimmed(line):
    result = list(line)
    while result and result[-1] == 0:
        result.pop()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=ROOT / "qa25" / "results")
    args = parser.parse_args()
    data = args.rom.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_ROM_SHA256:
        parser.error(f"HF19 ROM hash mismatch: {digest}")
    story, _ = story_inventory(data, "HF19")
    getters, _ = getter_inventory(data, "HF19")
    windows = window_inventory(data)
    rows = []
    for resource in story:
        words, _, terminated = words_until_end(data, int(resource["pointer"], 16))
        segments, dynamic, controls = pages(words)
        raw = [[line_info(line)[0] for line in segment] for segment in segments]
        visible = [[line_info(line)[1] for line in segment] for segment in segments]
        trailing = sum(line_info(line)[2] for segment in segments for line in segment)
        literal = sum(sum(segment) for segment in visible)
        if not literal:
            continue
        risk = "NONE"
        reasons = []
        if any(n > 13 for segment in visible for n in segment):
            risk = "VISIBLE_OVER_13"
            reasons.append("visible literal cells exceed 13")
        if dynamic:
            reasons.append("dynamic value: static line width cannot bound rendered value")
        imbalances = []
        for segment in visible:
            nonempty = [n for n in segment if n]
            if len(nonempty) == 2:
                imbalances.append(max(nonempty) - min(nonempty))
        max_imbalance = max(imbalances, default=0)
        if risk == "NONE" and max_imbalance >= 6:
            risk = "BALANCE_REVIEW"
            reasons.append("two authored lines differ by at least six cells")
        if risk == "NONE" and trailing:
            risk = "PADDING_ONLY"
            reasons.append("trailing empty cells only")
        rows.append({
            "id": resource["id"], "pointer": resource["pointer"],
            "stream_sha256": resource["stream_sha256"], "risk": risk,
            "raw_segments": json.dumps(raw), "visible_segments": json.dumps(visible),
            "max_imbalance_cells": max_imbalance, "trailing_blank_cells": trailing,
            "dynamic": dynamic, "controls": " ".join(controls),
            "terminated": terminated, "reason": "; ".join(reasons),
        })
    assert len(story) == 3488 and len(getters) == 2333 and len(rows) == 886
    assert all(x["terminated"] for x in rows)
    counts = Counter(x["risk"] for x in rows)
    summary = {
        "rom_sha256": digest,
        "status": "STATIC_TRIAGE_ONLY_NOT_GLOBAL_VISUAL_APPROVAL",
        "story_entries": len(story), "story_literal_resources": len(rows),
        "getter_entries": len(getters), "window_presets": len(windows),
        "risk_counts": dict(counts),
        "dynamic_literal_resources": sum(x["dynamic"] for x in rows),
        "raw_over_13": [x["id"] for x in rows if any(n > 13 for p in json.loads(x["raw_segments"]) for n in p)],
        "visible_over_13": [x["id"] for x in rows if x["risk"] == "VISIBLE_OVER_13"],
        "unbound_getters_nominal_over_208px": sum(x["common_copy_nominal_px"] > 208 for x in getters),
        "limitations": [
            "Balance is an editorial heuristic. Short trailing lines, names and deliberate pauses are not errors by count alone.",
            "FFF2 is a pause and does not necessarily clear the native window.",
            "Dynamic substitutions and shared/composed getter consumers need native runtime window traces.",
            "Static counts do not establish natural scene reachability, legibility, or actual on-screen margins.",
        ],
    }
    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / "story_layout.csv").open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (args.out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
