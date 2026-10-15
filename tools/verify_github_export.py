"""Verify the exact file inventory of the selected GitHub source export.

This inventory is distinct from the formal 115,444-file continuity snapshot.
Build outputs and Git metadata are ignored; everything else must match.
"""

import argparse
import hashlib
import json
from pathlib import Path

MANIFEST = "GITHUB_PACKAGE_MANIFEST.json"
IGNORED_DIRS = {".git", "build", "dist", "restored", "__pycache__"}


def inventory(root):
    result = {}
    for path in root.rglob("*"):
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(root)
        if any(part in IGNORED_DIRS for part in relative.parts):
            continue
        name = relative.as_posix()
        if name == MANIFEST:
            continue
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        result[name] = {"size": path.stat().st_size, "sha256": digest.hexdigest()}
    return dict(sorted(result.items()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?", default=Path("."))
    parser.add_argument("--write", action="store_true", help="seal the current export")
    args = parser.parse_args()
    root = args.root.resolve()
    path = root / MANIFEST
    actual = inventory(root)
    if args.write:
        if path.exists():
            parser.error("manifest already exists; remove it explicitly before resealing")
        manifest = {
            "schema": 1,
            "scope": "selected GitHub export, not the formal full snapshot",
            "authority_continuity_id": "1eb14098df9f00f9e583b74ed32ba75914af21087e1ea520bec0f1ef51042571",
            "files": actual,
        }
        path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"SEALED {len(actual)} files: {path}")
        return
    expected = json.loads(path.read_text(encoding="utf-8"))["files"]
    missing = sorted(expected.keys() - actual.keys())
    extra = sorted(actual.keys() - expected.keys())
    changed = sorted(name for name in expected.keys() & actual.keys() if expected[name] != actual[name])
    print(f"Checked {len(actual)} export files; missing={len(missing)}, extra={len(extra)}, changed={len(changed)}")
    for label, names in (("Missing", missing), ("Unexpected", extra), ("Changed", changed)):
        if names:
            print(f"{label}: " + ", ".join(names[:20]))
    if missing or extra or changed:
        raise SystemExit(1)
    print("PASS EXACT GITHUB EXPORT INVENTORY")


if __name__ == "__main__":
    main()
