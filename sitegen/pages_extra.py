"""Framework chapters, tools, glossary, decision sheet and long-form pages."""

from __future__ import annotations

from . import config as C
from . import layout as L
from . import md, svg
from .pages import breadcrumb_ld, article_ld


# ------------------------------------------------------------------ framework

def framework_index(stops: list[dict]) -> str:
    cards = "".join(L.layer_card(l) for l in C.LAYERS)

    stop_cards = []
    for i, l in enumerate(C.LAYERS):
        group = stops[i * 3:(i + 1) * 3]
        items = "".join(f"<li>{L.esc(s['text'])}</li>" for s in group)
        stop_cards.append(f"""
      <div class="card">
        <p class="eyebrow">Layer {l['n']} — {L.esc(l['name'])}</p>
        <ul class="risk-list">{items}</ul>
      </div>""")

    body = f"""
<section class="section framework-hero">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('Framework', None)])}
    <div class="section-head mt-2">
      <p class="eyebrow">The framework</p>
      <h1 class="section-title display">Five decisions, in the order that saves you money</h1>
      <p class="section-sub">Everything a foreign founder needs to settle before capital is paid in. Each layer has a stop condition: hit one and the plan ends, which is usually the cheapest possible outcome.</p>
    </div>
    {L.flow([(l['name'], l['question']) for l in C.LAYERS])}
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    {L.answer_box('How to use this', '<p>Read the five layers in order, once, before you register anything. It takes about forty minutes. Then use the layer that matches where you actually are — most founders discover they are on layer four while still undecided about layer one.</p>')}
    <div class="grid grid-3 layer-grid">{cards}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">The stop conditions</p>
      <h2 class="section-title">What ends a plan, and at which layer</h2>
      <p class="section-sub">These are the situations where the correct answer is to stop. Reading them first is faster than learning them at a bank counter.</p>
    </div>
    <div class="grid grid-2">{''.join(stop_cards)}</div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="next-steps">
      <div>
        <p class="eyebrow">The companion page</p>
        <h2 class="section-title">Deciding is half of it. Checking is the other half.</h2>
      </div>
      <div class="next-steps-links">
        <a href="/verify/">How to verify anything you are told →</a>
        <a href="/tools/structure/">Run the vehicle chooser →</a>
        <a href="/tools/setup-cost/">Cost the first year →</a>
        <a href="/faq/">Common questions →</a>
      </div>
    </div>
  </div>
</section>"""

    return L.page(
        title="The framework",
        description="A five-layer decision framework for foreigners starting a business in China: fit, access, structure, money and continuity — with a stop condition at every layer.",
        path="/framework/",
        body=body,
        nav_active="Framework",
        body_class="page-framework",
        jsonld=[
            breadcrumb_ld([("Home", "/"), ("Framework", "/framework/")]),
            {
                "@context": "https://schema.org",
                "@type": "ItemList",
                "name": "The five layers",
                "itemListElement": [
                    {"@type": "ListItem", "position": l["n"], "name": l["question"],
                     "url": f"{C.SITE_URL}/framework/{l['slug']}/"}
                    for l in C.LAYERS
                ],
            },
        ],
    )


def framework_chapter(ch: dict, prev: dict | None, nxt: dict | None,
                      guides: list[dict], cities: list[dict] | None = None) -> str:
    body_html = md.render(ch["body"])
    toc_html = L.toc(md.headings(body_html))
    related_html = L.related(guides, title=f"Guides that support layer {ch['n']}")

    body = f"""
<header class="chapter-head">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('Framework', '/framework/'), (f"Layer {ch['n']}", None)])}
    <p class="chapter-tag"><span class="chapter-num">{ch['n']:02d}</span> Layer {ch['n']} · {L.esc(ch['name'])}</p>
    <h1 class="chapter-title">{L.esc(ch['question'])}</h1>
    <p class="chapter-lede">{L.esc(ch['summary'])}</p>
  </div>
</header>

<div class="wrap chapter-layout">
  <aside class="chapter-rail">{L.rail(ch['slug'])}{toc_html}</aside>
  <div class="prose">
    {body_html}
    {L.tool_strip(ch['n'])}
    {L.city_strip(cities) if cities else ""}
  </div>
</div>

<div class="wrap">
  {L.pager(prev, nxt)}
</div>

{related_html}"""

    return L.page(
        title=f"Layer {ch['n']}: {ch['question']}",
        description=ch["description"],
        path=f"/framework/{ch['slug']}/",
        body=body,
        nav_active="Framework",
        body_class="page-chapter",
        jsonld=[
            breadcrumb_ld([("Home", "/"), ("Framework", "/framework/"),
                           (f"Layer {ch['n']}", f"/framework/{ch['slug']}/")]),
            article_ld({
                "title": f"Layer {ch['n']}: {ch['question']}",
                "description": ch["description"],
                "updated": ch["updated"],
                "read": ch.get("read", 8),
            }, f"/framework/{ch['slug']}/"),
        ],
    )


