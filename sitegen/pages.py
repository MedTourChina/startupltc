"""Page builders: home, sectors, city index, city detail, guide index, guide detail."""

from __future__ import annotations

from . import config as C
from . import layout as L
from . import md, svg

esc = L.esc

ORG_LD = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": C.SITE_NAME,
    "url": C.SITE_URL,
    "description": C.SITE_DESCRIPTION,
}

WEBSITE_LD = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": C.SITE_NAME,
    "url": C.SITE_URL,
    "description": C.SITE_DESCRIPTION,
    "inLanguage": "en",
}


def breadcrumb_ld(items: list[tuple[str, str | None]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": (C.SITE_URL + href) if href else C.SITE_URL + "/",
            }
            for i, (name, href) in enumerate(items)
        ],
    }


def article_ld(post: dict, path: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": post["title"],
        "description": post["description"],
        "dateModified": post["updated"],
        "datePublished": post["updated"],
        "inLanguage": "en",
        "author": {"@type": "Person", "name": post.get("author", C.AUTHOR_NAME)},
        "reviewedBy": {"@type": "Person", "name": post.get("reviewer", C.REVIEWER_NAME)},
        "publisher": {"@type": "Organization", "name": C.SITE_NAME, "url": C.SITE_URL},
        "mainEntityOfPage": C.SITE_URL + path,
    }


def access_class(access: str) -> str:
    a = access.lower()
    if a.startswith("closed"):
        return "is-closed"
    if a.startswith("restricted"):
        return "is-restricted"
    if "licence" in a:
        return "is-licence"
    return "is-open"


def sector_card(s: dict) -> str:
    return f"""
<a class="sector-card" href="/sectors/#{esc(s['slug'])}">
  <span class="sector-icon">{svg.icon(s.get('icon', 'briefcase'), 20)}</span>
  <span class="sector-name">{esc(s['name'])}</span>
  <span class="sector-zh">{esc(s['name_zh'])}</span>
  <span class="tag tag-access {access_class(s['access'])}">{esc(s['access'])}</span>
  <span class="sector-gate">{esc(s['gate'])}</span>
  <span class="sector-meta">{svg.icon('arrow', 14)} How to enter</span>
</a>"""


# --------------------------------------------------------------------- home

