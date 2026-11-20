#!/usr/bin/env python3
"""
Render responsive terminal-window project spotlight cards for top repositories.
"""
import os
import html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "..", "cards")
os.makedirs(OUT_DIR, exist_ok=True)

PROJECTS = [
    {
        "id": "securebox",
        "alt_id": "securethebox",
        "title": "SecureTheBox",
        "repo_url": "https://github.com/anirudhadg04/SecureBox",
        "cmd": "anirudhadg04@github: ~/projects/securethebox",
        "lab_code": "[0000CRYPTO]",
        "level": "HANDS-ON LAB",
        "level_color": "#39d353",
        "cat_pill": "CLIENT-SIDE CRYPTOGRAPHY SANDBOX",
        "desc": "Client-side document protection sandbox exploring authenticated AES-256-GCM encryption, binary envelope parsing, and SHA-256 integrity verification.",
        "tags": ["Web Crypto API", "AES-256-GCM", "SHA-256", "TypeScript", "JSZip"],
        "xp": "XP 2000",
        "footer_l": "49 Tests · NIST Verified",
        "status": "CLIENT ENCLAVE"
    },
    {
        "id": "verysecurewebsite",
        "alt_id": "card-appsec",
        "title": "VerySecureWebsite",
        "repo_url": "https://github.com/anirudhadg04/VerySecureWebsite",
        "cmd": "anirudhadg04@github: ~/labs/verysecurewebsite",
        "lab_code": "[0000APSEC]",
        "level": "CTF / LAB",
        "level_color": "#22d3ee",
        "cat_pill": "VULNERABILITY RESEARCH & TESTING",
        "desc": "Local security testing lab and vulnerability testbed for practicing exploit mechanics and automated verification for BOLA/IDOR, BFLA, and XSS.",
        "tags": ["Python", "Flask", "Pytest", "BOLA/IDOR", "XSS Labs"],
        "xp": "XP 1500",
        "footer_l": "Automated Pytest Verifiers",
        "status": "LEARNING EXPLOITS"
    },
    {
        "id": "tabzero",
        "alt_id": "card-tabzero",
        "title": "tabzero.",
        "repo_url": "https://github.com/anirudhadg04/tabzero",
        "cmd": "anirudhadg04@github: ~/projects/tabzero",
        "lab_code": "[0000FOCUS]",
        "level": "v1.0.2",
        "level_color": "#39d353",
        "cat_pill": "MINDFUL ATTENTION & FOCUS APP",
        "desc": "Cross-platform digital wellness project exploring browser extensions and Android development with calm nature sanctuaries and distraction-free boundaries.",
        "tags": ["Android APK", "Chrome / Firefox", "Local-First", "Focus Engine"],
        "xp": "RELEASE",
        "footer_l": "100% Offline & Local-First",
        "status": "ACTIVE PROJECT"
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
    badge_text = p["lab_code"]
    bw = len(badge_text) * 7.5 + 8
    parts.append(f'<rect x="{PAD}" y="{top_y}" width="{bw:.1f}" height="20" rx="3" fill="{GREEN}"/>')
    parts.append(f'<text x="{PAD + bw/2:.1f}" y="{top_y + 14}" fill="#000000" font-size="10" font-weight="900" text-anchor="middle">{badge_text}</text>')

    level_txt = f'● {p["level"]}'
    parts.append(f'<text x="{W - PAD}" y="{top_y + 14}" fill="{p["level_color"]}" font-size="10" font-weight="700" text-anchor="end">{level_txt}</text>')

    title_y = top_y + 38
    parts.append(f'<text x="{PAD}" y="{title_y}" fill="#ffffff" font-size="19" font-weight="800" letter-spacing="0.5">{html.escape(p["title"])}</text>')

    pill_y = title_y + 10
    cat_text = p["cat_pill"]
    parts.append(f'<rect x="{PAD}" y="{pill_y}" width="{W - PAD*2}" height="18" rx="3" fill="rgba(0, 210, 255, 0.12)" stroke="rgba(0, 210, 255, 0.4)" stroke-width="0.8"/>')
    parts.append(f'<text x="{PAD + 8}" y="{pill_y + 13}" fill="{CYAN}" font-size="9" font-weight="700" letter-spacing="0.8">{cat_text}</text>')

    words = p["desc"].split(" ")
    lines = []
    cur = []
    for w in words:
        if sum(len(x) for x in cur) + len(cur) + len(w) > 48:
            lines.append(" ".join(cur))
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(" ".join(cur))

    desc_y = pill_y + 30
    for idx, line in enumerate(lines[:2]):
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

    xp_text = p["xp"]
    xpw = len(xp_text) * 6.5 + 8
    parts.append(f'<rect x="{PAD}" y="{foot_line_y + 6}" width="{xpw:.1f}" height="16" rx="2" fill="rgba(0, 255, 65, 0.15)" stroke="{GREEN}" stroke-width="0.7"/>')
    parts.append(f'<text x="{PAD + xpw/2:.1f}" y="{foot_line_y + 17}" fill="{GREEN}" font-size="9" font-weight="700" text-anchor="middle">{xp_text}</text>')

    parts.append(f'<text x="{PAD + xpw + 10}" y="{foot_line_y + 17}" fill="{MUTED}" font-size="9.5">{html.escape(p["footer_l"])}</text>')

    parts.append(f'<text x="{W-PAD}" y="{foot_line_y + 17}" fill="{GREEN}" font-size="9.5" font-weight="700" text-anchor="end">{html.escape(p["status"])}</text>')

    parts.append('</g></svg>')
    return "".join(parts)

def main():
    for p in PROJECTS:
        svg_content = render_card(p)
        out1 = os.path.join(OUT_DIR, f"card-{p['id']}.svg")
        with open(out1, "w", encoding="utf-8") as f:
            f.write(svg_content)
        if "alt_id" in p:
            out2 = os.path.join(OUT_DIR, f"{p['alt_id']}.svg")
            with open(out2, "w", encoding="utf-8") as f:
                f.write(svg_content)
        print(f"Rendered card for {p['title']}")

if __name__ == "__main__":
    main()
