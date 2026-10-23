# PanicOpticon's Nokia 5G21 research

Original author: u/PanicOpticon (Reddit). This directory records external research **with attribution**. It does not claim ownership or redistribute original dumps.

## Primary source
- Reddit post, "Trashcan Hacking" (2022-10-30): https://www.reddit.com/r/tmobileisp/comments/yhpzfj/
- Public Drive folder supplied for this research: https://drive.google.com/drive/folders/1mPNO27pbXViPi8xBKaLvgWP-HPcnVPke
- Public Drive file supplied for this research: https://drive.google.com/file/d/1LRHiwnkAssWaHxouxJJL8OnSmD0-uQA4/view

## Researcher's reported findings
- Physical eMMC removal from a non-booting Nokia 5G21, followed by a chip-reader dump.
- ext4 partitions and SquashFS volumes extracted from the image.
- Partition naming and layout can be investigated using the author's `parted` output.
- Optical board scans were also published.
- Firmware version of the donor device was not confirmed in the original post.

These are reported findings from the Reddit post, **not independently verified by this repository**.

## Import status
The linked Google Drive assets have **not yet been downloaded, enumerated, hash-verified or reviewed** by this project. Do not mistake this reference directory for a copy of the original data.

## Suggested workflow
1. Download source assets into local `firmware/panicopticon/` (ignored by Git).
2. Generate a SHA-256 inventory using `tools/hash_inventory.py`.
3. Inspect partition tables and filesystem signatures offline.
4. Redact private information and check redistribution permission before publishing any derived data.
5. Commit only documented findings, safe metadata and scripts unless distribution rights are established.
