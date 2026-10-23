# Next milestone: read-only 5G21 management client

## Current state
We have an archived firmware partition inventory and OpenWrt-derived filesystem evidence. We have **not** established the owner's current firmware version, local management API contract, login method, container runtime access, or safe flashing path.

## Work plan
1. Read and compare HINT Control and tmo-monitor Nokia implementations.
2. Record observed GET/HEAD API paths and response schemas in a model/version compatibility table, without copying credentials.
3. Build a standard-library Python read-only client with configurable base URL, strict private-IP restriction, request timeout, and JSON output.
4. Add synthetic tests for response parsing and errors; keep tests offline.
5. Prototype a localhost-only dashboard displaying device status and cellular metrics from redacted fixtures.
6. When gateway is available, collect current version and run `python tools/gateway_probe.py 192.168.12.1 --json reports/gateway.json` (substitute actual gateway IP).
7. Do not enable writes, reboot actions, or persistent firmware modifications without explicit validation and backups.

## Immediate data to collect
- Model, hardware revision, firmware version from UI
- Actual gateway IP and accessible management ports
- Redacted read-only responses where available
- Whether T-Mobile connectivity is required for any status fields
