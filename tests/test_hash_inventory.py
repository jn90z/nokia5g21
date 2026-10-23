import hashlib
import tempfile
import unittest
from pathlib import Path
from tools.hash_inventory import inventory

class InventoryTests(unittest.TestCase):
    def test_hashes_local_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "sample.bin").write_bytes(b"abc")
            items = inventory(tmp)["files"]
            self.assertEqual(len(items), 1)
            self.assertEqual(items[0]["sha256"], hashlib.sha256(b"abc").hexdigest())
            self.assertEqual(items[0]["size_bytes"], 3)

if __name__ == "__main__":
    unittest.main()
