#!/usr/bin/env python3
"""
Render responsive terminal-window project spotlight cards with accurate, factual project data.
"""
import os
import html
import xml.etree.ElementTree as ET

PROJECTS = [
    {
        "id": "securebox",
        "alt_id": "securethebox",
        "title": "SecureBox",
        "repo_url": "https://github.com/anirudhadg04/SecureBox",
        "cmd": "anirudhadg04@github: ~/projects/securebox",
        "badge": "WEB APP",
        "level": "&#x25cf; Open Source",
        "level_color": "#39d353",
        "cat_pill": "CLIENT-SIDE DOCUMENT ENCRYPTION",
        "desc_lines": [
            "Privacy-first client-side document encryption",
            "with Web Crypto AES-256-GCM & SHA-256 integrity."
        ],
        "tags": ["Web Crypto API", "AES-256-GCM", "TypeScript", "React"],
        "footer_l": "136 Vitest Tests &#183; Client-Side Only",
        "status": "ACTIVE"
    },
    {
        "id": "verysecurewebsite",
        "alt_id": "card-appsec",
        "title": "VerySecureWebsite",
        "repo_url": "https://github.com/anirudhadg04/VerySecureWebsite",
        "cmd": "anirudhadg04@github: ~/labs/verysecurewebsite",
        "badge": "SECURITY LAB",
        "level": "&#x25cf; Educational",
        "level_color": "#22d3ee",
        "cat_pill": "VULNERABILITY RESEARCH & TESTING",
        "desc_lines": [
            "Intentionally vulnerable web application for",
            "learning AppSec with automated Pytest verifiers."
        ],
        "tags": ["Python", "Flask", "Pytest", "OWASP Top 10"],
        "footer_l": "Automated Pytest Verifiers",
        "status": "EDUCATIONAL"
    },
    {
        "id": "tabzero",
        "alt_id": "card-tabzero",
        "title": "tabzero.",
        "repo_url": "https://github.com/anirudhadg04/tabzero",
        "cmd": "anirudhadg04@github: ~/projects/tabzero",
        "badge": "HACKATHON",
        "level": "&#x25cf; SJC Hackathon",
        "level_color": "#39d353",
        "cat_pill": "DIGITAL WELLNESS ECOSYSTEM",
        "desc_lines": [
            "Hackathon digital wellness project built with",
            "@NyNehalJois (Extension & Android App)."
        ],
        "tags": ["Browser Extension", "Android APK", "Kotlin", "TypeScript"],
        "footer_l": "Collab with @NyNehalJois &#183; SJC Hackathon",
        "status": "HACKATHON"
    }
]

W = 410
H = 265
TITLEBAR_H = 34
PAD = 18

BG = "#040805"
BG2 = "#08100a"
BORDER = "#00ff41"
FRAME = "#1a3821"
MUTED = "#6e7681"
TEXT = "#e6edf3"
DESC_COLOR = "#8b949e"
GREEN = "#00ff41"
CYAN = "#00d2ff"

