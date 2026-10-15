import hashlib
import json
import random
import struct
import unittest
from pathlib import Path
from build import replace_checked
from tools.bps_codec import create, apply, crc, encode_number
ROOT=Path(__file__).resolve().parents[1]

class PatchTests(unittest.TestCase):
    def test_deterministic_roundtrip(self):
        rng=random.Random(13102026)
        for size in [0,1,16,128,16384]:
            source=bytes(rng.randrange(256) for _ in range(size))
            target=bytearray(source)
            for _ in range(min(size,90)):
                target[rng.randrange(size)]=rng.randrange(256)
            patch=create(source,bytes(target),b'test')
            self.assertEqual(apply(source,patch),bytes(target))
            self.assertEqual(create(source,bytes(target),b'test'),patch)
    def test_resizing(self):
        for source,target in [(b'abc',b'abcde'),(b'abcdef',b'a'),(b'',b'a')]:
            self.assertEqual(apply(source,create(source,target)),target)
    def test_wrong_base(self):
        with self.assertRaises(ValueError):apply(b'ABD',create(b'ABC',b'XYZ'))
    def test_tampered_patch(self):
        p=bytearray(create(b'ABC',b'XYZ'));p[7]^=1
        with self.assertRaises(ValueError):apply(b'ABC',bytes(p))
    def test_truncated_patch(self):
        with self.assertRaises(ValueError):apply(b'ABC',create(b'ABC',b'XYZ')[:-1])
    def test_sourcecopy_targetcopy(self):
        # Copy BC from source index 1, then overlap-copy BC twice from output.
        src=b'ABCD';dst=b'BCBCBC'
        stream=encode_number(((2-1)<<2)|2)+encode_number(2)
        stream+=encode_number(((4-1)<<2)|3)+encode_number(0)
        p=bytearray(b'BPS1'+encode_number(len(src))+encode_number(len(dst))+encode_number(0)+stream)
        p+=struct.pack('<II',crc(src),crc(dst));p+=struct.pack('<I',crc(p))
        self.assertEqual(apply(src,bytes(p)),dst)
    def test_overlapping_edit_rejected(self):
        edits=[{'offset':'0x0','before':'00','after':'01'},{'offset':'0x0','before':'01','after':'02'}]
        with self.assertRaises(ValueError):replace_checked(bytearray(b'\0'),edits)
    def test_preimage_rejected(self):
        with self.assertRaises(ValueError):replace_checked(bytearray(b'a'),[{'offset':'0x0','before':'62','after':'63'}])
    def test_ten_terminated_resources(self):
        rows=json.loads((ROOT/'localization/corrected_resources.json').read_text())
        self.assertEqual(len(rows),10)
        for r in rows:self.assertEqual(r['hf1_words_le'][-1],'FFFF')
    def test_caves_near_pointer_preserves_bank(self):
        rows=json.loads((ROOT/'localization/corrected_resources.json').read_text())
        moved=[r for r in rows if r['original_resource']!=r['hf1_resource']]
        self.assertEqual(len(moved),3)
        for r in moved:
            self.assertEqual(int(r['table'],0)>>16,int(r['hf1_resource'],0)>>16)
    def test_manifest_scope(self):
        m=json.loads((ROOT/'manifest.json').read_text())
        self.assertEqual(m['qa21_corrected_references'],len(json.loads((ROOT/'qa21/translations.json').read_text())))
        self.assertFalse(m['global_linguistic_approved'])
        self.assertFalse(m['global_layout_approved'])
        self.assertFalse(m['all_pdf_incidents_fixed'])

if __name__=='__main__':unittest.main()
