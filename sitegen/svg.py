"""Inline SVG assets: icon set, procedural city skylines, brand mark.

The site ships zero raster images. Skylines are generated deterministically
from a per-city seed so each city card has a distinct silhouette while the
whole set stays visually consistent.
"""

from __future__ import annotations

import random

_PATHS = {
    "arrow": '<path d="M4 12h15M13 6l6 6-6 6"/>',
    "arrow-up": '<path d="M7 17 17 7M8 7h9v9"/>',
    "check": '<path d="M4 12.5 9 17.5 20 6.5"/>',
    "pin": '<path d="M12 21s7-5.5 7-11a7 7 0 1 0-14 0c0 5.5 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/>',
    "scale": '<path d="M12 4v16M7 20h10M4 8h16M4 8l-2 5a3 3 0 0 0 6 0L6 8M20 8l-2 5a3 3 0 0 0 6 0l-2-5"/>',
    "shield": '<path d="M12 3 5 6v6c0 4.5 3 7.7 7 9 4-1.3 7-4.5 7-9V6l-7-3z"/><path d="m9 12 2.2 2.2L15.5 10"/>',
    "key": '<circle cx="8" cy="8" r="4"/><path d="m11 11 9 9M17 14l3-3M20 17l2-2"/>',
    "chart": '<path d="M4 20V4M4 20h16M8 16V11M12.5 16V7M17 16v-4"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "mail": '<rect x="3" y="5.5" width="18" height="13" rx="2"/><path d="m3.5 7 8.5 6 8.5-6"/>',
    "phone": '<path d="M6.5 3.5 9 3l2 5-2.5 1.5a12 12 0 0 0 6 6L16 13l5 2 .5 2.5A2 2 0 0 1 19.4 20C11 19.5 4.5 13 4 4.6a2 2 0 0 1 2.5-1.1z"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.5 2.3 3.8 5.3 3.8 8.5S14.5 18.2 12 20.5C9.5 18.2 8.2 15.2 8.2 12S9.5 5.8 12 3.5z"/>',
    "home": '<path d="m3.5 10.5 8.5-7 8.5 7V20a1 1 0 0 1-1 1h-15a1 1 0 0 1-1-1v-9.5z"/><path d="M9.5 21v-6h5v6"/>',
    "file": '<path d="M13 3.5H7a1.5 1.5 0 0 0-1.5 1.5v14A1.5 1.5 0 0 0 7 20.5h10a1.5 1.5 0 0 0 1.5-1.5V9l-5.5-5.5z"/><path d="M13 3.5V9h5.5M8.5 13h7M8.5 16.5h4.5"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6 6 18"/>',
    "chevron": '<path d="m6 9.5 6 6 6-6"/>',
    "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3.5 20c0-3 2.5-5.2 5.5-5.2s5.5 2.2 5.5 5.2"/><path d="M16 5.2a3.2 3.2 0 0 1 0 6.2M17.5 14.9c1.8.6 3 2.3 3 4.4"/>',
    "spark": '<path d="M12 3.5 13.9 9l5.6 1.9-5.6 1.9L12 18.5l-1.9-5.7L4.5 10.9 10.1 9 12 3.5z"/>',
    "building": '<path d="M4 21V6.5L12 3v18M12 21h8V10l-8-3.5"/><path d="M7 9.5h2M7 13h2M7 16.5h2M15 12.5h2M15 16.5h2M2.5 21h19"/>',
    "bank": '<path d="M3 9.5 12 4l9 5.5M4.5 10.5v8M9 10.5v8M15 10.5v8M19.5 10.5v8M2.5 20.5h19"/>',
    "receipt": '<path d="M6 3.5h12v17l-3-2-3 2-3-2-3 2v-17z"/><path d="M9 8h6M9 11.5h6M9 15h3.5"/>',
    "badge": '<circle cx="12" cy="9.5" r="5.5"/><path d="m8.5 14-1.5 6.5 5-2.5 5 2.5L15.5 14"/><path d="m10 9.5 1.5 1.5 3-3"/>',
    "factory": '<path d="M3 20.5V11l6 3.5V11l6 3.5V7l6 3.5v10H3z"/><path d="M6.5 17h2M11 17h2M15.5 17h2"/>',
    "code": '<path d="m8 8-4 4 4 4M16 8l4 4-4 4M13.5 5l-3 14"/>',
    "cart": '<path d="M3 4h2l2.4 11h10.2L20 7H6"/><circle cx="9.5" cy="19" r="1.4"/><circle cx="17" cy="19" r="1.4"/>',
    "coffee": '<path d="M4.5 9h12v5.5a4.5 4.5 0 0 1-4.5 4.5H9a4.5 4.5 0 0 1-4.5-4.5V9z"/><path d="M16.5 10.5H19a2 2 0 0 1 0 4h-2.5M7 3.5v2.5M11 3.5v2.5M15 3.5v2.5"/>',
    "health": '<path d="M12 4v16M4 12h16"/><circle cx="12" cy="12" r="9"/>',
    "truck": '<path d="M3 6h11v10H3zM14 9.5h4l3 3V16h-7z"/><circle cx="7" cy="18.5" r="1.8"/><circle cx="17" cy="18.5" r="1.8"/>',
    "briefcase": '<rect x="3" y="7.5" width="18" height="12.5" rx="2"/><path d="M9 7.5V6a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v1.5M3 12.5h18M10.5 12.5v2h3v-2"/>',
    "map": '<path d="m3.5 6.5 5-2 7 2 5-2v13l-5 2-7-2-5 2v-13z"/><path d="M8.5 4.5v13M15.5 6.5v13"/>',
    "lock": '<rect x="4.5" y="10" width="15" height="10.5" rx="2"/><path d="M8 10V7.5a4 4 0 0 1 8 0V10M12 14v3"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 4.5 4.5"/>',
    "alert": '<path d="M12 3.5 2.5 20.5h19L12 3.5z"/><path d="M12 9.5v5M12 17.5v.5"/>',
}


