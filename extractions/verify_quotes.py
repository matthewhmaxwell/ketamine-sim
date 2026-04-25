#!/usr/bin/env python3
"""
Verify every `raw_excerpt` in the JSONL extractions appears verbatim in its source HTML.

Why this exists:
    WebFetch's downstream summarizer silently paraphrases, abbreviates with ellipses,
    and occasionally misattributes quotes. Verbatim extraction must come from raw HTML
    (curl + Grep + Read), and every record must be auditable.

Usage:
    Cache source HTML once (or whenever a source's PMC page changes):
        curl -sL https://pmc.ncbi.nlm.nih.gov/articles/PMC8415567/ -o /tmp/mollaahmetoglu-2021.html
        curl -sL https://pmc.ncbi.nlm.nih.gov/articles/PMC12439531/ -o /tmp/kheirkhah-2025.html

    Then from this directory:
        python3 verify_quotes.py

Add a new source by appending to SOURCES below.

Exits non-zero on any mismatch — safe to run as a pre-commit or CI check.
"""

import html
import json
import re
import sys
from pathlib import Path

SOURCES = [
    ("mollaahmetoglu-2021", "/tmp/mollaahmetoglu-2021.html"),
    ("kheirkhah-2025",      "/tmp/kheirkhah-2025.html"),
]

EXTRACTIONS_DIR = Path(__file__).resolve().parent


def normalize(s: str, *, strip_html: bool = False) -> str:
    """Collapse whitespace, strip HTML, and fold smart-quote/ellipsis variants."""
    if strip_html:
        s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    s = (
        s.replace("\u2018", "'").replace("\u2019", "'")
         .replace("\u201c", '"').replace("\u201d", '"')
         .replace("\u2013", "-").replace("\u2014", "—")
         .replace("\u2026", "...").replace("\xa0", " ")
    )
    return re.sub(r"\s+", " ", s).strip()


def audit(source_id: str, html_path: str) -> tuple[int, list[tuple[str, str]]]:
    jsonl_path = EXTRACTIONS_DIR / f"{source_id}.jsonl"
    if not jsonl_path.exists():
        return 0, [("__file__", f"missing {jsonl_path}")]

    html_file = Path(html_path)
    if not html_file.exists():
        return 0, [("__file__",
                    f"source HTML not cached at {html_path} — run the curl from the docstring")]

    raw = normalize(html_file.read_text(), strip_html=True)
    misses: list[tuple[str, str]] = []
    n = 0
    for line in jsonl_path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        record = json.loads(line)
        n += 1
        excerpt = record.get("raw_excerpt", "")
        if not excerpt:
            continue  # paraphrase_only / cite_only records legitimately have no excerpt
        q = normalize(excerpt)
        if q in raw or (len(q) > 80 and q[20:80] in raw):
            continue
        misses.append((record["record_id"], q[:140]))
    return n, misses


def main() -> int:
    print("=== Verbatim quote audit ===")
    all_clean = True
    grand_total = 0
    for source_id, html_path in SOURCES:
        n, misses = audit(source_id, html_path)
        grand_total += n
        status = "OK" if not misses else f"FAIL ({len(misses)})"
        print(f"  {source_id}: {n} records — {status}")
        for record_id, snippet in misses:
            print(f"    MISS {record_id}: {snippet}")
            all_clean = False
    print(f"\n  TOTAL: {grand_total} records audited")
    if all_clean:
        print("  RESULT: ALL VERBATIM VERIFIED IN SOURCE HTML")
        return 0
    print("  RESULT: mismatches present — fix the JSONL or re-cache the source")
    return 1


if __name__ == "__main__":
    sys.exit(main())