# ---------------------------------------------------------------------- tools

def tools_index() -> str:
    body = f"""
<section class="section">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('Tools', None)])}
    <div class="section-head mt-2">
      <p class="eyebrow">Three tools</p>
      <h1 class="section-title display">Work it out before you ask anyone</h1>
      <p class="section-sub">These run entirely in your browser. Nothing is sent anywhere, nothing is stored, and there is no email field — because the point is your answer, not your address.</p>
    </div>
    <div class="grid grid-3">
      <a class="tool-card" href="/tools/structure/">
        <span class="tool-icon">{svg.icon('building', 22)}</span>
        <h2 class="tool-card-title">Which vehicle?</h2>
        <p class="tool-card-desc">Six questions on activity, ownership and staff. You get an indicative vehicle, or an argument for waiting.</p>
        <span class="tool-card-meta">Run the chooser</span>
      </a>
      <a class="tool-card" href="/tools/setup-cost/">
        <span class="tool-icon">{svg.icon('receipt', 22)}</span>
        <h2 class="tool-card-title">What does year one cost?</h2>
        <p class="tool-card-desc">Registration, address, accounting, audit, payroll and the buffer most founders forget.</p>
        <span class="tool-card-meta">Open the calculator</span>
      </a>
      <a class="tool-card" href="/tools/repatriation/">
        <span class="tool-icon">{svg.icon('bank', 22)}</span>
        <h2 class="tool-card-title">What arrives offshore?</h2>
        <p class="tool-card-desc">Corporate income tax, withholding tax and treaty rates on a dividend — and the cost of other routes out.</p>
        <span class="tool-card-meta">Model a dividend</span>
      </a>
    </div>
    {L.editorial_note('These are models, not advice. They will not tell you what a city will approve or what a bank will accept; they will tell you what a decision costs under assumptions you choose — which is the part you control.')}
  </div>
</section>"""

    return L.page(
        title="Tools",
        description="Three browser-based tools for foreign founders in China: a vehicle chooser, a first-year cost calculator, and a dividend repatriation model.",
        path="/tools/",
        body=body,
        nav_active="Tools",
        jsonld=[breadcrumb_ld([("Home", "/"), ("Tools", "/tools/")])],
    )


def _tool_epilogue(layer_n: int, links: list[tuple[str, str, str]],
                   terms: list[str] | None = None,
                   cities: list[dict] | None = None) -> str:
    """A calculator that ends in a number is a dead end. Hand the reader back to
    the reasoning the number sits inside, and to the decision sheet."""
    l = C.LAYERS[layer_n - 1]
    rows = [(f"Layer {l['n']} — {l['name']}: {l['question']}",
             f"/framework/{l['slug']}/",
             "The reasoning this figure sits inside.")]
    rows += list(links)
    rows.append(("Open the decision sheet", "/framework/decision-sheet/",
                 "Twenty-five checks and fifteen stop conditions, on one printable page."))
    items = "".join(
        '<a class="step-card" href="' + href + '">'
        '<span class="step-card-title">' + L.esc(title) + '</span>'
        '<span class="step-card-reason">' + L.esc(reason) + '</span></a>'
        for title, href, reason in rows
    )
    strip = ""
    if terms:
        strip = L.term_chips_by_ids(terms, "The words this tool is built on")
    city_html = L.city_strip(cities) if cities else ""
    return (
        '<section class="section"><div class="wrap">'
        '<p class="eyebrow">What a tool cannot decide</p>'
        '<h2 class="section-title">The number is the start of the argument, not the end of it.</h2>'
        '<p class="section-sub">This tool answers one question. The framework is where '
        'that answer is tested against the other four.</p>'
        '<div class="tool-strip-grid mt-2">' + items + '</div>'
        + strip + city_html +
        '</div></section>'
    )


def structure_tool(cities: list[dict]) -> str:
    body = f"""
<section class="section">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('Tools', '/tools/'), ('Vehicle chooser', None)])}
    <div class="section-head mt-2">
      <p class="eyebrow">Layers 1 and 3 · Fit and structure</p>
      <h1 class="section-title display">Which vehicle?</h1>
      <p class="section-sub">Six questions. The output is an indicative vehicle and the reasoning behind it — not a permission, and not a substitute for the regulator who issues the licence.</p>
    </div>
    <div class="tool-shell">
      <div class="quiz" data-quiz="structure">
        <fieldset class="quiz-step">
          <legend><span class="quiz-n">1</span> What does the entity most need to do?</legend>
          <label class="opt"><input type="radio" name="job" value="invoice"><span>Invoice Chinese business customers and receive RMB</span></label>
          <label class="opt"><input type="radio" name="job" value="employ"><span>Employ staff who work in China</span></label>
          <label class="opt"><input type="radio" name="job" value="licence"><span>Hold a sector licence (F&amp;B, clinic, school, travel, factory)</span></label>
          <label class="opt"><input type="radio" name="job" value="liaison"><span>Only coordinate suppliers, quality or market research</span></label>
          <label class="opt"><input type="radio" name="job" value="nothing"><span>Nothing yet — I am testing the market</span></label>
        </fieldset>

        <fieldset class="quiz-step">
          <legend><span class="quiz-n">2</span> What does the negative list say about your activity?</legend>
          <label class="opt"><input type="radio" name="access" value="open"><span>Open — no foreign-ownership restriction</span></label>
          <label class="opt"><input type="radio" name="access" value="restricted"><span>Restricted — a Chinese partner or an equity cap is required</span></label>
          <label class="opt"><input type="radio" name="access" value="closed"><span>Prohibited to foreign investment</span></label>
          <label class="opt"><input type="radio" name="access" value="unsure"><span>I do not know yet</span></label>
        </fieldset>

        <fieldset class="quiz-step">
          <legend><span class="quiz-n">3</span> How much control do you need?</legend>
          <label class="opt"><input type="radio" name="control" value="full"><span>100% — no Chinese equity partner</span></label>
          <label class="opt"><input type="radio" name="control" value="shared"><span>Shared control is acceptable for market access</span></label>
        </fieldset>

        <fieldset class="quiz-step">
          <legend><span class="quiz-n">4</span> Will you raise outside China or sell the business?</legend>
          <label class="opt"><input type="radio" name="exit" value="yes"><span>Yes, within about five years</span></label>
          <label class="opt"><input type="radio" name="exit" value="no"><span>No, this is a self-funded operating business</span></label>
          <label class="opt"><input type="radio" name="exit" value="unsure"><span>Not sure</span></label>
        </fieldset>

        <fieldset class="quiz-step">
          <legend><span class="quiz-n">5</span> How many people will the Chinese entity employ in year one?</legend>
          <label class="opt"><input type="radio" name="staff" value="0"><span>None — just me</span></label>
          <label class="opt"><input type="radio" name="staff" value="few"><span>One or two</span></label>
          <label class="opt"><input type="radio" name="staff" value="many"><span>Three or more</span></label>
        </fieldset>

        <fieldset class="quiz-step">
          <legend><span class="quiz-n">6</span> When do you need the entity to exist?</legend>
          <label class="opt"><input type="radio" name="when" value="now"><span>Within three months — a contract or hire depends on it</span></label>
          <label class="opt"><input type="radio" name="when" value="later"><span>Within a year</span></label>
          <label class="opt"><input type="radio" name="when" value="none"><span>No fixed date — I am still deciding</span></label>
        </fieldset>

        <button class="btn btn-primary btn-lg" type="button" data-quiz-run>Show my indicative vehicle</button>
        <div class="quiz-result" data-quiz-result hidden></div>
      </div>

      <aside class="calc-aside">
        <div class="card">
          <p class="eyebrow">Then do this</p>
          <p>Whatever this says, the next step is the same: check the sector against the negative list and the licence, then take the address question to the district registry and the bank in writing.</p>
          <a class="btn btn-ghost btn-block mt-2" href="/sectors/">Check your sector</a>
        </div>
        <div class="card mt-2">
          <p class="eyebrow">Why these six</p>
          <p>They are the facts that decide the vehicle: the job, the access rule, the control you need, the exit, the headcount and the clock. Tax is a result, not an input.</p>
        </div>
      </aside>
    </div>
  </div>
</section>"""

    return L.page(
        title="Which vehicle? Structure chooser",
        description="Six questions that produce an indicative vehicle for your China business — WFOE, joint venture, representative office, or no entity yet — with the reasoning.",
        path="/tools/structure/",
        body=body + _tool_epilogue(3, [
            ("Read the WFOE / JV / RO comparison", "/guides/wfoe-jv-roe-comparison/",
             "Control, liability, tax and exit, side by side."),
            ("Do you need an entity at all?", "/guides/do-you-need-a-china-entity/",
             "The five jobs only a Chinese company can do."),
            ("See how the twelve cities differ", "/cities/", "Same rules, different practice."),
        ], terms=["wfoe", "jv", "ro", "fie"], cities=cities),
        nav_active="Tools",
        body_class="page-tool",
        extra_scripts=f'<script src="/js/tools.js?v={C.ASSET_V}" defer></script>',
        jsonld=[breadcrumb_ld([("Home", "/"), ("Tools", "/tools/"), ("Vehicle chooser", "/tools/structure/")])],
    )


def setup_cost_tool(cities: list[dict]) -> str:
    city_opts = "".join(
        f'<option value="{L.esc(c["slug"])}" data-factor="{1.0 if c["rank"] <= 4 else (0.8 if c["rank"] <= 8 else 0.7)}">'
        f'{L.esc(c["name"])}</option>'
        for c in cities
    )
    body = f"""
<section class="section">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('Tools', '/tools/'), ('First-year cost', None)])}
    <div class="section-head mt-2">
      <p class="eyebrow">Layer 4 · Money</p>
      <h1 class="section-title display">What does the first year cost?</h1>
      <p class="section-sub">Registration is the cheap part. This calculator adds the address, the accountant, the audit, the payroll and the buffer — the lines founders discover in month three rather than month one.</p>
    </div>
    <div class="tool-shell">
      <div class="calc" data-calc="setup">
        <div class="calc-row">
          <div class="field">
            <label for="s-city">City of registration</label>
            <select id="s-city" data-in="city">{city_opts}</select>
          </div>
          <div class="field">
            <label for="s-address">Registered address</label>
            <select id="s-address" data-in="address">
              <option value="virtual">Agency virtual address</option>
              <option value="serviced" selected>Shared serviced office</option>
              <option value="office">Private office</option>
            </select>
          </div>
          <div class="field">
            <label for="s-staff">Local employees (besides you)</label>
            <input id="s-staff" type="number" data-in="staff" value="0" min="0" max="50" step="1">
          </div>
          <div class="field">
            <label for="s-salary">Your monthly salary (¥)</label>
            <input id="s-salary" type="number" data-in="salary" value="25000" min="0" step="1000">
          </div>
          <div class="field">
            <label for="s-audit">Annual audit required?</label>
            <select id="s-audit" data-in="audit">
              <option value="yes" selected>Yes — foreign-invested company</option>
              <option value="no">No</option>
            </select>
          </div>
        </div>
        <div class="calc-out">
          <div class="calc-total">
            <span>Year one, all-in</span>
            <strong data-out="total">—</strong>
          </div>
          <ul class="calc-breakdown">
            <li><span>One-off setup (agent, seals, bank)</span><b data-out="setup">—</b></li>
            <li><span>Registered address</span><b data-out="address">—</b></li>
            <li><span>Bookkeeping and filings</span><b data-out="books">—</b></li>
            <li><span>Annual audit</span><b data-out="audit">—</b></li>
            <li><span>Payroll service</span><b data-out="payroll">—</b></li>
            <li><span>Employer social insurance and fund</span><b data-out="social">—</b></li>
            <li><span>Your salary (12 months)</span><b data-out="salary">—</b></li>
            <li class="calc-sum"><span>Working buffer (3 months of costs)</span><b data-out="buffer">—</b></li>
          </ul>
          <p class="calc-note" data-out="note"></p>
        </div>
      </div>
      <aside class="calc-aside">
        <div class="card">
          <p class="eyebrow">What is not in this number</p>
          <ul class="risk-list">
            <li>Rent and fit-out for licensed premises</li>
            <li>Your own individual income tax</li>
            <li>Sector licence fees and consultant costs</li>
            <li>VAT and corporate income tax on revenue</li>
            <li>Legal work on contracts, IP or a JV</li>
          </ul>
          <a class="btn btn-ghost btn-block mt-2" href="/guides/registered-capital-five-year-rule/">Read the capital guide</a>
        </div>
      </aside>
    </div>
  </div>
</section>"""

    return L.page(
        title="First-year cost calculator",
        description="Estimate the true first-year cost of a Chinese company: registration, registered address, bookkeeping, audit, payroll, social insurance and a working buffer.",
        path="/tools/setup-cost/",
        body=body + _tool_epilogue(4, [
            ("Read the registered-address guide", "/guides/registered-address-in-china/",
             "Why the cheap address is the expensive one."),
            ("Read the WFOE/JV/RO comparison", "/guides/wfoe-jv-roe-comparison/",
             "The vehicle changes the compliance bill."),
            ("Check your sector", "/sectors/", "Licensed sectors add costs this model does not include."),
        ], terms=["registered-address", "registered-capital", "annual-report", "social-insurance"],
           cities=cities),
        nav_active="Tools",
        body_class="page-tool",
        extra_scripts=f'<script src="/js/tools.js?v={C.ASSET_V}" defer></script>',
        jsonld=[breadcrumb_ld([("Home", "/"), ("Tools", "/tools/"), ("First-year cost", "/tools/setup-cost/")])],
    )