def home(cities: list[dict], guides: list[dict], sectors: list[dict]) -> str:
    layer_rows = "".join(
        f"""<li>
          <span class="hero-layer-num">{l['n']:02d}</span>
          <span class="hero-layer-q">{esc(l['question'])}</span>
          <span class="hero-layer-name">{esc(l['name'])}</span>
        </li>"""
        for l in C.LAYERS
    )

    hero = f"""
<section class="hero">
  <div class="wrap hero-inner">
    <div class="hero-copy">
      <p class="hero-kicker"><span class="dot"></span> Free · independent · no advertising</p>
      <h1 class="hero-title">Starting a business in China,<br>in the right <em>order</em>.</h1>
      <p class="hero-sub">Five decisions come before the first yuan of capital: whether you need an entity at all, whether you are allowed to do this, which vehicle, how money moves, and who keeps it legal. Most foreign founders start at the fourth.</p>
      <div class="hero-actions">
        {L.btn('Start with layer 1', '/framework/fit/', 'light', size='lg', icon_name='arrow')}
        {L.btn('See the whole framework', '/framework/', 'outline-light', size='lg', icon_name=None)}
      </div>
      <div class="hero-stats">
        {L.stat('5', 'layers, in order', 'each one can veto')}
        {L.stat('12', 'sectors mapped', 'list, licence, gate')}
        {L.stat('10', 'cities compared', 'same dimensions')}
      </div>
    </div>
    <div class="hero-visual">
      <div class="hero-panel">
        <p class="hero-panel-kicker">The five decisions</p>
        <ol class="hero-layers">{layer_rows}</ol>
        <p class="hero-panel-note">Read top to bottom. A "no" at any layer ends the plan — that is the point of doing them in order.</p>
      </div>
    </div>
  </div>
</section>"""

    why = f"""
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Why this exists</p>
      <h2 class="section-title">The information is not missing. The order is.</h2>
      <p class="section-sub">English-language advice on starting a company in China is abundant and almost entirely about the mechanics of registration. The decisions that determine whether registration is a good idea are made earlier, and nobody sequences them.</p>
    </div>
    <div class="grid grid-3">
      <div class="pillar">
        <p class="pillar-num">01 — Access first</p>
        <h3 class="pillar-title">The list decides, then the licence</h3>
        <p>A sector can be open to 100% foreign ownership and still be impossible to enter because the licence is not issued to new companies, or because the premises cannot meet the standard. The negative list is the first gate, not the only one.</p>
      </div>
      <div class="pillar">
        <p class="pillar-num">02 — Structure second</p>
        <h3 class="pillar-title">A vehicle is not a strategy</h3>
        <p>A WFOE, a joint venture and a representative office do different things. Founders choose by tax rate, then discover the vehicle cannot hold the licence they need. Control and permission come before optimisation.</p>
      </div>
      <div class="pillar">
        <p class="pillar-num">03 — Verification</p>
        <h3 class="pillar-title">Paths, not conclusions</h3>
        <p>We do not tell you a city is easy. We tell you which counter to stand at, which documents to ask for, and what a written answer looks like — because registration practice is municipal and changes without much notice.</p>
      </div>
    </div>
  </div>
</section>"""

    flow_block = f"""
<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">The sequence</p>
      <h2 class="section-title">Five decisions, in this order</h2>
      <p class="section-sub">Each layer has a stop condition. Hit one and the plan ends — which is cheaper than finding out after the capital is paid in.</p>
    </div>
    {L.flow([(l['name'], l['question']) for l in C.LAYERS])}
    <p class="mt-2">{L.btn('Open the framework', '/framework/', 'primary')}</p>
  </div>
</section>"""

    layers = "".join(L.layer_card(l) for l in C.LAYERS)
    layer_block = f"""
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Read in order</p>
      <h2 class="section-title">The five layers</h2>
    </div>
    <div class="grid grid-3 layer-grid">{layers}</div>
  </div>
</section>"""

    sector_cards = "".join(sector_card(s) for s in sectors)
    sectors_block = f"""
<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Layer 2, applied</p>
      <h2 class="section-title">Twelve sectors, one question each</h2>
      <p class="section-sub">Is foreign ownership allowed, and what licence gates it? The answer differs more than the negative list suggests.</p>
    </div>
    <div class="grid grid-3">{sector_cards}</div>
    <p class="mt-2">{L.btn('Compare all twelve sectors', '/sectors/', 'ghost')}</p>
  </div>
</section>"""

    city_cards = "".join(L.city_card(c, i) for i, c in enumerate(cities))
    cities_block = f"""
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Where to register</p>
      <h2 class="section-title">Ten cities, the same four questions</h2>
      <p class="section-sub">Address supply, banking practice, work-permit processing and sector mix. Compare on the same dimensions, so "I liked it there" is not the deciding argument.</p>
    </div>
    <div class="grid grid-4">{city_cards}</div>
    <p class="mt-2">{L.btn('Compare all cities', '/cities/', 'ghost')}</p>
  </div>
</section>"""

    tools = f"""
<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Work it out yourself</p>
      <h2 class="section-title">Three tools that run in your browser</h2>
      <p class="section-sub">No accounts, no uploads, nothing leaves the page. They exist to help you reach a decision, not to collect a lead.</p>
    </div>
    <div class="grid grid-3">
      <a class="tool-card" href="/tools/structure/">
        <span class="tool-icon">{svg.icon('building', 22)}</span>
        <h3 class="tool-card-title">Which vehicle?</h3>
        <p class="tool-card-desc">Six questions on activity, ownership and staff. Get an indicative vehicle — or an argument for waiting.</p>
        <span class="tool-card-meta">Run the chooser</span>
      </a>
      <a class="tool-card" href="/tools/setup-cost/">
        <span class="tool-icon">{svg.icon('receipt', 22)}</span>
        <h3 class="tool-card-title">What does year one cost?</h3>
        <p class="tool-card-desc">Registration, address, accounting, payroll and the buffer most founders forget.</p>
        <span class="tool-card-meta">Open the calculator</span>
      </a>
      <a class="tool-card" href="/tools/repatriation/">
        <span class="tool-icon">{svg.icon('bank', 22)}</span>
        <h3 class="tool-card-title">What arrives offshore?</h3>
        <p class="tool-card-desc">Corporate income tax, withholding tax and treaty rates, as one number on a dividend.</p>
        <span class="tool-card-meta">Model a dividend</span>
      </a>
    </div>
  </div>
</section>"""

    latest = "".join(L.guide_card(g) for g in guides[:3])
    guides_block = f"""
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">The fact base</p>
      <h2 class="section-title">Dated, sourced, and willing to say no</h2>
      <p class="section-sub">Every guide shows when it was last checked and who checked it. If a rule has moved, the page says so at the top rather than quietly ageing.</p>
    </div>
    <div class="grid grid-3">{latest}</div>
    <p class="mt-2">{L.btn('All guides', '/guides/', 'ghost')}</p>
  </div>
</section>"""

    pledge = f"""
<section class="section section-alt">
  <div class="wrap">
    <div class="pledge-band">
      <div>
        <p class="eyebrow">What this is not</p>
        <h2 class="section-title">No agents. No referrals. No fees.</h2>
      </div>
      <ul class="pledge-list">
        <li>{svg.icon('check', 16)}<span>No advertising, no sponsored content, no affiliate links</span></li>
        <li>{svg.icon('check', 16)}<span>No commissions from registration agents, lawyers, banks or landlords</span></li>
        <li>{svg.icon('check', 16)}<span>No forms, no newsletters, no accounts, no tracking</span></li>
        <li>{svg.icon('check', 16)}<span>No named recommendations — only how to vet people yourself</span></li>
      </ul>
    </div>
    <p class="pledge-close">The only thing we ask is that you use the framework before you pay anyone to register anything. <a href="/about/">Why this exists</a>.</p>
  </div>
</section>"""

    body = hero + why + flow_block + layer_block + sectors_block + cities_block + tools + guides_block + pledge
    return L.page(
        title="Starting a business in China as a foreigner",
        description=C.SITE_DESCRIPTION,
        path="/",
        body=body,
        nav_active=None,
        body_class="page-home",
        jsonld=[ORG_LD, WEBSITE_LD],
    )


