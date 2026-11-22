"""HTML shell, shared chrome and reusable components.

No forms. No analytics hooks. No third-party requests. The only script on the
site is a small local file that powers the three calculators.
"""

from __future__ import annotations

import json
import re

from . import config as C
from . import svg


def esc(value: object) -> str:
    text = "" if value is None else str(value)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def btn(label: str, href: str, kind: str = "primary", *, size: str = "",
        icon_name: str | None = "arrow", block: bool = False) -> str:
    cls = f"btn btn-{kind}"
    if size:
        cls += f" btn-{size}"
    if block:
        cls += " btn-block"
    glyph = f'<span class="btn-icon">{svg.icon(icon_name, 18)}</span>' if icon_name else ""
    return f'<a class="{cls}" href="{href}">{label}{glyph}</a>'


def crumbs(items: list[tuple[str, str | None]]) -> str:
    parts = []
    for label, href in items:
        if href:
            parts.append(f'<a href="{href}">{esc(label)}</a>')
        else:
            parts.append(f'<span aria-current="page">{esc(label)}</span>')
    return (
        '<nav class="crumbs" aria-label="Breadcrumb"><ol>'
        + "".join(f"<li>{p}</li>" for p in parts)
        + "</ol></nav>"
    )


def site_header(nav_active: str | None = None) -> str:
    links = []
    for label, href in C.NAV:
        current = ' aria-current="page"' if label == nav_active else ""
        links.append(f'<a class="nav-link" href="{href}"{current}>{label}</a>')
    return f"""
<header class="site-header" data-header>
  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="{C.SITE_NAME} — home">
      {svg.BRAND_MARK}
      <span class="brand-text">
        <span class="brand-name">{C.BRAND_LINE_1}</span>
        <span class="brand-sub">{C.BRAND_LINE_2}</span>
      </span>
    </a>
    <nav class="main-nav" id="site-nav" aria-label="Primary">
      {''.join(links)}
    </nav>
    <div class="header-actions">
      <a class="btn btn-primary header-cta" href="/framework/fit/">Start here</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
        <span data-icon-open>{svg.icon('menu', 22)}</span>
        <span data-icon-close hidden>{svg.icon('close', 22)}</span>
      </button>
    </div>
  </div>
</header>"""


def site_footer() -> str:
    cols = []
    for title, links in C.FOOTER_NAV:
        items = "".join(f'<li><a href="{h}">{esc(l)}</a></li>' for l, h in links)
        cols.append(f'<div class="footer-col"><h2 class="footer-head">{title}</h2><ul>{items}</ul></div>')

    return f"""
<footer class="site-footer">
  <div class="footer-sky" aria-hidden="true">{svg.skyline('footer', 1400, 120, '#d98a3a', 0.10, 'skyline skyline-wide')}</div>
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand brand-light" href="/">
          {svg.BRAND_MARK}
          <span class="brand-text">
            <span class="brand-name">{C.BRAND_LINE_1}</span>
            <span class="brand-sub">{C.BRAND_LINE_2}</span>
          </span>
        </a>
        <p class="footer-blurb">{C.SITE_TAGLINE} A free, independent guide that helps foreigners decide whether to start a company in China — and how to check every rule before they commit.</p>
        <p class="pledge">{svg.icon('shield', 18)}<span>{C.PLEDGE}</span></p>
      </div>
      {''.join(cols)}
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 {C.SITE_NAME}. {esc(C.LEGAL_ENTITY)}. Written and maintained by {esc(C.AUTHOR_NAME)}.</p>
      <p class="footer-disclosure">General information only — not legal, tax or investment advice. <a href="/legal/disclaimer/">Read the disclaimer</a>.</p>
    </div>
  </div>
</footer>"""


