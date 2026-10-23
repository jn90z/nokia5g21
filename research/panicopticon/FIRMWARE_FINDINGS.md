# Firmware findings from five extracted text reports

Source files supplied by repository owner from PanicOpticon's 5G21 research. These are observations of a 2021-era image, **not evidence about the latest T-Mobile firmware**.

## Storage
- 29.13 GiB (31,272,730,624 bytes), 61,079,552 sectors, 512 bytes per sector, GPT.
- 38 partitions. Exact sector boundaries are in `sdb.bin.fdisk.txt`.
- p27/p29 rootfs: SquashFS 4.0, xz, 4,477 inodes, creation timestamp 2021-03-17.
- p28/p30 Wi-Fi firmware: SquashFS 4.0, xz, 42 inodes, timestamp 2020-12-25.
- p32–p38: ext4. `user_data` is flagged as needing journal recovery in the `file` report; never repair the only copy.
- Earlier Parted report warned of a corrupt backup GPT. Keep raw image immutable and verify checksums before recovery work.

## Boot and CPU
- SBL1, QSEE, DEVCFG, RPM, APPSBL, HLOS partition names indicate a Qualcomm-style boot chain.
- `file` identifies SBL1/RPM/APPSBL as ARM 32-bit ELF and QSEE/DEVCFG as ARM64 ELF. This does **not** establish the rootfs userspace ABI.
- Repeated boot and rootfs partitions suggest redundant firmware slots, but boot selection is unverified.

## Rootfs software (from directory listing only)
- `/etc/openwrt_release`, `/etc/openwrt_version`, `/bin/opkg`, `/bin/ubus`, BusyBox: strongly supports an OpenWrt-derived userspace.
- `/etc/init.d/sshd`, `/usr/sbin/sshd`, `/etc/ssh/sshd_config`: OpenSSH server files are present; network reachability and login permissions are unknown.
- `/etc/hb/lighttpd.pcd`, `/usr/sbin/lighttpd`: web service components are present.
- `/etc/config/docker`, `/etc/lxc/`, `lxc-* binaries`, `ContainerMgr`: container tooling is included; actual kernel support and runtime configuration must be verified.
- `/etc/config/openvpn`, `/etc/mosquitto/`, `/etc/config/firewall`, `/etc/config/dhcp`: potential building blocks for repurposing.

## Security and privacy
- Listings contain `/etc/shadow`, `/etc/config/id_rsa`, `/etc/cert/internalkey.pem`, `/etc/cert/webkey.pem`, and other potentially sensitive assets.
- Do not publish those contents, device-specific credentials, or private keys.
- A file listing is not sufficient to conclude that any credentials work on another device.

## Highest priority actual contents to inspect (redacted)
1. `sdb27/etc/openwrt_release`, `openwrt_version`, `buildinfo`, `SWVersion`, `device_info`
2. `sdb27/etc/inittab`, `init.d/sshd`, `init.d/lighttpd`
3. `sdb27/etc/config/docker`, `etc/lxc/lxc.conf`, `etc/config/network` (if present)
4. `sdb27/etc/hb/ContainerMgr.pcd` and `lighttpd.pcd`
5. Architecture of ordinary user-space binaries (`bin/busybox`, `usr/sbin/sshd`), not just boot components

Do not run untrusted firmware binaries on a workstation.
