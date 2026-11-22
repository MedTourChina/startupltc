#!/usr/bin/env python3
"""Static checks on the built site: internal links, anchors, and basics.

    python check.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sitegen import config as C

DIST = Path(__file__).resolve().parent / "dist"
SITE_HOST = C.SITE_URL.split("//", 1)[-1]

HREF = re.compile(r'(?:href|src)="(/[^"#]*)"')
ANCHOR = re.compile(r'href="(/[^"#?]*)#([^"]+)"')
ID = re.compile(r'\sid="([^"]+)"')


def target_file(url_path: str) -> Path:
    url_path = url_path.split("?", 1)[0]  # ignore cache-busting query strings
    rel = url_path.lstrip("/")
    if not rel:
        return DIST / "index.html"
    if url_path.endswith("/"):
        rel += "index.html"
    return DIST / rel


def main() -> int:
    pages = sorted(DIST.rglob("*.html"))
    if not pages:
        print("no pages built")
        return 1

    ids_by_file: dict[Path, set[str]] = {}
    for page in pages:
        ids_by_file[page] = set(ID.findall(page.read_text(encoding="utf-8")))

    missing: list[tuple[Path, str]] = []
    bad_anchors: list[tuple[Path, str]] = []
    external: set[str] = set()

    for page in pages:
        text = page.read_text(encoding="utf-8")
        for href in set(HREF.findall(text)):
            target = target_file(href)
            if not target.exists():
                missing.append((page, href))
        for path_part, frag in set(ANCHOR.findall(text)):
            # resolve the anchor against the page the link actually points at,
            # so cross-page fragments (/glossary/#deed-tax) are checked properly
            target = target_file(path_part)
            ids = ids_by_file.get(target)
            if ids is None:
                continue  # missing page already reported by the HREF pass
            if frag not in ids:
                bad_anchors.append((page, f"{path_part}#{frag}"))

    for page in pages:
        for m in re.finditer(r'(?:href|src)="(https?://[^"]+)"', page.read_text(encoding="utf-8")):
            if SITE_HOST not in m.group(1):
                external.add(m.group(1))

    print(f"pages checked: {len(pages)}")
    print(f"external urls: {len(external)}")
    for url in sorted(external):
        print(f"  ext {url}")

    if missing:
        print(f"\nMISSING TARGETS ({len(missing)}):")
        for page, href in missing[:40]:
            print(f"  {page.relative_to(DIST)}  ->  {href}")
    else:
        print("\nall internal links resolve")

    if bad_anchors:
        print(f"\nBROKEN ANCHORS ({len(bad_anchors)}):")
        for page, frag in bad_anchors[:40]:
            print(f"  {page.relative_to(DIST)}  ->  {frag}")
    else:
        print("all anchors resolve (same-page and cross-page)")

    # every page should carry a title, description and canonical
    problems = 0
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for needle in ('<title>', 'name="description"', 'rel="canonical"', 'id="main"'):
            if needle not in text:
                print(f"  !! {page.relative_to(DIST)} missing {needle}")
                problems += 1
    print(f"metadata problems: {problems}")

    return 1 if (missing or bad_anchors or problems) else 0


if __name__ == "__main__":
    sys.exit(main())
