#!/usr/bin/env python3
"""Read-only status requests for a locally owned Nokia 5G21 gateway.

Reference endpoints observed in highvolt-dev/tmo-monitor's Nokia controller.
No authentication, configuration changes, or reboot actions are implemented.
"""
import argparse
import ipaddress
import json
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

ENDPOINTS = {
    "device": "/dashboard_device_info_status_web_app.cgi",
    "radio": "/fastmile_radio_status_web_app.cgi",
}

def fetch_status(host, timeout=3.0):
    address = ipaddress.ip_address(host)
    if not address.is_private:
        raise ValueError("Gateway must be at a private IP address")
    result = {"gateway": str(address), "endpoints": {}}
    for name, path in ENDPOINTS.items():
        url = f"http://{address}{path}"
        try:
            with urlopen(url, timeout=timeout) as response:
                payload = json.load(response)
            result["endpoints"][name] = {"ok": True, "data": payload}
        except (URLError, HTTPError, ValueError, OSError) as exc:
            result["endpoints"][name] = {"ok": False, "error": type(exc).__name__}
    return result

def summarize(data):
    device = data["endpoints"].get("device", {})
    radio = data["endpoints"].get("radio", {})
    info = device.get("data", {}).get("device_app_status", [{}])
    info = info[0] if isinstance(info, list) and info else {}
    summary = {
        "gateway": data["gateway"],
        "firmware": info.get("SoftwareVersion"),
        "uptime": info.get("UpTime"),
        "lte_band": None,
        "nr_band": None,
        "endpoint_ok": {key: val.get("ok", False) for key, val in data["endpoints"].items()},
    }
    if radio.get("ok"):
        payload = radio.get("data", {})
        for key, field in (("cell_LTE_stats_cfg", "lte_band"), ("cell_5G_stats_cfg", "nr_band")):
            rows = payload.get(key, [])
            if isinstance(rows, list) and rows and isinstance(rows[0], dict):
                summary[field] = rows[0].get("stat", {}).get("Band")
    return summary

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host", nargs="?", default="192.168.12.1")
    parser.add_argument("--timeout", type=float, default=3.0)
    parser.add_argument("--json", type=Path, dest="output")
    args = parser.parse_args()
    if not 0 < args.timeout <= 10:
        parser.error("--timeout must be between 0 and 10")
    result = summarize(fetch_status(args.host, args.timeout))
    rendered = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)

if __name__ == "__main__":
    main()