def repatriation_tool(cities: list[dict]) -> str:
    body = f"""
<section class="section">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('Tools', '/tools/'), ('Repatriation', None)])}
    <div class="section-head mt-2">
      <p class="eyebrow">Layer 4 · Money</p>
      <h1 class="section-title display">What arrives offshore?</h1>
      <p class="section-sub">A dividend is taxed twice before it leaves: corporate income tax on the profit, then withholding tax on the distribution. Treaties reduce the second, not the first. Model both before you plan the cash flow.</p>
    </div>
    <div class="tool-shell">
      <div class="calc" data-calc="repat">
        <div class="calc-row">
          <div class="field">
            <label for="p-profit">Profit before tax (¥)</label>
            <input id="p-profit" type="number" data-in="profit" value="1000000" min="0" step="10000">
          </div>
          <div class="field">
            <label for="p-cit">Corporate income tax</label>
            <select id="p-cit" data-in="cit">
              <option value="25" selected>25% — standard rate</option>
              <option value="5">5% — small low-profit company (conditions apply)</option>
              <option value="15">15% — high-tech enterprise</option>
            </select>
          </div>
          <div class="field">
            <label for="p-wht">Withholding tax on distribution</label>
            <select id="p-wht" data-in="wht">
              <option value="10" selected>10% — no treaty relief</option>
              <option value="5">5% — Hong Kong parent, 25%+ holding, residence certificate</option>
              <option value="10">10% — treaty without a dividend reduction</option>
            </select>
          </div>
          <div class="field">
            <label for="p-reserve">Statutory reserve set aside?</label>
            <select id="p-reserve" data-in="reserve">
              <option value="no" selected>No — already funded</option>
              <option value="yes">Yes — 10% of after-tax profit (until 50% of capital)</option>
            </select>
          </div>
          <div class="field">
            <label for="p-route">Route out</label>
            <select id="p-route" data-in="route">
              <option value="dividend" selected>Dividend to shareholder</option>
              <option value="royalty">Royalty to the parent (6% VAT + WHT)</option>
              <option value="service">Service fee to the parent (6% VAT + WHT)</option>
              <option value="interest">Shareholder loan interest (6% VAT + WHT)</option>
            </select>
          </div>
        </div>
        <div class="calc-out">
          <div class="calc-total">
            <span>Net received offshore</span>
            <strong data-out="net">—</strong>
          </div>
          <ul class="calc-breakdown">
            <li><span>Corporate income tax</span><b data-out="cit">—</b></li>
            <li><span>Statutory reserve</span><b data-out="reserve">—</b></li>
            <li><span>Distributable profit</span><b data-out="dist">—</b></li>
            <li><span>Withholding tax</span><b data-out="wht">—</b></li>
            <li><span>VAT and surcharges</span><b data-out="vat">—</b></li>
            <li class="calc-sum"><span>Effective rate on profit</span><b data-out="effective">—</b></li>
          </ul>
          <p class="calc-note" data-out="note"></p>
        </div>
      </div>
      <aside class="calc-aside">
        <div class="card">
          <p class="eyebrow">What the model assumes</p>
          <ul class="risk-list">
            <li>The profit is already realised and the accounts are audited</li>
            <li>Withholding tax is applied to the distribution, not the profit</li>
            <li>VAT at 6% plus about 12% surcharges on the VAT</li>
            <li>No transfer-pricing adjustment, no late tax, no penalties</li>
            <li>Treaty relief is available and documented, not assumed</li>
          </ul>
          <p class="calc-note">Every route has a different file. The number is the easy part; the documents are the work.</p>
        </div>
      </aside>
    </div>
  </div>
</section>"""

    return L.page(
        title="Repatriation calculator",
        description="Model what reaches an offshore shareholder from a Chinese company: corporate income tax, the statutory reserve, withholding tax and treaty rates.",
        path="/tools/repatriation/",
        body=body + _tool_epilogue(4, [
            ("Read the repatriation guide", "/guides/repatriating-profits-from-china/",
             "Every route out, the tax at each step, and the bank file."),
            ("Read the Hong Kong holding guide", "/guides/hong-kong-holding-company/",
             "When the 5% treaty rate is available, and what substance costs."),
            ("Read the fapiao guide", "/guides/fapiao-for-foreign-founders/",
             "The tax base starts with what you invoiced."),
        ], terms=["withholding-tax", "cit", "tax-treaty", "fapiao"], cities=cities),
        nav_active="Tools",
        body_class="page-tool",
        extra_scripts=f'<script src="/js/tools.js?v={C.ASSET_V}" defer></script>',
        jsonld=[breadcrumb_ld([("Home", "/"), ("Tools", "/tools/"), ("Repatriation", "/tools/repatriation/")])],
    )


# ------------------------------------------------------------- content pages

def _next_step_html(post: dict) -> str:
    layer = post.get("layer")
    if not layer:
        return ""
    return L.next_step(int(layer))


def content_page(post: dict, *, nav_active: str | None = None) -> str:
    body_html = md.render(post["body"])
    toc_html = L.toc(md.headings(body_html))
    kicker = post.get("kicker", "")

    body = f"""
<header class="article-head">
  <div class="wrap">
    {L.crumbs(post["crumbs"])}
    {f'<p class="eyebrow mt-2">{L.esc(kicker)}</p>' if kicker else ''}
    <h1 class="article-title">{L.esc(post['title'])}</h1>
    <p class="article-standfirst">{L.esc(post['description'])}</p>
  </div>
</header>
<div class="wrap article-layout article-layout-content">
  <div class="prose">{body_html}{_next_step_html(post)}</div>
  <aside class="article-aside">{toc_html}</aside>
</div>"""

    return L.page(
        title=post["title"],
        description=post["description"],
        path=post["path"],
        body=body,
        nav_active=nav_active,
        body_class="page-content",
        jsonld=[breadcrumb_ld(post["crumbs"])],
    )


def faq_page(items: list[dict]) -> str:
    order = ["Deciding", "Structure & ownership", "Access & licences",
             "Money, tax & banking", "People & permits", "Compliance & exit"]
    blocks = []
    for cat in order:
        group = [x for x in items if x["cat"] == cat]
        if not group:
            continue
        qs = "".join(
            f'<details class="faq-item"><summary>{L.esc(x["q"])}</summary>'
            f'<div class="faq-a">{md.inline(x["a"])}</div></details>'
            for x in group
        )
        blocks.append(f'<h2 class="section-title sub-head" id="{md.slugify(cat)}">{L.esc(cat)}</h2><div class="faq-group">{qs}</div>')

    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": x["q"],
             "acceptedAnswer": {"@type": "Answer", "text": L.strip_tags(md.inline(x["a"]))}}
            for x in items
        ],
    }

    body = f"""
<section class="section">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('FAQ', None)])}
    <div class="section-head mt-2">
      <p class="eyebrow">Straight answers</p>
      <h1 class="section-title display">Questions people actually ask</h1>
      <p class="section-sub">Short answers, with the guide or framework layer that goes deeper linked from most of them. Nothing here is a substitute for a written answer from the registry, the bank or the sector regulator.</p>
    </div>
    {''.join(blocks)}
  </div>
</section>"""

    return L.page(
        title="FAQ",
        description="Short, direct answers to the questions foreign founders ask most often about starting and running a company in China.",
        path="/faq/",
        body=body,
        nav_active="About",
        jsonld=[breadcrumb_ld([("Home", "/"), ("FAQ", "/faq/")]), faq_ld],
    )


def decision_sheet(sheet: dict) -> str:
    by_n = {l["n"]: l for l in C.LAYERS}
    blocks = []

    for entry in sheet["layers"]:
        n = int(entry["n"])
        meta = by_n.get(n)
        if not meta:
            continue

        checks = "".join(
            '<li><label class="sheet-opt">'
            f'<input type="checkbox" data-check="{L.esc(c["id"])}">'
            '<span class="sheet-mark" aria-hidden="true"></span>'
            f'<span class="sheet-text">{L.esc(c["text"])}</span>'
            "</label></li>"
            for c in entry["checks"]
        )

        tools = C.LAYER_TOOLS.get(n, [])
        tool_links = " · ".join(f'<a href="{h}">{L.esc(lbl)}</a>' for lbl, h, _ in tools)
        tool_html = (f'<p class="sheet-layer-tools">Work this layer out first: {tool_links}</p>'
                     if tool_links else "")

        blocks.append(f"""
<section class="sheet-layer" data-layer="{n}" data-slug="{meta['slug']}" data-name="{L.esc(meta['name'])}">
  <div class="sheet-layer-head">
    <span class="sheet-layer-num">{n:02d}</span>
    <div class="sheet-layer-title-wrap">
      <h2 class="sheet-layer-title">{L.esc(meta['name'])}</h2>
      <p class="sheet-layer-q">{L.esc(meta['question'])}</p>
    </div>
    <a class="sheet-layer-link" href="/framework/{meta['slug']}/">Read layer {n}</a>
  </div>
  <p class="sheet-group-label">Tick each line that is true for you</p>
  <ul class="sheet-list">{checks}</ul>
  {tool_html}
</section>""")

    stops = "".join(
        '<li><label class="sheet-opt sheet-opt-stop">'
        f'<input type="checkbox" data-stop="{L.esc(s["id"])}">'
        '<span class="sheet-mark" aria-hidden="true"></span>'
        f'<span class="sheet-text">{L.esc(s["text"])}</span>'
        "</label></li>"
        for s in sheet["stops"]
    )

    body = f"""
<header class="chapter-head">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('Framework', '/framework/'), ('Decision sheet', None)])}
    <p class="eyebrow">Layers 1 to 5, in order</p>
    <h1 class="chapter-title display">The decision sheet</h1>
    <p class="chapter-lede">Twenty-five things to confirm and fifteen things that end the plan, arranged so that failure stays cheap.</p>
  </div>
</header>

<section class="section">
  <div class="wrap">
    <div class="sheet-intro prose">
      <p>{L.esc(sheet['intro'])}</p>
      <p>{L.esc(sheet['note'])}</p>
    </div>

    <div class="sheet" data-sheet>
      <div class="sheet-top">
        <div class="sheet-meter">
          <p class="sheet-progress" data-progress>0 of 5 layers cleared</p>
          <div class="sheet-bar" aria-hidden="true"><span data-bar style="width:0%"></span></div>
        </div>
        <button type="button" class="sheet-reset" data-sheet-reset>Clear all</button>
      </div>
      <div class="sheet-verdict" data-verdict hidden></div>
      {''.join(blocks)}
      <section class="sheet-layer sheet-layer-stop" data-layer="6" data-slug="" data-name="the stop conditions">
        <div class="sheet-layer-head">
          <span class="sheet-layer-num">!</span>
          <div class="sheet-layer-title-wrap">
            <h2 class="sheet-layer-title">Stop conditions</h2>
            <p class="sheet-layer-q">Any one of these ends the plan, whatever the other layers say</p>
          </div>
        </div>
        <ul class="sheet-list">{stops}</ul>
      </section>
      <p class="sheet-foot">Print this page and take it to your lawyer. A ticked box is your own answer, not evidence — the sheet exists to show you which answers you have not actually checked.</p>
    </div>

    <div class="sheet-intro prose">
      <p><strong>What this sheet is not.</strong> It is not a legal opinion, a valuation, or a prediction. It does not tell you whether the business will work. It is a way of finding out, in ten minutes and for nothing, whether a plan you are considering fails on the first two layers — which is where most plans by foreign founders actually fail.</p>
      <p>If you want the reasoning behind any line, follow it back to <a href="/framework/">the framework</a>. If you want the vocabulary you will hear at the counter, the <a href="/glossary/">glossary</a> has the terms that come up most often, with the characters you will see on paper.</p>
    </div>
  </div>
</section>"""

    return L.page(
        title="The decision sheet",
        description="The five-layer framework as a working checklist: twenty-five checks and fifteen stop conditions for foreigners starting a business in China.",
        path="/framework/decision-sheet/",
        body=body,
        nav_active="Framework",
        body_class="page-chapter",
        jsonld=[breadcrumb_ld([("Home", "/"), ("Framework", "/framework/"),
                               ("Decision sheet", "/framework/decision-sheet/")])],
        extra_scripts=f'<script src="/js/decision.js?v={C.ASSET_V}" defer></script>',
    )


