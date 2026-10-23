# Nokia 5G21 eMMC partition analysis

Source: user-supplied `sdb.bin.parted.txt`, attributed to PanicOpticon's 5G21 research. This is a transcription of the supplied GNU Parted output, not an independent inspection of the 31.3 GB image.

## Confirmed by supplied text
- GNU Parted 3.4; 512-byte logical/physical sectors; GPT; disk size reported as 31.3 GB.
- 38 numbered partitions.
- ext4 is explicitly shown for partitions 32–38.
- Duplicate-named components include QSEE, DEVCFG, RPM, CDT, APPSBL, HLOS, rootfs and WIFIFW.
- Warning: backup GPT corrupt, primary appears OK.
- Warning: an additional 8192 blocks appeared unused; operator chose Ignore.

## Architecture hypotheses (not yet verified)
- SBL1/QSEE/RPM/APPSBL/HLOS naming is consistent with a Qualcomm-oriented boot chain.
- Repeated boot and root filesystem partitions suggest an A/B or redundant update design.
- `container` and `user_data` are large ext4 volumes, but contents and role remain unknown.
- `ART` and `Factory_MIM` may contain factory-specific data; never overwrite them without a verified backup.

## Selected partition inventory
| # | Name | Reported size | Filesystem |
|---|---|---|---|
| 1 | 0:SBL1 | 524 kB | unknown |
| 18 | 0:APPSBL | 655 kB | unknown |
| 19 | 0:APPSBL_1 | 655 kB | unknown |
| 25 | 0:HLOS | 6291 kB | unknown |
| 26 | 0:HLOS_1 | 6291 kB | unknown |
| 27 | rootfs | 134 MB | unknown |
| 29 | rootfs_1 | 134 MB | unknown |
| 32 | configs | 21.0 MB | ext4 |
| 33 | SWR | 537 MB | ext4 |
| 34 | log | 134 MB | ext4 |
| 35 | rootfs_data | 268 MB | ext4 |
| 36 | rootfs_data1 | 268 MB | ext4 |
| 37 | container | 17.2 GB | ext4 |
| 38 | user_data | 12.6 GB | ext4 |

## Next analysis
Obtain raw image and inspect GPT in read-only mode. Use exact sector offsets from a machine-readable partition table rather than Parted's rounded kB/MB display. Verify primary and backup GPT checksums. Do not run `parted fix` or repair the source image in place.
