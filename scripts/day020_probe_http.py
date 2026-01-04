"""Day020 - Minimal HTTP probe (standard library).

Usage (PowerShell):
  python scripts/day020_probe_http.py <host> <port>

Outputs:
  - Prints status line and key headers (Server/Date/Content-Type)

Security notes:
  - Only probe hosts you own or have explicit authorization to test.
"""

from __future__ import annotations

import http.client
import sys


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Usage: python scripts/day020_probe_http.py <host> <port>")
        return 2

    host = argv[1]
    try:
        port = int(argv[2])
    except ValueError:
        print("ERROR: port must be an integer")
        return 2

    try:
        conn = http.client.HTTPConnection(host, port, timeout=5)
        conn.request("HEAD", "/", headers={"User-Agent": "day020-probe"})
        resp = conn.getresponse()

        print(f"HTTP/{resp.version/10:.1f} {resp.status} {resp.reason}")
        for k in ["Server", "Date", "Content-Type", "Content-Length"]:
            v = resp.getheader(k)
            if v:
                print(f"{k}: {v}")

        conn.close()
        return 0
    except Exception as exc:
        print("ERROR:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
