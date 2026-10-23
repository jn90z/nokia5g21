# First Power-On Checklist

1. Photograph the gateway label and note the hardware model/revision. **Do not publish IMEI, serial, SIM or Wi-Fi credentials.**
2. Isolate the gateway from the main home network; connect a test computer by Ethernet.
3. Record displayed firmware version and software/hardware revision, if accessible.
4. Run `ipconfig /all` (Windows) or `ip route` (Linux) to determine the gateway IP.
5. Run `python tools/gateway_probe.py <gateway-ip> --json reports/gateway.json`.
6. Save screenshots of the management interface, redacting secrets.
7. Record behavior with and without a SIM; do not factory reset yet.
8. If opening the enclosure later, photograph both sides of boards before touching anything. Identify UART voltage before connecting an adapter; never connect adapter VCC blindly.
9. Do not attempt firmware flashing until original images and a recovery procedure have been verified.

## Record
- Model / board revision:
- Firmware version:
- Gateway LAN IP:
- Management interface:
- Observed open ports:
- Notes:
