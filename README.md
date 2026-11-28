# startupltc — Lifetourchina Startup

A free, independent guide for foreigners starting and running a company in mainland
China. It is the startup companion to [realtyltc](https://github.com/MedTourChina/realtyltc)
(property) and [china-expat-finance](https://github.com/MedTourChina/china-expat-finance)
(investing), and it is published at **https://startup.lifetourchina.com**.

The site answers one question in five ordered layers — Fit, Access, Structure, Money,
Continuity — and gives a path, not a verdict. Every number carries the date it was
checked, and every rule names the authority behind it.

## What is here

- `sitegen/` — a zero-dependency Python static generator: Markdown subset renderer
  (`md.py`), layout and components (`layout.py`), page builders (`pages.py`,
  `pages_extra.py`), brand SVG (`svg.py`), site constants (`config.py`).
- `content/` — all editorial content: 45 guides, 5 framework chapters, 12 sectors,
  10 cities, 71 glossary entries, 49 FAQ answers, a 25-check decision sheet and
  4 content pages. Markdown with YAML-ish front matter; data as JSON.
- `static/` — hand-written CSS and JavaScript. No frameworks, no build step, no fonts
  or scripts loaded from third parties.
- `dist/` — the built site, committed on purpose (see Deployment).
- `check.py` — link, anchor and metadata checker for the built output.

## Build

Requires Python 3.10+. Nothing else.

```sh
python build.py          # rebuild dist/
python build.py --og     # also regenerate dist/img/og.png (needs Pillow)
python build.py --serve  # rebuild and preview on http://127.0.0.1:8080
python check.py          # verify internal links, anchors and page metadata
```

Always run `build.py` and `check.py` before committing.

## Deployment

Cloudflare Pages, Git integration, build command **empty**, output directory `dist`.
`dist/` is committed because the build is reproducible from a Python-free CI runner
and the output is small. `_headers` and `_redirects` are copied into `dist/` by the
build.

## Editorial rules

- Independent and non-commercial: no advertising, no commissions, no accounts, no
  forms, no analytics. Nothing is collected about readers.
- Every price is a range in RMB, dated, with the city or national scope named.
- Every rule names the law, ministry or registry that issues it.
- Guides say when *not* to register a company, and when to stop and talk to a
  Chinese lawyer instead.
- Pages are reviewed; the review date is on the page.
- Corrections: `notes@lifetourchina.com`.

## Licence

Text and original illustrations are © Lifetourchina Startup. Quoting short excerpts
with a link is welcome; wholesale republication is not.
