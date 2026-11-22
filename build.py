#!/usr/bin/env python3
"""Build the Lifetourchina Startup static site into dist/.

Zero dependencies. Run: python build.py [--serve] [--og]
"""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent
CONTENT = BASE / "content"
STATIC = BASE / "static"
DIST = BASE / "dist"

from sitegen import config as C
from sitegen import md
from sitegen import pages as PG
from sitegen import pages_extra as PX
from sitegen import svg

GUIDE_CATEGORIES = ["Deciding", "Access", "Structure", "Money", "People", "Compliance", "Exit"]


# --------------------------------------------------------------- frontmatter

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse the tiny YAML dialect used in content/: scalar keys, plus JSON
    arrays/objects (crumbs). No nesting, no multiline scalars."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    head = text[3:end].strip("\n")
    body = text[end + 4:].lstrip("\n")
    meta: dict = {}
    for line in head.splitlines():
        line = line.rstrip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, raw = line.partition(":")
        key = key.strip()
        raw = raw.strip()
        if not raw:
            meta[key] = ""
            continue
        if raw[0] in "[{":
            try:
                meta[key] = json.loads(raw)
                continue
            except json.JSONDecodeError:
                pass
        if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
            raw = raw[1:-1]
        if raw.isdigit():
            meta[key] = int(raw)
        else:
            meta[key] = raw
    return meta, body