# ------------------------------------------------------------------ sectors

def sector_more(s: dict) -> str:
    slug = s.get("guide")
    if not slug:
        return ""
    return (
        f'<p class="sector-detail-more">'
        f'{L.btn("Read the sector guide", f"/guides/{slug}/", "ghost")}</p>'
    )


def sectors_index(sectors: list[dict]) -> str:
    cards = "".join(sector_card(s) for s in sectors)
    blocks = []
    for s in sectors:
        blocks.append(f"""
<article class="sector-detail" id="{esc(s['slug'])}">
  <div class="sector-detail-head">
    <span class="sector-detail-icon">{svg.icon(s.get('icon', 'briefcase'), 24)}</span>
    <div>
      <p class="eyebrow">{esc(s['name_zh'])}</p>
      <h2 class="section-title">{esc(s['name'])}</h2>
      <p class="sector-detail-tagline">{esc(s['tagline'])}</p>
    </div>
    <span class="tag tag-access {access_class(s['access'])}">{esc(s['access'])}</span>
  </div>
  <div class="sector-facts">
    <div><dt>Foreign equity</dt><dd>{esc(s['equity'])}</dd></div>
    <div><dt>The gate</dt><dd>{esc(s['gate'])}</dd></div>
    <div><dt>Typical timeline</dt><dd>{esc(s['timeline'])}</dd></div>
  </div>
  <p class="sector-detail-gate">{esc(s['gate_detail'])}</p>
  <p class="sector-detail-reality">{esc(s['reality'])}</p>
  <p class="sector-detail-watch"><strong>Watch for:</strong> {esc(s['watch'])}</p>
  {sector_more(s)}
</article>""")

    body = f"""
<section class="section">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('Sectors', None)])}
    <div class="section-head mt-2">
      <p class="eyebrow">Layer 2 · Access</p>
      <h1 class="section-title display">Twelve sectors, and what gates each one</h1>
      <p class="section-sub">The negative list decides whether you may own the business. The licence decides whether you may operate it. Both are checked here, sector by sector, because a founder who reads only the list usually stops one gate too early.</p>
    </div>
    <div class="grid grid-3">{cards}</div>
    {L.answer_box('How to read this page', '<p>The access tag is about ownership: open, open with a licence, restricted, or closed. The gate line is about permission: the licence, the premises or the partner that a new company cannot get around. If either fails, the sector fails for you — regardless of how good the market looks.</p>')}
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Sector by sector</p>
      <h2 class="section-title">The detail behind each tag</h2>
      <p class="section-sub">Equity limits, the licence that matters, how long it takes, and what foreign founders usually discover too late.</p>
    </div>
    <div class="sector-detail-list">{''.join(blocks)}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="quote-block">
      <p class="quote-text">A sector is not a market. It is a licence, a premises standard, and a regulator who has seen your business model before.</p>
      <p class="quote-cite">The three things layer 2 asks you to check</p>
    </div>
    <p class="mt-2">{L.btn('Read the negative list guide', '/guides/negative-list/', 'primary')} {L.btn('How to verify what a consultant tells you', '/verify/', 'ghost', icon_name=None)}</p>
  </div>
</section>"""

    return L.page(
        title="Sectors",
        description="Twelve sectors for foreign founders in China, compared on negative-list access, foreign equity limits, the licence that gates entry, and typical timelines.",
        path="/sectors/",
        body=body,
        nav_active="Sectors",
        jsonld=[breadcrumb_ld([("Home", "/"), ("Sectors", "/sectors/")])],
    )


