# PanicOpticon source inventory (verified from uploaded ZIP reports)

The inventory was generated locally by the repository's Windows PowerShell script and supplied by the user. **The archive contents themselves have not yet been extracted or inspected.**

| ZIP | Bytes | SHA-256 |
|---|---:|---|
| Nokia 5G21-20261023T165513Z-1-001.zip | 1187306368 | 7ae3f35ba1fbb8e7a77de68c6477aaa21df112274d8339bdafd3468afbcfdcc2 |
| Nokia 5G21-20261023T165513Z-1-002.zip | 2137864558 | 9ef9362c9cabea8d8ae7b829bf8d4676a15bec707866cc4524f10de0bdda57df |

- 63 ZIP entries total.
- 38 individually compressed partition images: `sdb1.bin.bz2` through `sdb38.bin.bz2`.
- Complete compressed eMMC image: `emmc/dds/sdb.bin.bz2` (1,384,504,638 bytes).
- Rootfs partition archives: `sdb27.bin.bz2` and `sdb29.bin.bz2` (44,136,833 bytes each).
- HLOS partition archives: `sdb25.bin.bz2` and `sdb26.bin.bz2` (4,208,437 bytes each).
- Extracted SquashFS: `emmc/fs/squashfs/squashfs.7z` (73,417,206 bytes).
- Mounted ext4 archive: `emmc/fs/ext4/mounted_fs.7za` (221,504,091 bytes).
- Textual evidence: `sdb.bin.fdisk.txt`, `sdb.bin.blkid.txt`, `bins.file.txt`, `squashfs.lslr.txt`, `sdb.fs.lslr.txt`, `mounted_fs.txt`.
- Six PCB scans under `scans/`: radio-a-1, radio-b-1, router-a-1, router-a-2, router-b-1, router-b-2.
- `passwd.txt` and `shadow.txt` appear in filesystem directories. Treat as sensitive, do not commit.
- Source URLs: https://drive.google.com/drive/folders/1mPNO27pbXViPi8xBKaLvgWP-HPcnVPke and https://drive.google.com/file/d/1LRHiwnkAssWaHxouxJJL8OnSmD0-uQA4/view

## Priority for next inspection
1. `sdb.bin.fdisk.txt`, `sdb.bin.blkid.txt`, `bins.file.txt`
2. `squashfs.lslr.txt` and `mounted_fs.txt`
3. `squashfs.7z` and selected extracted rootfs files
4. Board scans
5. Raw partition images only where needed

**Caution:** A ZIP listing establishes filenames and compressed sizes, not the firmware version, executable contents, or integrity of the inner bzip2 images.