def human_date(iso: str) -> str:
    try:
        d = date.fromisoformat(str(iso))
    except (ValueError, TypeError):
        return str(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


def reading_time(body: str) -> int:
    """Rough minutes at ~200 words per minute; ignores table pipes and markup."""
    words = [w for w in body.replace("|", " ").split() if any(c.isalnum() for c in w)]
    return max(3, round(len(words) / 200))


# -------------------------------------------------------------------- loaders

def load_json(name: str):
    with (CONTENT / name).open(encoding="utf-8") as fh:
        return json.load(fh)


def load_guides() -> list[dict]:
    posts = []
    for path in sorted((CONTENT / "guides").glob("*.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        post = {
            "slug": path.stem,
            "title": meta.get("title", path.stem),
            "description": meta.get("description", ""),
            "category": meta.get("category", "Deciding"),
            "layer": int(meta.get("layer", 1)),
            "answer": meta.get("answer", ""),
            "updated": str(meta.get("updated", "2026-11-01")),
            "read": reading_time(body),
            "author": meta.get("author", C.AUTHOR_NAME),
            "reviewer": meta.get("reviewer", C.REVIEWER_NAME),
            "body": body,
        }
        post["updated_human"] = human_date(post["updated"])
        posts.append(post)
    posts.sort(key=lambda p: (p["layer"], p["title"]))
    return posts


def load_framework() -> list[dict]:
    chapters = []
    for layer in C.LAYERS:
        path = CONTENT / "framework" / f"{layer['n']}-{layer['slug']}.md"
        if not path.exists():
            raise SystemExit(f"missing framework chapter: {path}")
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        chapters.append({
            "n": layer["n"],
            "slug": layer["slug"],
            "name": layer["name"],
            "question": meta.get("question", layer["question"]),
            "summary": meta.get("summary", layer["summary"]),
            "title": meta.get("title", layer["question"]),
            "description": meta.get("description", layer["summary"]),
            "answer": meta.get("answer", ""),
            "read": reading_time(body),
            "updated": str(meta.get("updated", "2026-11-19")),
            "body": body,
        })
    return chapters


def load_pages() -> list[dict]:
    out = []
    for path in sorted((CONTENT / "pages").glob("*.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        crumbs = meta.get("crumbs")
        if not isinstance(crumbs, list):
            crumbs = [["Home", "/"], [meta.get("title", path.stem), None]]
        out.append({
            "slug": path.stem,
            "title": meta.get("title", path.stem),
            "description": meta.get("description", ""),
            "kicker": meta.get("kicker", ""),
            "path": meta.get("path", f"/{path.stem}/"),
            "crumbs": [tuple(c) for c in crumbs],
            "body": body,
        })
    return out


# ------------------------------------------------------------------- helpers

def asset_version() -> str:
    h = hashlib.sha1()
    for rel in ("css/site.css", "js/main.js", "js/tools.js", "js/decision.js"):
        p = STATIC / rel
        if p.exists():
            h.update(p.read_bytes())
    return h.hexdigest()[:8]


def url_to_file(url: str) -> Path:
    url = url.split("?")[0].split("#")[0]
    if url == "/" or url == "":
        return DIST / "index.html"
    rel = url.lstrip("/")
    if url.endswith("/"):
        return DIST / rel / "index.html"
    if "." in rel.rsplit("/", 1)[-1]:
        return DIST / rel
    return DIST / rel / "index.html"


def write(rel: str, text: str) -> None:
    path = DIST / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


# --------------------------------------------------------------- og / favicon

def make_og_image() -> bool:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return False

    W, H = 1200, 630
    ink = (18, 25, 43)
    paper = (247, 243, 234)
    amber = (217, 154, 43)
    muted = (168, 160, 145)

    img = Image.new("RGB", (W, H), ink)
    d = ImageDraw.Draw(img)

    def font(size: int, serif: bool = False):
        names = (
            ["C:/Windows/Fonts/georgiab.ttf", "C:/Windows/Fonts/timesbd.ttf"]
            if serif else
            ["C:/Windows/Fonts/seguisb.ttf", "C:/Windows/Fonts/arialbd.ttf"]
        )
        for name in names:
            try:
                return ImageFont.truetype(name, size)
            except OSError:
                continue
        return ImageFont.load_default()

    # five layer bars, the visual motif of the framework
    for i in range(5):
        x = 96 + i * 46
        h = 24 + i * 14
        d.rectangle([x, 470 - h, x + 30, 470], fill=amber if i == 4 else (60, 72, 96))

    d.text((96, 84), "LIFETOURCHINA", font=font(28, serif=True), fill=amber)
    d.text((96, 126), "STARTUP", font=font(34, serif=True), fill=paper)
    d.text((96, 220), "Starting a business in China,", font=font(58), fill=paper)
    d.text((96, 292), "in the right order.", font=font(58), fill=paper)
    d.text((96, 396), "Five decisions before the first yuan of capital.", font=font(30), fill=muted)
    d.text((96, 540), "startup.lifetourchina.com", font=font(26), fill=muted)

    out = STATIC / "img" / "og.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    return True


# --------------------------------------------------------------------- build

def build() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    C.ASSET_V = asset_version()

    cities = sorted(load_json("cities.json"), key=lambda c: int(c.get("rank", 99)))
    sectors = load_json("sectors.json")
    glossary_entries = load_json("glossary.json")
    faq_items = load_json("faq.json")
    sheet = load_json("decision-sheet.json")

    guides = load_guides()
    chapters = load_framework()
    content_pages = load_pages()

    # glossary terms used by each guide (reverse of `see`)
    for post in guides:
        post["terms"] = [g for g in glossary_entries if post["slug"] in g.get("see", [])][:6]

    by_slug = {g["slug"]: g for g in guides}

    written: list[tuple[str, str]] = []  # (url path, priority)

    # ---- home
    write("index.html", PG.home(cities, guides, sectors))
    written.append(("/", "1.0"))

    # ---- framework
    write("framework/index.html", PX.framework_index(sheet["stops"]))
    written.append(("/framework/", "0.9"))
    for i, ch in enumerate(chapters):
        prev = chapters[i - 1] if i > 0 else None
        nxt = chapters[i + 1] if i + 1 < len(chapters) else None
        layer_guides = [g for g in guides if g["layer"] == ch["n"]][:3]
        write(f"framework/{ch['slug']}/index.html",
              PX.framework_chapter(ch, prev, nxt, layer_guides, cities))
        written.append((f"/framework/{ch['slug']}/", "0.9"))

    write("framework/decision-sheet/index.html", PX.decision_sheet(sheet))
    written.append(("/framework/decision-sheet/", "0.7"))

    # ---- sectors / cities
    write("sectors/index.html", PG.sectors_index(sectors))
    written.append(("/sectors/", "0.9"))
    write("cities/index.html", PG.cities_index(cities))
    written.append(("/cities/", "0.9"))
    city_guides = [by_slug[s] for s in
                   ("registered-address-in-china", "opening-a-corporate-bank-account",
                    "do-you-need-a-china-entity") if s in by_slug]
    for city in cities:
        write(f"cities/{city['slug']}/index.html",
              PG.city_page(city, cities, city_guides or guides[:3], sectors))
        written.append((f"/cities/{city['slug']}/", "0.8"))

    # ---- guides
    write("guides/index.html", PG.guides_index(guides))
    written.append(("/guides/", "0.9"))
    for post in guides:
        related = [by_slug[s] for s in post.get("related_slugs", []) if s in by_slug]
        if not related:
            related = [g for g in guides
                       if g["slug"] != post["slug"] and g["category"] == post["category"]][:3]
        write(f"guides/{post['slug']}/index.html", PG.guide_page(post, related, cities))
        written.append((f"/guides/{post['slug']}/", "0.8"))

    # ---- tools
    write("tools/index.html", PX.tools_index())
    written.append(("/tools/", "0.8"))
    write("tools/structure/index.html", PX.structure_tool(cities))
    written.append(("/tools/structure/", "0.7"))
    write("tools/setup-cost/index.html", PX.setup_cost_tool(cities))
    written.append(("/tools/setup-cost/", "0.7"))
    write("tools/repatriation/index.html", PX.repatriation_tool(cities))
    written.append(("/tools/repatriation/", "0.7"))

    # ---- reference
    write("faq/index.html", PX.faq_page(faq_items))
    written.append(("/faq/", "0.7"))
    write("glossary/index.html", PX.glossary(glossary_entries, guides))
    written.append(("/glossary/", "0.7"))

    for page in content_pages:
        write(url_to_file(page["path"]).relative_to(DIST).as_posix(),
              PX.content_page(page, nav_active="About" if page["path"] == "/about/" else None))
        written.append((page["path"], "0.5"))

    # ---- 404
    write("404.html", PX.not_found())

    # ---- static
    shutil.copytree(STATIC / "css", DIST / "css")
    shutil.copytree(STATIC / "js", DIST / "js")
    (DIST / "img").mkdir(exist_ok=True)
    (DIST / "img" / "favicon.svg").write_text(svg.FAVICON, encoding="utf-8")
    og = DIST / "img" / "og.png"
    if (STATIC / "img" / "og.png").exists():
        shutil.copy2(STATIC / "img" / "og.png", og)

    # ---- sitemap
    today = "2026-11-22"
    entries = "".join(
        f"  <url><loc>{C.SITE_URL}{path}</loc><lastmod>{today}</lastmod>"
        f"<priority>{prio}</priority></url>\n"
        for path, prio in written
    )
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          f"{entries}</urlset>\n")

    write("robots.txt",
          "User-agent: *\nAllow: /\nDisallow: /404.html\n\n"
          f"Sitemap: {C.SITE_URL}/sitemap.xml\n")

    csp = (
        "default-src 'self'; "
        "img-src 'self' data:; "
        "style-src 'self' 'unsafe-inline'; "
        "script-src 'self'; "
        "font-src 'self'; "
        "connect-src 'none'; "
        "form-action 'none'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "object-src 'none'"
    )
    write("_headers",
          "/*\n"
          f"  Content-Security-Policy: {csp}\n"
          "  X-Content-Type-Options: nosniff\n"
          "  Referrer-Policy: strict-origin-when-cross-origin\n"
          "  Permissions-Policy: geolocation=(), microphone=(), camera=()\n"
          "\n/css/*\n  Cache-Control: public, max-age=31536000, immutable\n"
          "\n/js/*\n  Cache-Control: public, max-age=31536000, immutable\n"
          "\n/img/*\n  Cache-Control: public, max-age=31536000, immutable\n")

    write("_redirects",
          "https://www.startup.lifetourchina.com/*  https://startup.lifetourchina.com/:splat  301!\n")

    # trailing-slash normalisation is handled by Cloudflare Pages' default
    # pretty-URL behaviour for directory indexes.

    print(f"built {len(written)} pages into {DIST}")
    if not og.exists():
        print("  (og.png missing — run with --og on a machine with Pillow and Windows fonts)")


def main() -> None:
    args = set(sys.argv[1:])
    if "--og" in args:
        made = make_og_image()
        print("og.png written" if made else "og.png skipped (Pillow or fonts unavailable)")
    build()
    if "--serve" in args:
        from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
        import functools
        handler = functools.partial(SimpleHTTPRequestHandler, directory=str(DIST))
        print("serving http://127.0.0.1:8080/")
        ThreadingHTTPServer(("127.0.0.1", 8080), handler).serve_forever()


if __name__ == "__main__":
    main()