def render_card(p):
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        '<style>',
        '@keyframes cardIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }',
        '.card { animation: cardIn 0.5s ease-out both; }',
        '.hud-border { stroke: #00ff41; stroke-opacity: 0.6; transition: stroke-opacity 0.2s; }',
        '.hud-border:hover { stroke-opacity: 1; }',
        '@media (prefers-reduced-motion: reduce) { .card { animation: none !important; opacity: 1 !important; transform: none !important; } }',
        '</style>',
        f'<defs>',
        f'<linearGradient id="lbg_{p["id"]}" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>',
        f'</linearGradient>',
        f'</defs>',
        f'<g class="card">',
        f'<rect width="{W}" height="{H}" rx="10" fill="url(#lbg_{p["id"]})"/>',
        f'<rect class="hud-border" x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="none" stroke-width="1.2"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-width="1"/>',
    ]

    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*14}" cy="{TITLEBAR_H/2}" r="4" fill="{dotcol}"/>')
    parts.append(f'<text x="{PAD + 48}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="10.5">{html.escape(p["cmd"])}</text>')

    top_y = TITLEBAR_H + 14
    badge_text = p["badge"]
    bw = len(badge_text) * 7.5 + 14
    parts.append(f'<rect x="{PAD}" y="{top_y}" width="{bw:.1f}" height="20" rx="3" fill="{GREEN}"/>')
    parts.append(f'<text x="{PAD + bw/2:.1f}" y="{top_y + 14}" fill="#000000" font-size="10" font-weight="900" text-anchor="middle">{html.escape(badge_text)}</text>')

    level_txt = p["level"]
    # level already has &#x25cf;
    parts.append(f'<text x="{W - PAD}" y="{top_y + 14}" fill="{p["level_color"]}" font-size="10" font-weight="700" text-anchor="end">{level_txt}</text>')

    title_y = top_y + 38
    parts.append(f'<text x="{PAD}" y="{title_y}" fill="#ffffff" font-size="19" font-weight="800" letter-spacing="0.5">{html.escape(p["title"])}</text>')

    pill_y = title_y + 10
    cat_text = p["cat_pill"]
    parts.append(f'<rect x="{PAD}" y="{pill_y}" width="{W - PAD*2}" height="18" rx="3" fill="rgba(0, 210, 255, 0.12)" stroke="rgba(0, 210, 255, 0.4)" stroke-width="0.8"/>')
    parts.append(f'<text x="{PAD + 8}" y="{pill_y + 13}" fill="{CYAN}" font-size="9" font-weight="700" letter-spacing="0.8">{html.escape(cat_text)}</text>')

    desc_y = pill_y + 30
    for idx, line in enumerate(p["desc_lines"][:2]):
        parts.append(f'<text x="{PAD}" y="{desc_y + idx*16}" fill="{DESC_COLOR}" font-size="11">{html.escape(line)}</text>')

    tag_y = H - 52
    cur_tag_x = PAD
    for tag in p["tags"][:4]:
        tw = len(tag) * 6.5 + 12
        parts.append(f'<rect x="{cur_tag_x:.1f}" y="{tag_y}" width="{tw:.1f}" height="18" rx="3" fill="#0d140e" stroke="{FRAME}" stroke-width="0.8"/>')
        parts.append(f'<text x="{cur_tag_x + tw/2:.1f}" y="{tag_y + 13}" fill="{GREEN}" font-size="9.5" text-anchor="middle">{html.escape(tag)}</text>')
        cur_tag_x += tw + 6

    foot_line_y = H - 28
    parts.append(f'<line x1="{PAD}" y1="{foot_line_y}" x2="{W-PAD}" y2="{foot_line_y}" stroke="{FRAME}" stroke-opacity="0.6"/>')

    parts.append(f'<text x="{PAD}" y="{foot_line_y + 17}" fill="{MUTED}" font-size="9.5">{p["footer_l"]}</text>')
    parts.append(f'<text x="{W-PAD}" y="{foot_line_y + 17}" fill="{GREEN}" font-size="9.5" font-weight="700" text-anchor="end">{html.escape(p["status"])}</text>')

    parts.append('</g></svg>')
    return "".join(parts)

def main():
    out_dir = os.path.join(os.path.dirname(__file__), "cards")
    os.makedirs(out_dir, exist_ok=True)
    for p in PROJECTS:
        svg_content = render_card(p)
        # Validate XML parse strictly
        ET.fromstring(svg_content)
        out_path = os.path.join(out_dir, f"card-{p['id']}.svg")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        if "alt_id" in p:
            alt_path = os.path.join(out_dir, f"{p['alt_id']}.svg")
            with open(alt_path, "w", encoding="utf-8") as f:
                f.write(svg_content)
        print(f"Validated and saved: {p['title']}")

if __name__ == "__main__":
    main()