def glossary(entries: list[dict], guides: list[dict]) -> str:
    titles = {g["slug"]: g["title"] for g in guides}
    ordered = sorted(entries, key=lambda e: e["english"].lower())

    by_letter: dict[str, list[dict]] = {}
    for e in ordered:
        by_letter.setdefault(e["english"][0].upper(), []).append(e)

    def card(e: dict) -> str:
        gid = e["id"]
        see = "".join(
            f'<a href="/guides/{L.esc(s)}/">{L.esc(titles.get(s, s.replace("-", " ")))}</a>'
            for s in e.get("see", []) if s
        )
        see_html = f'<p class="gterm-see">Where this matters: {see}</p>' if see else ""
        return f"""
<li class="gterm" id="{gid}">
  <div class="gterm-head">
    <h3 class="gterm-zh">{L.esc(e['term'])}</h3>
    <p class="gterm-py">{L.esc(e['pinyin'])}</p>
    <p class="gterm-en">{L.esc(e['english'])}</p>
  </div>
  <p class="gterm-def">{L.esc(e['def'])}</p>
  {see_html}
</li>"""

    jump = "".join(f'<a href="#letter-{k}">{k}</a>' for k in by_letter)
    sections = "".join(
        f'<h2 class="g-letter" id="letter-{k}">{k}</h2>'
        f'<ul class="g-list">{"".join(card(e) for e in group)}</ul>'
        for k, group in by_letter.items()
    )

    term_set = {
        "@context": "https://schema.org",
        "@type": "DefinedTermSet",
        "name": "Glossary of Chinese company and investment terms",
        "hasDefinedTerm": [
            {"@type": "DefinedTerm", "name": e["english"],
             "alternateName": e["term"], "description": e["def"]}
            for e in ordered
        ],
    }

    body = f"""
<header class="chapter-head">
  <div class="wrap">
    {L.crumbs([('Home', '/'), ('Glossary', None)])}
    <p class="eyebrow">{len(entries)} terms</p>
    <h1 class="chapter-title display">The words on the paperwork</h1>
    <p class="chapter-lede">Every term you are likely to meet at a registry counter, a bank or a licence inspection, with the characters, the pinyin, and what it actually decides.</p>
  </div>
</header>

<section class="section">
  <div class="wrap">
    <div class="glossary-intro prose">
      <p>Company formation in China is discussed in a vocabulary that carries legal weight and is almost never translated in the room. Knowing the characters on a business licence is the difference between understanding what you own and being told what you own.</p>
      <p>The pinyin is included because you will hear these words spoken long before you see them written. Say the term out loud once; it is the fastest way to stop a conversation that has moved past you.</p>
    </div>
    <nav class="g-jump" aria-label="Jump to letter">{jump}</nav>
    {sections}
    <div class="glossary-intro prose">
      <p>If a term you met is missing, that is a gap worth reporting — <a href="/about/">tell us</a> and it will be added with the same treatment.</p>
    </div>
  </div>
</section>"""

    return L.page(
        title="Glossary",
        description="Chinese company, investment and tax terms with characters, pinyin and plain-English definitions, from 营业执照 to 清算.",
        path="/glossary/",
        body=body,
        body_class="page-chapter",
        jsonld=[breadcrumb_ld([("Home", "/"), ("Glossary", "/glossary/")]), term_set],
    )


def not_found() -> str:
    body = f"""
<section class="section">
  <div class="wrap">
    <div class="notfound">
      <p class="eyebrow">404</p>
      <h1 class="section-title display">That page does not exist</h1>
      <p class="section-sub">It may have been renamed, or it may never have existed. The framework is a good place to pick up again.</p>
      <p class="mt-2">{L.btn('The framework', '/framework/', 'primary')} {L.btn('All sectors', '/sectors/', 'ghost', icon_name=None)}</p>
    </div>
  </div>
</section>"""

    return L.page(
        title="Page not found",
        description="Page not found.",
        path="/404.html",
        body=body,
        noindex=True,
    )
