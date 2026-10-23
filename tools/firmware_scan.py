#!/usr/bin/env python3
"""Non-destructive firmware signature inventory; not a partition parser."""
import argparse
import hashlib
import json
from pathlib import Path

SIGNATURES = {
    "squashfs_le": b"hsqs",
    "squashfs_be": b"sqsh",
    "gzip": b"\x1f\x8b\x08",
    "zip": b"PK\x03\x04",
    "elf": b"\x7fELF",
    "uimage": b"\x27\x05\x19\x56",
    "ubi": b"UBI#",
    "dtb": b"\xd0\x0d\xfe\xed",
}
CHUNK = 1024 * 1024

def scan(path):
    path = Path(path)
    digest = hashlib.sha256()
    hits = []
    overlap = max(map(len, SIGNATURES.values())) - 1
    tail = b""
    total = 0
    with path.open("rb") as fh:
        while chunk := fh.read(CHUNK):
            digest.update(chunk)
            window = tail + chunk
            base = total - len(tail)
            for name, sig in SIGNATURES.items():
                pos = window.find(sig)
                while pos >= 0:
                    offset = base + pos
                    if offset >= 0 and offset + len(sig) > total:
                        hits.append({"type": name, "offset": offset, "hex": hex(offset)})
                    pos = window.find(sig, pos + 1)
            total += len(chunk)
            tail = window[-overlap:] if overlap else b""
    return {"file": path.name, "size": total, "sha256": digest.hexdigest(),
            "signature_candidates": sorted(hits, key=lambda h: h["offset"]),
            "warning": "Magic bytes may occur by chance; offsets are not verified partitions."}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--json", type=Path, dest="output")
    args = parser.parse_args()
    result = scan(args.image)
    rendered = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)

if __name__ == "__main__":
    main()
