# Analysis plan

## Stage 1 — source preservation
- Inventory each downloaded asset with SHA-256 and byte size.
- Preserve original filenames and record download date.
- Separate raw flash images, extracted filesystems, board photos and logs.
- Avoid checking binaries into Git history.

## Stage 2 — flash layout
- Review the original `parted` output, if available.
- Identify partition names, sector size, start/end sectors, partition types.
- Cross-check against the raw image, if provided.
- Document uncertainty: eMMC boot areas may not appear in a user-area partition dump.

## Stage 3 — filesystem inspection
- Identify ext4, SquashFS and other filesystem images.
- Record architecture, kernel version, init system, mount table, and service names.
- Review bootloader configuration, device trees and update mechanisms.
- Avoid publishing embedded credentials, private keys, IMEI, serial numbers or subscriber data.

## Stage 4 — hardware correlation
- Correlate board photos with identifiable chip markings.
- Locate candidate UART and test pads, but verify voltages electrically.
- Compare observed live firmware to donor image before extrapolating.

## Stage 5 — custom software
- Begin with reversible user-space experimentation.
- Evaluate persistent storage, service startup and package compatibility.
- Treat bootloader changes and flashing as separate, high-risk milestones.
