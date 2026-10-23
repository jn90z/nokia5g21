# Nokia FastMile 5G21 Research Toolkit

Research and repurposing toolkit for the T-Mobile Nokia FastMile 5G21 cylindrical gateway.

## Goals
- Identify firmware formats, embedded filesystems, and partition candidates.
- Collect non-invasive network diagnostics from a personally owned gateway.
- Document hardware, serial access, backup and recovery.
- Evaluate custom applications and eventually alternative firmware, if supported.

**Status:** pre-hardware reconnaissance. No firmware compatibility, shell access, or flashing path is yet verified.

## Quick start

Python 3.11+ is recommended; no third-party Python dependencies are required.

```sh
python tools/firmware_scan.py path/to/firmware.bin --json reports/firmware.json
python tools/gateway_probe.py 192.168.12.1 --json reports/gateway.json
python -m unittest discover -s tests -v
```

Gateway probing performs TCP connection tests and HTTP HEAD requests to explicitly selected ports on one host only. Run only against equipment you own or administer. The default address is an example, not a confirmed gateway address.

## Layout
- `tools/`: offline firmware scanning and read-only gateway discovery
- `docs/`: hardware inventory, safety, weekend checklist, research references
- `tests/`: synthetic regression tests
- `reports/`: local output, ignored by Git
- `firmware/`: local firmware artifacts, ignored by Git

## Research boundaries
No flash writes, credentials, private keys, modem identifiers, or extracted proprietary firmware are committed. Back up device-specific calibration and configuration data before any modifications. Do not assume techniques for other FastMile models apply to 5G21.

## Milestones
1. [x] Repository skeleton and analysis tools
2. [ ] Record hardware and firmware revisions
3. [ ] Analyze legally obtained firmware image
4. [ ] Verify serial/bootloader access and recovery
5. [ ] Prototype custom services
6. [ ] Assess feasibility of alternative Linux/OpenWrt images