# -------------------------------------------------------------------- cities

def cities_index(cities: list[dict]) -> str:
    cards = "".join(L.city_card(c, i) for i, c in enumerate(cities))
    rows = "".join(
        f"""<tr>
      <td><a href="/cities/{c['slug']}/"><strong>{L.esc(c['name'])}</strong></a><br><span class="muted">{L.esc(c['name_zh'])}</span></td>
      <td>{L.esc(c['region'])}</td>
      <td class="nowrap">{L.esc(c['address_band'])}</td>
      <td class="nowrap">{L.esc(c['setup_time'])}</td>
      <td>{L.esc(c['best_for'])}</td>
    </tr>"""
        for c in cities
    )

    body = f"""
<section class="section">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('Cities', None)])}
    <div class="section-head mt-2">
      <p class="eyebrow">Where to register</p>
      <h1 class="section-title display">Ten cities, one comparison</h1>
      <p class="section-sub">These are the cities where foreign founders actually register. Each is assessed on the same dimensions — address supply, banking practice, permit processing and sector mix — so that a comparison between two of them means something.</p>
    </div>
    <div class="grid grid-4">{cards}</div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">At a glance</p>
      <h2 class="section-title">Compare on the practical numbers</h2>
      <p class="section-sub">Indicative address costs and setup times for a small service company, compiled from public listings and practitioner reports. They are ranges, not quotes.</p>
    </div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>City</th><th>Region</th><th>Registered address</th><th>Typical setup</th><th>Best suited to</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
    {L.editorial_note('Ranges, not appraisals. Address costs move with district supply, and setup time depends on the licence. Check the specific district before you use any number here in a budget.')}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="quote-block">
      <p class="quote-text">A city is not a market. It is a registry counter, a bank branch, and a set of inspectors who will visit your address.</p>
      <p class="quote-cite">The three things a city choice actually decides</p>
    </div>
    <p class="mt-2">{L.btn('What layer 2 asks about a city', '/framework/access/', 'primary')} {L.btn('How to verify an address', '/verify/', 'ghost', icon_name=None)}</p>
  </div>
</section>"""

    return L.page(
        title="Cities",
        description="Ten Chinese cities compared for foreign founders: registered-address costs, setup times, banking practice, work permits and sector mix.",
        path="/cities/",
        body=body,
        nav_active="Cities",
        jsonld=[breadcrumb_ld([("Home", "/"), ("Cities", "/cities/")])],
    )


