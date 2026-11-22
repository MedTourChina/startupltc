"""A deliberately small Markdown renderer.

Supports the subset the editorial team actually uses:

    # / ## / ###        headings (H1 is reserved for the page title)
    paragraphs, **bold**, *italic*, `code`, [links](url)
    - unordered lists, 1. ordered lists
    | pipe tables with :---: alignment |
    > blockquotes
    --- hr
    :::answer ... :::   callout blocks (answer, note, warn, checklist)

No dependencies, no HTML pass-through: raw HTML is escaped, which keeps the
output safe for a static build that will be deployed without a WAF.
"""

from __future__ import annotations

import html as _html
import re

_ESCAPE = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}

_SLUG_STRIP = re.compile(r"[^a-z0-9\s-]")

CALLOUTS = {
    "answer": ("callout callout-answer", "The short answer"),
    "note": ("callout callout-note", "Note"),
    "warn": ("callout callout-warn", "Watch out"),
    "checklist": ("callout callout-checklist", "Action checklist"),
    "kill": ("callout callout-kill", "Stop here"),
    "rule": ("callout callout-rule", "Rule of thumb"),
}


def slugify(text: str) -> str:
    text = _html.unescape(re.sub(r"<[^>]+>", "", text)).lower()
    text = _SLUG_STRIP.sub("", text)
    text = re.sub(r"\s+", "-", text.strip())
    return re.sub(r"-{2,}", "-", text).strip("-") or "section"


def _esc(text: str) -> str:
    for k, v in _ESCAPE.items():
        text = text.replace(k, v)
    return text


def inline(text: str) -> str:
    """Render inline markdown on an already line-scoped string."""
    stash: list[str] = []

    def keep(fragment: str) -> str:
        stash.append(fragment)
        return f"\x00{len(stash) - 1}\x00"

    # Code spans first so their contents are never re-interpreted.
    text = re.sub(r"`([^`\n]+)`", lambda m: keep(f"<code>{_esc(m.group(1))}</code>"), text)

    text = _esc(text)

    # Links: [label](href) — href is escaped but never markdown-processed.
    def _link(m: re.Match) -> str:
        label, href = m.group(1), _esc(m.group(2))
        external = href.startswith(("http://", "https://"))
        rel = ' rel="noopener"' if external else ""
        return keep(f'<a href="{href}"{rel}>{label}</a>')

    text = re.sub(r"\[([^\]\n]+)\]\(([^)\s]+)\)", _link, text)

    text = re.sub(r"\*\*([^*\n]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"~~([^~\n]+)~~", r"<del>\1</del>", text)

    for i, fragment in enumerate(stash):
        text = text.replace(f"\x00{i}\x00", fragment)
    return text


def _table(lines: list[str], i: int) -> tuple[str, int]:
    rows = []
    while i < len(lines) and lines[i].strip().startswith("|"):
        rows.append(lines[i].strip())
        i += 1
    if len(rows) < 2:
        return "", i

    def cells(row: str) -> list[str]:
        return [c.strip() for c in row.strip().strip("|").split("|")]

    header = cells(rows[0])
    aligns = []
    for spec in cells(rows[1]):
        spec = spec.strip()
        if spec.startswith(":") and spec.endswith(":"):
            aligns.append("center")
        elif spec.endswith(":"):
            aligns.append("right")
        else:
            aligns.append("left")

    def rs(cell_list: list[str], tag: str) -> str:
        out = []
        for idx, cell in enumerate(cell_list):
            align = aligns[idx] if idx < len(aligns) else "left"
            style = f' style="text-align:{align}"' if align != "left" else ""
            out.append(f"<{tag}{style}>{inline(cell)}</{tag}>")
        return "".join(out)

    body = "".join(f"<tr>{rs(cells(r), 'td')}</tr>" for r in rows[2:])
    return (
        '<div class="table-wrap"><table><thead><tr>'
        + rs(header, "th")
        + f"</tr></thead><tbody>{body}</tbody></table></div>",
        i,
    )


def render(md: str) -> str:
    """Render a markdown document body to HTML."""
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # Callout blocks -------------------------------------------------
        if stripped.startswith(":::"):
            kind = stripped[3:].strip().lower()
            i += 1
            buf: list[str] = []
            while i < n and not lines[i].strip().startswith(":::"):
                buf.append(lines[i])
                i += 1
            i += 1  # closing :::
            css, label = CALLOUTS.get(kind, CALLOUTS["note"])
            inner = render("\n".join(buf))
            head = "" if kind == "checklist" else f'<p class="callout-label">{label}</p>'
            out.append(f'<div class="{css}">{head}{inner}</div>')
            continue

        # Headings -------------------------------------------------------
        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            text = stripped[level:].strip()
            if 1 <= level <= 4 and text:
                # The page title owns <h1>, so map # and ## to h2, then 3 and 4.
                tag = f"h{min(max(level, 2), 4)}"
                hid = slugify(text)
                out.append(f'<{tag} id="{hid}">{inline(text)}</{tag}>')
                i += 1
                continue

        # Horizontal rule ------------------------------------------------
        if stripped in ("---", "***", "___"):
            out.append("<hr>")
            i += 1
            continue

        # Tables ---------------------------------------------------------
        if stripped.startswith("|"):
            table, i = _table(lines, i)
            if table:
                out.append(table)
            continue

        # Blockquote -----------------------------------------------------
        if stripped.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip())
                i += 1
            out.append(f"<blockquote>{render(chr(10).join(buf))}</blockquote>")
            continue

        # Lists ----------------------------------------------------------
        if re.match(r"^[-*+]\s+", stripped) or re.match(r"^\d+[.)]\s+", stripped):
            ordered = bool(re.match(r"^\d+[.)]\s+", stripped))
            items: list[str] = []
            while i < n:
                cur = lines[i]
                cur_s = cur.strip()
                if not cur_s:
                    # A blank line ends the list unless the next line continues it.
                    if i + 1 < n and (
                        re.match(r"^[-*+]\s+", lines[i + 1].strip())
                        or re.match(r"^\d+[.)]\s+", lines[i + 1].strip())
                    ):
                        i += 1
                        continue
                    break
                m = re.match(r"^[-*+]\s+(.*)$", cur_s) or re.match(r"^\d+[.)]\s+(.*)$", cur_s)
                if m:
                    items.append(m.group(1))
                elif cur.startswith(("  ", "\t")) and items:
                    items[-1] += " " + cur_s  # continuation line
                else:
                    break
                i += 1
            tag = "ol" if ordered else "ul"
            body = "".join(f"<li>{inline(x)}</li>" for x in items)
            out.append(f"<{tag}>{body}</{tag}>")
            continue

        # Paragraph ------------------------------------------------------
        buf = []
        while i < n and lines[i].strip() and not re.match(
            r"^(#{1,4}\s|[-*+]\s|\d+[.)]\s|>|\||:::|(---|\*\*\*|___)$)", lines[i].strip()
        ):
            buf.append(lines[i].rstrip())
            i += 1
        if not buf:
            buf = [lines[i].rstrip()]
            i += 1
        text = " ".join(x.strip() for x in buf)
        text = text.replace("  ", "\x01").replace("\x01", "<br>")
        out.append(f"<p>{inline(text)}</p>")

    return "\n".join(out)


def headings(html: str) -> list[tuple[str, str]]:
    """Extract (id, text) pairs from rendered H2s, for the table of contents."""
    found = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', html, flags=re.S)
    return [(hid, re.sub(r"<[^>]+>", "", text)) for hid, text in found]
