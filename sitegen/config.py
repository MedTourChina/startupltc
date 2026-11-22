"""Site-wide configuration.

This project is deliberately non-commercial: there is no company behind it,
no advertising, no referral fees and no data collection. Nothing in the
configuration should imply otherwise.
"""

from __future__ import annotations

SITE_NAME = "Lifetourchina Startup"
# The masthead is set on two lines, matching the social card. SITE_NAME is the
# single string used in <title>, copyright and structured data.
BRAND_LINE_1 = "Lifetourchina"
BRAND_LINE_2 = "Startup"
SITE_TAGLINE = "Starting a business in China, in the right order."
SITE_DESCRIPTION = (
    "A free, independent guide for foreigners starting and running a company in China — "
    "whether you need an entity at all, what the negative list lets you own, and what "
    "registration, banking, tax and compliance actually cost."
)

SITE_URL = "https://startup.lifetourchina.com"

# Set at build time to a short hash of the CSS/JS bundle. Appended to asset
# URLs so the immutable cache in _headers can never serve a stale stylesheet
# after a redesign.
ASSET_V = ""

# Corrections only. There is no sales inbox, because there is no sales.
CORRECTIONS_EMAIL = "notes@lifetourchina.com"

LEGAL_ENTITY = "An independent editorial project"
LAST_UPDATED = "November 2026"

AUTHOR_NAME = "Maya Chen"
AUTHOR_ROLE = "Editor"
REVIEWER_NAME = "Wei Lian"
REVIEWER_ROLE = "Corporate counsel, Shanghai"

# The five layers are the spine of the site. Order matters: each layer can
# veto the project before the next one is reached.
LAYERS = [
    {
        "n": 1,
        "slug": "fit",
        "name": "Fit",
        "question": "Does your business need a Chinese entity at all?",
        "summary": (
            "Most founders register a company before they can say what the company is for. "
            "Start with the job the entity has to do — invoice, hire, hold a licence, or nothing yet."
        ),
    },
    {
        "n": 2,
        "slug": "access",
        "name": "Access",
        "question": "Are you allowed to do this, here?",
        "summary": (
            "The negative list, the sector licence and the registered address decide whether "
            "a company is possible at all — before structure, capital or tax matter."
        ),
    },
    {
        "n": 3,
        "slug": "structure",
        "name": "Structure",
        "question": "Which vehicle, and who controls it?",
        "summary": (
            "WFOE, joint venture, representative office or a Hong Kong holding company: "
            "four different answers to control, liability, tax and the exit you will need one day."
        ),
    },
    {
        "n": 4,
        "slug": "money",
        "name": "Money",
        "question": "How much capital, and how does money move?",
        "summary": (
            "Registered capital is a promise with a five-year clock. The bank account, the "
            "capital account and the invoice system decide whether you can actually trade."
        ),
    },
    {
        "n": 5,
        "slug": "continuity",
        "name": "Continuity",
        "question": "Who runs it, and how does it stay legal?",
        "summary": (
            "Work permits, payroll, social insurance, annual filings, audit and the closure "
            "you will eventually need. A company is a recurring obligation, not a one-off filing."
        ),
    },
]

NAV = [
    ("Framework", "/framework/"),
    ("Sectors", "/sectors/"),
    ("Cities", "/cities/"),
    ("Guides", "/guides/"),
    ("Tools", "/tools/"),
    ("About", "/about/"),
]

FOOTER_NAV = [
    (
        "The framework",
        [("Overview", "/framework/")] + [
            (f"{l['n']}. {l['name']}", f"/framework/{l['slug']}/") for l in LAYERS
        ] + [("Decision sheet", "/framework/decision-sheet/")],
    ),
    (
        "Explore",
        [
            ("Sectors", "/sectors/"),
            ("Cities", "/cities/"),
            ("Guides", "/guides/"),
            ("Tools", "/tools/"),
            ("Glossary", "/glossary/"),
            ("How to verify", "/verify/"),
        ],
    ),
    (
        "About",
        [
            ("What this is", "/about/"),
            ("Questions", "/faq/"),
            ("Disclaimer", "/legal/disclaimer/"),
        ],
    ),
]

# The four variables that actually differ between cities, as glossary ids.
# Shown on every city page: these are the words local practice is argued in.
CITY_TERMS = [
    "registered-address",
    "work-permit",
    "social-insurance",
    "corporate-bank-account",
]

# What to do next, per layer. A framework that dead-ends is a lecture.
# Each entry: (label, href, one-line reason)
LAYER_TOOLS = {
    1: [
        ("Work out whether you need an entity", "/tools/structure/",
         "Six questions, an indicative answer, and the reasons behind it."),
        ("Read the entity-alternatives guide", "/guides/do-you-need-a-china-entity/",
         "Exporting through an agent, using a partner, or waiting — and what each costs you."),
    ],
    2: [
        ("Check your sector", "/sectors/",
         "Twelve sectors, their negative-list status and the licence that gates each one."),
        ("Read the registered-address guide", "/guides/registered-address-in-china/",
         "Why a cheap address is the most expensive line on the invoice."),
        ("Compare ten cities", "/cities/",
         "The same dimensions everywhere, so a comparison means something."),
    ],
    3: [
        ("Run the structure chooser", "/tools/structure/",
         "WFOE, JV, representative office or Hong Kong holding company, by what you need it to do."),
        ("Read the WFOE/JV/RO comparison", "/guides/wfoe-jv-roe-comparison/",
         "Control, liability, tax and exit, side by side."),
        ("Read the Hong Kong holding guide", "/guides/hong-kong-holding-company/",
         "When a holding company helps, when it is decoration, and what it costs to keep."),
    ],
    4: [
        ("Cost the first year", "/tools/setup-cost/",
         "Registration, address, accounting, payroll and the buffer most founders forget."),
        ("Read the registered-capital guide", "/guides/registered-capital-five-year-rule/",
         "The five-year clock, and how much to promise."),
        ("Read the fapiao guide", "/guides/fapiao-for-foreign-founders/",
         "The invoice system is the business system; it is not paperwork."),
        ("Model a dividend", "/tools/repatriation/",
         "CIT, withholding tax and treaty rates, as one number."),
    ],
    5: [
        ("Read the compliance calendar", "/guides/annual-compliance-calendar/",
         "Every recurring filing, with the month it falls due."),
        ("Read the first-hire guide", "/guides/hiring-first-employee-china/",
         "Contracts, social insurance and the cost of a salary."),
        ("Read the closure guide", "/guides/closing-a-company-in-china/",
         "How an exit works, and why it takes longer than the entry."),
    ],
}

# Shown on every page footer. It is the whole business model.
PLEDGE = (
    "No advertising. No commissions. No accounts. No forms. "
    "This site collects nothing about you and sells nothing to anyone."
)

USD_CNY = 7.10