def city_page(city: dict, cities: list[dict], guides: list[dict],
              sectors: list[dict] | None = None) -> str:
    sky = svg.skyline(city["slug"], 1400, 130, "currentColor", 1, "skyline")
    intro = "".join(f"<p>{L.esc(p)}</p>" for p in city["intro"])
    districts = "".join(
        f"""<div class="district">
      <div><h3 class="district-name">{L.esc(d['name'])}<span class="district-zh">{L.esc(d['zh'])}</span></h3></div>
      <p>{L.esc(d['note'])}</p>
    </div>"""
        for d in city["districts"]
    )
    risks = "".join(f"<li>{L.esc(r)}</li>" for r in city["risks"])
    guide_cards = "".join(L.guide_card(g) for g in guides)
    names = {s["slug"]: s["name"] for s in (sectors or [])}
    sector_chips = "".join(
        f'<a class="city-chip" href="/sectors/#{L.esc(slug)}"><span class="city-chip-en">{L.esc(names.get(slug, slug.replace("-", " ")))}</span></a>'
        for slug in city.get("sectors", [])
    )

    body = f"""
<section class="city-hero">
  <div class="city-hero-sky">{sky}</div>
  <div class="wrap city-hero-inner">
    <div>
      {L.crumbs([('Home', '/'), ('Cities', '/cities/'), (city['name'], None)])}
      <h1 class="city-hero-title mt-2">{L.esc(city['name'])}<span class="city-hero-zh">{L.esc(city['name_zh'])}</span></h1>
      <p class="city-hero-sub">{L.esc(city['tagline'])}</p>
    </div>
    <dl class="city-facts">
      <div class="city-fact"><dt>Registered address</dt><dd>{L.esc(city['address_band'])}</dd></div>
      <div class="city-fact"><dt>Typical setup</dt><dd>{L.esc(city['setup_time'])}</dd></div>
      <div class="city-fact"><dt>Region</dt><dd>{L.esc(city['region'])}</dd></div>
      <div class="city-fact"><dt>Best suited to</dt><dd>{L.esc(city['best_for'])}</dd></div>
    </dl>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid grid-2" style="align-items:start;gap:clamp(2rem,5vw,4rem)">
      <div class="prose">
        {intro}
        {L.answer_box('What actually differs here?', f"<p>{L.esc(city['foreign_note'])}</p>")}
        <p>{L.esc(city['cost_note'])}</p>
      </div>
      <aside class="card side-card">
        <p class="eyebrow">Before you commit to an address here</p>
        <p>The figures on this page are ranges. District practice decides whether a specific address will register, bank and pass inspection — and it changes without much notice.</p>
        <p><strong>Take it to the counter:</strong> ask the district market regulator and the bank to confirm the address before you sign the lease, using the script in <a href="/verify/">how to verify</a>.</p>
        <a class="btn btn-primary btn-block mt-2" href="/verify/">How to check it</a>
      </aside>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Registration practice</p>
      <h2 class="section-title">How the paperwork actually goes in {L.esc(city['name'])}</h2>
      <p class="section-sub">Registry speed, address rules and the district-level differences that decide whether a plan is realistic.</p>
    </div>
    <div class="grid grid-2">
      <div class="card">
        <p class="eyebrow">Registering</p>
        <p>{L.esc(city['practice'])}</p>
        <hr class="rule">
        <p class="eyebrow">Banking</p>
        <p>{L.esc(city['banking'])}</p>
      </div>
      <div class="card">
        <p class="eyebrow">Work permits</p>
        <p>{L.esc(city['work_permit'])}</p>
        <hr class="rule">
        <p class="eyebrow">Address supply</p>
        <p>{L.esc(city['address_band'])}. Expect a lease, a property certificate and a utility bill in the company's name before a bank will look at the file.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Where to locate</p>
      <h2 class="section-title">Districts foreign founders actually use</h2>
      <p class="section-sub">Not a ranking of neighbourhoods. The districts where registration, banking and the relevant sector cluster together.</p>
    </div>
    <div class="district-list">{districts}</div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="grid grid-2" style="gap:2.5rem">
      <div>
        <p class="eyebrow">Sector mix</p>
        <h2 class="section-title">What people build here</h2>
        <p class="section-sub">The sectors where this city has the deepest supplier base, the most experienced agents and the regulators who have seen your model before.</p>
        <div class="city-chips mt-2">{sector_chips}</div>
      </div>
      <div class="card">
        <p class="eyebrow">Know before you commit</p>
        <h2 class="section-title" style="font-size:1.45rem">Three risks in this city</h2>
        <ul class="risk-list">{risks}</ul>
        <hr class="rule">
        <p class="eyebrow">Best suited to</p>
        <p class="mt-1">{L.esc(city['best_for'])}</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Numbers, not impressions</p>
      <h2 class="section-title">Put {L.esc(city['name'])} into the calculators</h2>
      <p class="section-sub">Replace the defaults with what a local agent and a local bank actually quote you. The defaults are national; the differences are local.</p>
    </div>
    <div class="tool-strip-grid">
      <a class="step-card" href="/tools/setup-cost/">
        <span class="step-card-title">What year one costs here<span class="step-card-arrow">{svg.icon('arrow', 15)}</span></span>
        <span class="step-card-reason">Address at this city's band, plus registration, accounting and payroll.</span>
      </a>
      <a class="step-card" href="/tools/structure/">
        <span class="step-card-title">Which vehicle fits<span class="step-card-arrow">{svg.icon('arrow', 15)}</span></span>
        <span class="step-card-reason">Sector, ownership and staff — the three things that decide it.</span>
      </a>
      <a class="step-card" href="/tools/repatriation/">
        <span class="step-card-title">What reaches the shareholder<span class="step-card-arrow">{svg.icon('arrow', 15)}</span></span>
        <span class="step-card-reason">CIT and withholding tax on a dividend out of this city.</span>
      </a>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Before you commit</p>
      <h2 class="section-title">Read these first</h2>
    </div>
    <div class="grid grid-3">{guide_cards}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="next-steps">
      <div>
        <p class="eyebrow">Carry on through the framework</p>
        <h2 class="section-title">A city is layer 2. Three layers decide whether it matters.</h2>
      </div>
      <div class="next-steps-links">
        <a href="/framework/fit/">01 · Do you need an entity →</a>
        <a href="/framework/structure/">03 · Which vehicle →</a>
        <a href="/framework/money/">04 · How money moves →</a>
        <a href="/framework/continuity/">05 · Who keeps it legal →</a>
        <a href="/framework/decision-sheet/">Open the decision sheet →</a>
      </div>
    </div>
  </div>
</section>"""

    return L.page(
        title=f"Starting a business in {city['name']} as a foreigner",
        description=(f"{city['tagline']} Registration practice, registered-address costs "
                     f"({city['address_band']}), setup time and work-permit practice in {city['name']}."),
        path=f"/cities/{city['slug']}/",
        body=body,
        nav_active="Cities",
        body_class="page-city",
        jsonld=[
            breadcrumb_ld([("Home", "/"), ("Cities", "/cities/"), (city["name"], f"/cities/{city['slug']}/")]),
            {
                "@context": "https://schema.org",
                "@type": "Place",
                "name": city["name"],
                "alternateName": city["name_zh"],
                "address": {"@type": "PostalAddress", "addressCountry": "CN", "addressRegion": city["region"]},
            },
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [{
                    "@type": "Question",
                    "name": f"Can a foreigner register a company in {city['name']}?",
                    "acceptedAnswer": {"@type": "Answer", "text": (
                        f"{city['foreign_note']} Typical setup is {city['setup_time']}, and a registered "
                        f"address costs about {city['address_band']} a year.")},
                }],
            },
        ],
    )


