"""Expand the selected older native traces into an isolated inspection folder."""

import argparse
from pathlib import Path, PurePosixPath
from zipfile import ZipFile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--to", required=True, type=Path, help="new or empty output directory")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    archive = root / "support/historical_native_evidence.zip"
    destination = args.to.resolve()
    if destination.exists() and any(destination.iterdir()):
        parser.error("output directory must be empty")
    with ZipFile(archive) as z:
        names = z.namelist()
        for name in names:
            path = PurePosixPath(name)
            if path.is_absolute() or ".." in path.parts or path.parts[0] != "evidence":
                parser.error(f"unsafe archive entry: {name}")
        destination.mkdir(parents=True, exist_ok=True)
        z.extractall(destination)
        assert z.testzip() is None, "damaged evidence archive"
    print(f"Restored {len(names)} evidence files to {destination / 'evidence'}")


if __name__ == "__main__":
    main()
