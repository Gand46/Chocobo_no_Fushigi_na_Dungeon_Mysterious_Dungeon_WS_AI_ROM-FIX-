#!/usr/bin/env python3
"""Index historical native images for QA25 review; never relabel them HF19 runtime."""
import csv
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "qa25" / "results"
rows = list(csv.DictReader((OUT / "story_layout.csv").open(encoding="utf-8")))
rows = sorted((x for x in rows if x["risk"] == "BALANCE_REVIEW"),
              key=lambda x: (-int(x["max_imbalance_cells"]), x["id"]))
evidence = ROOT / "evidence"
prefixes = ("final_", "release2_", "verified_", "release_")


def images_for(id):
    slug = id.replace(":", "_")
    for phase in range(24, 18, -1):
        for prefix in prefixes:
            folder = evidence / f"qa{phase}_runs" / (prefix + slug)
            if not folder.is_dir():
                continue
            images = sorted(folder.glob("page_*.png"))
            if not images:
                images = sorted(folder.glob("end_text.png"))
            if images:
                return phase, images
    return None, []


index = []
for x in rows:
    phase, paths = images_for(x["id"])
    index.append({"id": x["id"], "visible_segments": json.loads(x["visible_segments"]),
                  "imbalance_cells": int(x["max_imbalance_cells"]), "evidence_phase": phase,
                  "images": [{"path": str(p.relative_to(ROOT)), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                             for p in paths], "scope": "HISTORICAL_NATIVE_SCREENSHOT" if phase != 24 else "HF19_SYNTHETIC_SCREENSHOT"})
(OUT / "balance_evidence_index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")

for start in range(0, len(index), 16):
    selection = index[start:start + 16]
    sheet = Image.new("RGB", (3 * 236, 6 * 195), "#eeeeee")
    draw = ImageDraw.Draw(sheet)
    for pos, x in enumerate(selection):
        xx, yy = (pos % 3) * 236, (pos // 3) * 195
        label = f'{x["id"]}  Δ{x["imbalance_cells"]}  QA{x["evidence_phase"] or "?"}'
        draw.text((xx + 4, yy + 4), label, fill="black")
        draw.text((xx + 4, yy + 177), str(x["visible_segments"])[:35], fill="black")
        if x["images"]:
            with Image.open(ROOT / x["images"][0]["path"]) as img:
                if img.width == 224 and img.height in (144, 157):
                    sheet.paste(img.convert("RGB"), (xx + 4, yy + 16))
                else:
                    draw.text((xx + 4, yy + 32), f"Unexpected image size: {img.size}", fill="red")
        else:
            draw.text((xx + 4, yy + 32), "NO NATIVE IMAGE", fill="red")
    sheet.save(OUT / f"balance_contact_{start // 16 + 1:02d}.png")
secondaries = [(x, n, img) for x in index for n, img in enumerate(x["images"][1:], start=2)]
for start in range(0, len(secondaries), 16):
    sheet = Image.new("RGB", (3 * 236, 6 * 195), "#eeeeee")
    draw = ImageDraw.Draw(sheet)
    for pos, (x, n, img) in enumerate(secondaries[start:start + 16]):
        xx, yy = (pos % 3) * 236, (pos // 3) * 195
        draw.text((xx + 4, yy + 4), f'{x["id"]} page {n} QA{x["evidence_phase"]}', fill="black")
        with Image.open(ROOT / img["path"]) as native:
            sheet.paste(native.convert("RGB"), (xx + 4, yy + 16))
        draw.text((xx + 4, yy + 177), str(x["visible_segments"])[:35], fill="black")
    sheet.save(OUT / f"balance_more_pages_{start // 16 + 1:02d}.png")
print(json.dumps({"candidates": len(index), "with_images": sum(bool(x["images"]) for x in index),
                  "contacts": (len(index) + 15) // 16, "secondary_pages": len(secondaries),
                  "shown_on_contacts": len(index) + len(secondaries)}))