# -------------------------------------------------------------------- guides

def guides_index(guides: list[dict]) -> str:
    order = ["Deciding", "Access", "Structure", "Money", "People", "Compliance", "Exit"]
    buckets: dict[str, list[dict]] = {k: [] for k in order}
    for g in guides:
        buckets.setdefault(g["category"], []).append(g)

    blocks = []
    for cat in order:
        group = buckets.get(cat) or []
        if not group:
            continue
        cards = "".join(L.guide_card(g) for g in group)
        blocks.append(f"""
    <h2 class="section-title sub-head" id="{md.slugify(cat)}">{L.esc(cat)}</h2>
    <div class="grid grid-3 mt-2">{cards}</div>""")

    body = f"""
<section class="section">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('Guides', None)])}
    <div class="section-head mt-2">
      <p class="eyebrow">The fact base</p>
      <h1 class="section-title display">Guides, written to be finished</h1>
      <p class="section-sub">Each guide answers a question a foreign founder actually asked, carries a review date, and has been checked against the rule it describes. They support the framework; they do not replace it.</p>
    </div>
    {''.join(blocks)}
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="quote-block">
      <p class="quote-text">Read the framework first. Then use these pages to check a specific rule, not to find an opinion.</p>
      <p class="quote-cite">{L.btn('Open the framework', '/framework/', 'primary')}</p>
    </div>
  </div>
</section>"""

    return L.page(
        title="Guides",
        description="In-depth English guides to starting, funding, staffing and closing a company in China as a foreigner — dated and reviewed.",
        path="/guides/",
        body=body,
        nav_active="Guides",
        jsonld=[breadcrumb_ld([("Home", "/"), ("Guides", "/guides/")])],
    )


