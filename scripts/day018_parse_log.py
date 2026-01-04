"""Day018 - Parse demo log and fetch a public JSON API (standard library only).

Inputs:
  - scripts/day017-demo.log (created in Day017)
Outputs:
  - scripts/day018_log.json
  - prints repo info from GitHub API

Notes:
  - This is learning/demo code. It avoids external dependencies.
  - Be mindful of rate limits on the GitHub API.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path


LOG_PATH = Path("scripts/day017-demo.log")
OUT_JSON = Path("scripts/day018_log.json")
REPO_API = "https://api.github.com/repos/Tigercoll/network-security-notes"


LINE_RE = re.compile(r"^(?P<ts>\S+\s+\S+)\s+(?P<level>INFO|WARN|ERROR)\s+(?P<msg>.*)$")


def parse_log(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = LINE_RE.match(line.strip())
        if not m:
            continue
        rows.append(
            {
                "Time": m.group("ts"),
                "Level": m.group("level"),
                "Msg": m.group("msg"),
            }
        )
    return rows


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            # GitHub API requires a User-Agent.
            "User-Agent": "network-security-notes-day018",
            "Accept": "application/vnd.github+json",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = resp.read().decode("utf-8")
        return json.loads(data)


def main() -> int:
    try:
        if not LOG_PATH.exists():
            print(f"ERROR: log file not found: {LOG_PATH}")
            print("Hint: run Day017 Task 1 to generate scripts/day017-demo.log")
            return 2

        rows = parse_log(LOG_PATH)
        OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        OUT_JSON.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote {OUT_JSON} ({len(rows)} rows)")

        repo = fetch_json(REPO_API)
        out = {
            "full_name": repo.get("full_name"),
            "stargazers_count": repo.get("stargazers_count"),
            "updated_at": repo.get("updated_at"),
        }
        print("GitHub repo:")
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print("ERROR:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