def page(
    *,
    title: str,
    description: str,
    path: str,
    body: str,
    nav_active: str | None = None,
    body_class: str = "",
    jsonld: list[dict] | None = None,
    og_type: str = "website",
    noindex: bool = False,
    extra_scripts: str = "",
) -> str:
    canonical = C.SITE_URL + path
    full_title = title if title == C.SITE_NAME else f"{title} · {C.SITE_NAME}"
    robots = '<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'

    schemas = ""
    if jsonld:
        for obj in jsonld:
            schemas += (
                '<script type="application/ld+json">'
                + json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
                + "</script>\n"
            )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{C.SITE_NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="en_US">
<meta property="og:image" content="{C.SITE_URL}/img/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#12192b">
<link rel="icon" href="/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/img/favicon.svg">
<link rel="stylesheet" href="/css/site.css?v={C.ASSET_V}">
{schemas}</head>
<body class="{body_class}">
<a class="skip-link" href="#main">Skip to content</a>
{site_header(nav_active)}
<main id="main">
{body}
</main>
{site_footer()}
<script src="/js/main.js?v={C.ASSET_V}" defer></script>
{extra_scripts}
</body>
</html>
"""


# ---------------------------------------------------------------- components

def section(kicker: str, title: str, sub: str = "", inner: str = "", *,
            sid: str = "", cls: str = "", head_cls: str = "") -> str:
    id_attr = f' id="{sid}"' if sid else ""
    sub_html = f'<p class="section-sub">{sub}</p>' if sub else ""
    kick_html = f'<p class="eyebrow">{kicker}</p>' if kicker else ""
    return f"""
<section class="section {cls}"{id_attr}>
  <div class="wrap">
    <div class="section-head {head_cls}">
      {kick_html}
      <h2 class="section-title">{title}</h2>
      {sub_html}
    </div>
    {inner}
  </div>
</section>"""


def answer_box(label: str, html_body: str) -> str:
    return f"""
<aside class="answer">
  <p class="answer-label">{esc(label)}</p>
  <div class="answer-body">{html_body}</div>
</aside>"""


def stat(num: str, label: str, note: str = "") -> str:
    note_html = f'<span class="stat-note">{esc(note)}</span>' if note else ""
    return f'<div class="stat"><span class="stat-num">{esc(num)}</span><span class="stat-label">{esc(label)}</span>{note_html}</div>'


def editorial_note(text: str) -> str:
    return f"""
<aside class="editorial-note">
  {svg.icon('file', 18)}
  <p>{text}</p>
</aside>"""


def city_card(city: dict, index: int = 0) -> str:
    sky = svg.skyline(city["slug"], 340, 104, "currentColor", 1.0, "skyline")
    return f"""
<a class="city-card" href="/cities/{city['slug']}/" style="--i:{index}">
  <div class="city-card-sky">{sky}</div>
  <div class="city-card-body">
    <div class="city-card-top">
      <h3 class="city-card-name">{esc(city['name'])}</h3>
      <span class="city-card-zh">{esc(city['name_zh'])}</span>
    </div>
    <p class="city-card-tag">{esc(city['tagline'])}</p>
    <dl class="city-card-stats">
      <div><dt>Registered address</dt><dd>{esc(city['address_band'])}</dd></div>
      <div><dt>Typical setup</dt><dd>{esc(city['setup_time'])}</dd></div>
    </dl>
  </div>
</a>"""


def guide_card(post: dict) -> str:
    layer = post.get("layer")
    layer_html = ""
    if layer:
        layer_html = f'<span class="tag tag-layer">Layer {layer}</span>'
    return f"""
<a class="guide-card" href="/guides/{post['slug']}/">
  <div class="guide-card-meta">
    <span class="tag tag-cat">{esc(post['category'])}</span>{layer_html}
  </div>
  <h3 class="guide-card-title">{esc(post['title'])}</h3>
  <p class="guide-card-desc">{esc(post['description'])}</p>
  <span class="guide-card-more">Read the guide {svg.icon('arrow', 16)}</span>
</a>"""


def layer_card(layer: dict) -> str:
    return f"""
<a class="layer-card" href="/framework/{layer['slug']}/">
  <span class="layer-card-num">{layer['n']:02d}</span>
  <h3 class="layer-card-title">{esc(layer['question'])}</h3>
  <p class="layer-card-desc">{esc(layer['summary'])}</p>
  <span class="layer-card-more">{esc(layer['name'])} {svg.icon('arrow', 15)}</span>
</a>"""


def tool_strip(layer_n: int, title: str = "What to do next") -> str:
    """The step that follows a framework chapter: a tool, or the checklist."""
    items = C.LAYER_TOOLS.get(layer_n, [])
    if not items:
        return ""
    cards = "".join(
        f"""
    <a class="step-card" href="{href}">
      <span class="step-card-title">{esc(label)}<span class="step-card-arrow">{svg.icon('arrow', 15)}</span></span>
      <span class="step-card-reason">{esc(reason)}</span>
    </a>"""
        for label, href, reason in items
    )
    return f"""
<aside class="tool-strip">
  <p class="tool-strip-label">{esc(title)}</p>
  <div class="tool-strip-grid">{cards}</div>
  <p class="tool-strip-note">The words on the paperwork are rarely translated in the room. <a href="/glossary/">The glossary gives each one its characters, pinyin and plain meaning →</a></p>
</aside>"""


def next_step(layer_n: int) -> str:
    """Closing block for a guide: where the reader goes after reading."""
    items = C.LAYER_TOOLS.get(layer_n, [])
    links = "".join(
        f'<li><a href="{href}">{esc(label)}</a> <span>{esc(reason)}</span></li>'
        for label, href, reason in items
    )
    sheet = (
        '<li><a href="/framework/decision-sheet/">Open the decision sheet</a> '
        "<span>Twenty-five checks and fifteen stop conditions, in order.</span></li>"
        if layer_n != 4 and layer_n != 5
        else ""
    )
    gloss = (
        '<li><a href="/glossary/">Look up a term</a> '
        "<span>The words on the licence, with characters and pinyin.</span></li>"
    )
    return f"""
<aside class="next-step">
  <p class="next-step-label">Your next step</p>
  <ul class="next-step-list">{links}{sheet}{gloss}</ul>
</aside>"""


def city_strip(cities: list[dict], limit: int = 4, title: str = "Check this in the city you will register in") -> str:
    """Compact link row to the largest markets, for pages that describe national rules."""
    picked = sorted(cities, key=lambda c: c.get("rank", 99))[:limit]
    chips = "".join(
        f'<a class="city-chip" href="/cities/{esc(c["slug"])}/"><span class="city-chip-en">{esc(c["name"])}</span>'
        f'<span class="city-chip-zh">{esc(c["name_zh"])}</span></a>'
        for c in picked
    )
    return f"""
<aside class="city-strip">
  <p class="city-strip-label">{esc(title)}</p>
  <div class="city-strip-row">{chips}</div>
  <p class="city-strip-note">Registration practice, address supply and work-permit processing are municipal, and they change without much notice. <a href="/cities/">All {len(cities)} cities →</a></p>
</aside>"""


def term_chips(terms: list[dict], label: str = "Terms this page uses") -> str:
    """Glossary terms that a given page actually uses, resolved through the reverse index."""
    if not terms:
        return ""
    chips = "".join(
        f'<li><a href="/glossary/#{esc(t["id"])}"><span class="term-chip-zh">{esc(t["term"])}</span>'
        f'<span class="term-chip-en">{esc(t["english"])}</span></a></li>'
        for t in terms
    )
    return f"""
<aside class="term-strip">
  <p class="term-strip-label">{esc(label)}</p>
  <ul class="term-strip-list">{chips}</ul>
</aside>"""


def term_chips_by_ids(ids: list[str], label: str = "Terms this page uses") -> str:
    """Curated term strip by glossary id, for pages that are not tied to one guide."""
    index = {t["id"]: t for t in getattr(C, "GLOSSARY_TERMS", [])}
    return term_chips([index[i] for i in ids if i in index], label)


def flow(steps: list[tuple[str, str]]) -> str:
    """Horizontal decision flow: label, caption."""
    parts = []
    for i, (label, caption) in enumerate(steps):
        parts.append(
            f'<li class="flow-step"><span class="flow-num">{i + 1}</span>'
            f'<span class="flow-label">{esc(label)}</span>'
            f'<span class="flow-caption">{esc(caption)}</span></li>'
        )
    arrows = '<span class="flow-arrow" aria-hidden="true">→</span>'
    return f'<ol class="flow">' + arrows.join(parts) + "</ol>"


def kill_box(title: str, html_body: str) -> str:
    return f"""
<aside class="kill-box">
  <p class="kill-title">{svg.icon('close', 15)} {esc(title)}</p>
  <div class="kill-body">{html_body}</div>
</aside>"""


def byline(post: dict) -> str:
    return f"""
<div class="byline">
  <div class="byline-item">
    <span class="byline-label">Written by</span>
    <span class="byline-value">{esc(post.get('author', C.AUTHOR_NAME))}</span>
  </div>
  <div class="byline-item">
    <span class="byline-label">Reviewed by</span>
    <span class="byline-value">{esc(post.get('reviewer', C.REVIEWER_NAME))}</span>
  </div>
  <div class="byline-item">
    <span class="byline-label">Last reviewed</span>
    <span class="byline-value">{esc(post.get('updated_human', C.LAST_UPDATED))}</span>
  </div>
  <div class="byline-item">
    <span class="byline-label">Reading time</span>
    <span class="byline-value">{esc(post.get('read', '8'))} min</span>
  </div>
</div>"""


def toc(items: list[tuple[str, str]]) -> str:
    if len(items) < 3:
        return ""
    links = "".join(f'<li><a href="#{hid}">{esc(text)}</a></li>' for hid, text in items)
    return f"""
<nav class="toc" aria-label="On this page">
  <p class="toc-title">On this page</p>
  <ol>{links}</ol>
</nav>"""


def related(posts: list[dict], title: str = "Related guides") -> str:
    if not posts:
        return ""
    cards = "".join(guide_card(p) for p in posts)
    return f"""
<section class="section section-tight">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Keep reading</p>
      <h2 class="section-title">{esc(title)}</h2>
    </div>
    <div class="grid grid-3">{cards}</div>
  </div>
</section>"""


def rail(active: str | None = None) -> str:
    """Sticky layer navigation for framework chapters."""
    items = []
    for l in C.LAYERS:
        cls = "rail-item is-active" if l["slug"] == active else "rail-item"
        items.append(
            f'<a class="{cls}" href="/framework/{l["slug"]}/">'
            f'<span class="rail-num">{l["n"]:02d}</span><span class="rail-name">{esc(l["name"])}</span></a>'
        )
    return f'<nav class="rail" aria-label="The five layers">{"".join(items)}</nav>'


def pager(prev: dict | None, nxt: dict | None) -> str:
    parts = []
    if prev:
        parts.append(
            f'<a class="pager-item pager-prev" href="/framework/{prev["slug"]}/">'
            f'<span class="pager-label">Layer {prev["n"]:02d} — previous</span>'
            f'<span class="pager-title">{esc(prev["name"])}</span></a>'
        )
    if nxt:
        parts.append(
            f'<a class="pager-item pager-next" href="/framework/{nxt["slug"]}/">'
            f'<span class="pager-label">Layer {nxt["n"]:02d} — next</span>'
            f'<span class="pager-title">{esc(nxt["name"])}</span></a>'
        )
    if not parts:
        return ""
    return f'<nav class="pager" aria-label="Chapter navigation">{"".join(parts)}</nav>'


def strip_tags(html_text: str) -> str:
    return re.sub(r"<[^>]+>", "", html_text).strip()


def fmt_price(cny: int | float) -> str:
    try:
        value = float(cny)
    except (TypeError, ValueError):
        return "—"
    if value >= 1_000_000:
        return f"¥{value / 1_000_000:.2f}".rstrip("0").rstrip(".") + "M"
    if value >= 1_000:
        return f"¥{value / 1_000:.0f}k"
    return f"¥{value:.0f}"
