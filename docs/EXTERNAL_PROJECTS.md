# External research projects to evaluate

These are candidates for code review, **not validated API specifications** for this exact firmware.

- HINT Control: https://github.com/zacharee/HINTControl — T-Mobile gateway management client; investigate its Nokia-specific implementation and licensing before reuse.
- tmo-monitor: https://github.com/highvolt-dev/tmo-monitor — gateway monitoring; examine NOK5G21 detection, request paths, authentication, response handling.
- Project Black, Hacking the Nokia Fastmile: https://projectblack.io/blog/hacking-the-nokia-fastmile/ — hardware/firmware research on a different FastMile variant; do not transfer UART pinouts, credentials, or firmware assumptions to the 5G21.
- FastMileScraper: https://github.com/zayigo/FastMileScraper — different FastMile model; conceptual reference only.

## Evaluation checklist
- Confirm the repository is accessible and inspect the actual implementation.
- Record supported model and firmware versions, endpoint paths, auth requirements, error behavior and licenses.
- Separate read-only telemetry endpoints from configuration-changing operations.
- Never hard-code passwords or commit raw API responses containing serials, IMEIs, MACs or tokens.
- Prefer a read-only local adapter and mock fixtures before integration with a physical gateway.
