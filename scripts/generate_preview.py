from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from test_publish import convert_markdown_to_html


def main() -> None:
    root = ROOT
    md = root / "daily" / "Day001.md"
    html = convert_markdown_to_html(str(md))

    out = root / "preview.html"
    out.write_text(
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>"
        "<title>WeChat Preview</title></head><body>"
        + html
        + "</body></html>",
        encoding="utf-8",
    )
    print(f"preview generated: {out} (len={len(html)})")


if __name__ == "__main__":
    main()