def icon(name: str, size: int = 20, cls: str = "icon") -> str:
    path = _PATHS.get(name, _PATHS["spark"])
    return (
        f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true" focusable="false">{path}</svg>'
    )


def skyline(seed: str, width: int = 340, height: int = 104, fill: str = "currentColor",
            opacity: float = 1.0, cls: str = "skyline") -> str:
    """Deterministic procedural skyline for a city card."""
    rnd = random.Random(seed)
    parts: list[str] = []
    x = 0.0
    while x < width:
        w = min(rnd.randint(13, 33), width - x)
        if w < 7:
            break
        h = rnd.randint(int(height * 0.22), int(height * 0.94))
        y = height - h
        parts.append(f'<rect x="{x:.0f}" y="{y}" width="{w}" height="{h}"/>')
        roll = rnd.random()
        cx = x + w / 2
        if roll < 0.16:
            parts.append(f'<rect x="{cx - 1:.0f}" y="{max(y - 14, 0)}" width="2" height="14"/>')
        elif roll < 0.30:
            inner = round(w * 0.56)
            parts.append(
                f'<rect x="{x + (w - inner) / 2:.0f}" y="{max(y - 9, 0)}" width="{inner}" height="9"/>'
            )
        elif roll < 0.40:
            parts.append(
                f'<path d="M{x:.0f} {y:.0f} L{cx:.0f} {max(y - h * 0.22, 0):.0f} '
                f'L{x + w:.0f} {y:.0f} Z"/>'
            )
        x += w + rnd.choice([1, 2, 2, 3, 5])

    return (
        f'<svg class="{cls}" viewBox="0 0 {width} {height}" preserveAspectRatio="none" '
        f'fill="{fill}" opacity="{opacity}" aria-hidden="true" focusable="false">'
        + "".join(parts)
        + "</svg>"
    )


# A sprout rising out of a baseline: growth, but rooted in something.
BRAND_MARK = (
    '<svg class="brand-mark" viewBox="0 0 32 32" aria-hidden="true" focusable="false">'
    '<circle cx="16" cy="17" r="13.5" fill="currentColor" opacity=".08"/>'
    '<path d="M16 27.5V13.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
    '<path d="M16 19.5c0-5.2-3.6-8.4-8.4-8.4 0 5.3 3.2 8.4 8.4 8.4z" fill="var(--amber)"/>'
    '<path d="M16 15.5c0-4.2 2.9-6.8 6.9-6.8 0 4.4-2.8 6.8-6.9 6.8z" fill="var(--amber)" opacity=".62"/>'
    '<rect x="6.5" y="26.6" width="19" height="2.4" rx="1.2" fill="currentColor"/>'
    "</svg>"
)

FAVICON = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
    '<rect width="32" height="32" rx="7" fill="#12192b"/>'
    '<path d="M16 26.5V13" stroke="#faf8f4" stroke-width="2" stroke-linecap="round"/>'
    '<path d="M16 19c0-4.8-3.4-7.7-7.8-7.7 0 4.9 3 7.7 7.8 7.7z" fill="#d98a3a"/>'
    '<path d="M16 15.2c0-3.9 2.7-6.3 6.4-6.3 0 4.1-2.6 6.3-6.4 6.3z" fill="#d98a3a" opacity=".65"/>'
    '<rect x="7" y="25.8" width="18" height="2.2" rx="1.1" fill="#faf8f4"/>'
    "</svg>"
)
