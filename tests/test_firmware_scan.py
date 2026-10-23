import tempfile
import unittest
from pathlib import Path
from tools.firmware_scan import scan

class FirmwareScanTests(unittest.TestCase):
    def test_signatures_across_chunk_boundary(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "synthetic.bin"
            path.write_bytes(b"X" * (1024 * 1024 - 2) + b"hsqs" + b"Y" * 5)
            result = scan(path)
            matches = [x for x in result["signature_candidates"] if x["type"] == "squashfs_le"]
            self.assertEqual([x["offset"] for x in matches], [1024 * 1024 - 2])
            self.assertEqual(result["size"], 1024 * 1024 + 7)

if __name__ == "__main__":
    unittest.main()
