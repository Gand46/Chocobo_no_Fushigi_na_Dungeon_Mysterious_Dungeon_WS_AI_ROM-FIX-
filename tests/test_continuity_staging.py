import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import continuity


class ContinuityStagingTests(unittest.TestCase):
    def test_stage_hashes_source_and_rejects_late_source_change(self):
        with tempfile.TemporaryDirectory() as d:
            source, stage = Path(d) / "source", Path(d) / "stage"
            source.mkdir()
            stage.mkdir()
            (source / "a.txt").write_bytes(b"original")
            entries = {"a.txt": {"kind": "file",
                                  "sha256": hashlib.sha256(b"original").hexdigest()}}
            continuity.copy_sources(source, stage, entries)
            self.assertEqual((stage / "a.txt").read_bytes(), b"original")
            (source / "a.txt").write_bytes(b"changed")
            with self.assertRaises(continuity.GuardError):
                continuity.copy_sources(source, Path(d) / "second", entries)

    def test_copy_fallback_keeps_verified_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            source, stage = Path(d) / "source", Path(d) / "stage"
            source.mkdir()
            stage.mkdir()
            (source / "a.txt").write_bytes(b"evidence")
            entries = {"a.txt": {"kind": "file",
                                  "sha256": hashlib.sha256(b"evidence").hexdigest()}}
            with patch.object(continuity.os, "link", side_effect=OSError("unsupported")):
                continuity.copy_sources(source, stage, entries)
            self.assertEqual((stage / "a.txt").read_bytes(), b"evidence")
            self.assertNotEqual((source / "a.txt").stat().st_ino,
                                (stage / "a.txt").stat().st_ino)


if __name__ == "__main__":
    unittest.main()
