# Nokia 5G21 firmware research findings

## Evidence scope
PanicOpticon's archived 2021 eMMC filesystem, not a live measurement of the owner's gateway. Findings below are based on supplied partition reports and the archived filesystem listing. Firmware build identifiers were reported from direct archive inspection earlier in the research conversation; independently recheck extracted files before treating those strings as verified for a live device.

## Platform
- GPT eMMC image: 31,272,730,624 bytes, 38 partitions, 512-byte logical sectors.
- Boot partition labels include SBL1, QSEE, DEVCFG, RPM, APPSBL and HLOS; consistent with a Qualcomm boot chain.
- Rootfs partitions 27 and 29: SquashFS 4.0 xz, 4,477 inodes each, timestamps March 17, 2021.
- Wi-Fi firmware partitions 28 and 30: SquashFS 4.0 xz, 42 inodes each.
- Writable ext4 partitions 32–38 include configs, SWR, log, rootfs_data, rootfs_data1, container, user_data.
- OpenWrt-derived userspace evidenced by openwrt_release, opkg, ubus, BusyBox, procd-style service scripts and OpenWrt config directories.
- Previously extracted metadata identifies OpenWrt Chaos Calmer 15.05.1, target ipq/ipq807x_64, device family HB5GGW, build HB5GGW_R200303B73T0101E0178, timestamp 20210317041344. Verify against actual files and the running device.
- The listing includes LXC, Docker-related config, ContainerMgr, lighttpd, OpenSSH, and Nokia cellular management components. Presence does not establish current runtime access or permission.

## Interpretation and cautions
- Dual rootfs/HLOS/Wi-Fi firmware images suggest redundant slots, but slot selection and rollback remain unknown.
- A Qualcomm-style partition layout and ipq807x target do not prove the exact SoC variant or modem chipset.
- The archived rootfs is not a current firmware compatibility guarantee.
- Do not publish keys, password hashes, calibration, identifiers, or proprietary firmware.
- Do not write to eMMC or attempt firmware flashing before recovery is validated.

## Next checks
1. Read the owner's current firmware version from the official management UI.
2. Run read-only single-host gateway_probe.py and retain its local JSON.
3. Confirm exact device hardware revision and network addresses.
4. Inspect local API behavior without making state-changing requests.
5. Assess whether a separate dashboard can use documented or observed read-only APIs.
