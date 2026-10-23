#!/usr/bin/env python3
"""Single-host read-only TCP and HTTP HEAD reconnaissance."""
import argparse
import http.client
import ipaddress
import json
import socket
from pathlib import Path

DEFAULT_PORTS = (22, 23, 80, 443, 8080, 8443)

def probe(host, ports=DEFAULT_PORTS, timeout=1.5):
    address = ipaddress.ip_address(host)
    if not address.is_private:
        raise ValueError("Only private IP addresses are accepted")
    results = []
    for port in ports:
        item = {"port": port, "tcp_open": False}
        try:
            with socket.create_connection((str(address), port), timeout=timeout):
                item["tcp_open"] = True
        except (OSError, TimeoutError):
            pass
        if item["tcp_open"] and port in (80, 443, 8080, 8443):
            conn_cls = http.client.HTTPSConnection if port in (443, 8443) else http.client.HTTPConnection
            conn = conn_cls(str(address), port, timeout=timeout)
            try:
                conn.request("HEAD", "/")
                response = conn.getresponse()
                item["http_status"] = response.status
                item["server"] = response.getheader("Server")
                response.read()
            except (OSError, TimeoutError, http.client.HTTPException) as exc:
                item["http_error"] = type(exc).__name__
            finally:
                conn.close()
        results.append(item)
    return {"host": str(address), "ports": results}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host", help="Single private IPv4 or IPv6 address")
    parser.add_argument("--json", type=Path, dest="output")
    parser.add_argument("--timeout", type=float, default=1.5)
    args = parser.parse_args()
    if not 0 < args.timeout <= 10:
        parser.error("--timeout must be between 0 and 10 seconds")
    data = probe(args.host, timeout=args.timeout)
    rendered = json.dumps(data, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)

if __name__ == "__main__":
    main()
