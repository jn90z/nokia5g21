#!/usr/bin/env python3
"""Generate a SHA-256 inventory for locally downloaded research files."""
import argparse
import hashlib
import json
from pathlib import Path

def inventory(root):
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError("Input must be a directory")
    entries = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        entries.append({"path": path.relative_to(root).as_posix(),
                        "size_bytes": path.stat().st_size,
                        "sha256": digest.hexdigest()})
    return {"source_directory": root.name, "files": entries}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--json", type=Path, dest="output")
    args = parser.parse_args()
    result = inventory(args.directory)
    rendered = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)

if __name__ == "__main__":
    main()