def guide_page(post: dict, related: list[dict], cities: list[dict] | None = None) -> str:
    body_html = md.render(post["body"])
    toc_html = L.toc(md.headings(body_html))
    answer_html = L.answer_box("The short answer", md.render(post["answer"])) if post.get("answer") else ""

    layer = post.get("layer")
    layer_html = ""
    if layer:
        l = C.LAYERS[layer - 1]
        layer_html = f"""
      <a class="layer-strip" href="/framework/{l['slug']}/">
        <span class="layer-strip-num">{l['n']:02d}</span>
        <span class="layer-strip-text">Part of Layer {l['n']} — {esc(l['name'])}: {esc(l['question'])}</span>
        {svg.icon('arrow', 16)}
      </a>"""

    next_html = L.next_step(int(layer)) if layer else ""
    terms_html = L.term_chips(post.get("terms") or [])
    city_html = L.city_strip(cities) if cities else ""

    body = f"""
<article>
  <header class="article-head">
    <div class="wrap">
      {L.crumbs([('Home', '/'), ('Guides', '/guides/'), (post['title'], None)])}
      <p class="eyebrow mt-2">{L.esc(post['category'])}</p>
      <h1 class="article-title">{L.esc(post['title'])}</h1>
      <p class="article-standfirst">{L.esc(post['description'])}</p>
      {L.byline(post)}
      {layer_html}
    </div>
  </header>
  <div class="wrap article-layout">
    <aside class="article-aside">
      <div class="card side-card">
        <p class="eyebrow">General information</p>
        <p>This page explains how a rule works. It cannot tell you how the rule applies to your file — that answer comes from a specific counter in a specific district, and we show you how to get it in writing.</p>
        <a class="btn btn-ghost btn-block mt-2" href="/verify/">How to verify</a>
      </div>
    </aside>
    <div class="prose">
      {answer_html}
      {body_html}
      {terms_html}
      {city_html}
      {next_html}
      {L.editorial_note('General information only — not legal, tax or investment advice. Rules change, and city practice varies. Confirm the position for your own file before acting.')}
    </div>
    <aside class="article-aside">
      {toc_html}
    </aside>
  </div>
</article>

{L.related(related)}"""

    return L.page(
        title=post["title"],
        description=post["description"],
        path=f"/guides/{post['slug']}/",
        body=body,
        nav_active="Guides",
        body_class="page-guide",
        og_type="article",
        jsonld=[
            breadcrumb_ld([("Home", "/"), ("Guides", "/guides/"), (post["title"], f"/guides/{post['slug']}/")]),
            article_ld(post, f"/guides/{post['slug']}/"),
        ],
    )
