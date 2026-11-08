#!/usr/bin/env python3
"""Mirror the prompt markdown files into the <pre> windows on the page.

The page promises that `copy` gives exactly the text `link` opens, so every edit to a
prompt file in ~/Prompts has to be reflected in index.html as well.

    python3 tools/sync_prompts.py          # sync
    python3 tools/sync_prompts.py --check  # report drift, change nothing

Only the body after the first `---` rule is used, so the repo file's own headings and
front matter stay out of the pasteable window.
"""
from __future__ import annotations

import html
import pathlib
import re
import sys

PAGE = pathlib.Path(__file__).resolve().parents[1] / "index.html"
PROMPTS = pathlib.Path.home() / "Prompts" / "prompts"

# page <pre id> -> markdown file
MAP = (
    ("p-fromzero", "02-biotechcorp-from-zero.md"),
    ("p-generic", "01-autonomous-ad-ctf-agent.md"),
)


def body(path: pathlib.Path) -> str:
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"^---\s*$", text, maxsplit=1, flags=re.M)
    if len(parts) != 2:
        sys.exit(f"error: no '---' separator in {path}")
    return parts[1].lstrip("\n").rstrip() + "\n"


def pattern(pre_id: str) -> re.Pattern[str]:
    return re.compile(r'(<pre id="' + re.escape(pre_id) + r'">)(.*?)(</pre>)', re.S)


def current(src: str, pre_id: str) -> str:
    found = pattern(pre_id).findall(src)
    if len(found) != 1:
        sys.exit(f"error: expected exactly one <pre id=\"{pre_id}\">, found {len(found)}")
    return html.unescape(found[0][1])


def main() -> int:
    check_only = "--check" in sys.argv[1:]
    src = PAGE.read_text(encoding="utf-8")
    drift = 0

    for pre_id, fname in MAP:
        want = body(PROMPTS / fname)
        have = current(src, pre_id)
        same = have.strip("\n") == want.strip("\n")
        print(f"{pre_id:<12} {fname:<34} {'in sync' if same else 'DRIFT'}"
              f"  ({want.count(chr(10))} lines)")
        if same or check_only:
            drift += 0 if same else 1
            continue
        esc = html.escape(want, quote=False)
        src = pattern(pre_id).sub(lambda m: m.group(1) + esc + m.group(3), src, count=1)
        drift += 0

    if check_only:
        return 1 if drift else 0

    PAGE.write_text(src, encoding="utf-8")
    print("written:", PAGE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
