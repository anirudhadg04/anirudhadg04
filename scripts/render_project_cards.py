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
        "title": "SecureBox",
        "cmd": "cat ~/projects/securebox.ts",
        "badge": "CRYPTOGRAPHY & SECURITY",
        "badge_color": "#39d353",
        "badge_bg": "rgba(57, 211, 83, 0.15)",
        "desc": "Privacy-first client-side document & archive protection. Native Web Crypto AES-256-GCM encryption with AAD-bound binary envelopes & SHA-256 integrity verification.",
        "tags": ["AES-256-GCM", "Web Crypto API", "TypeScript", "JSZip", "49 Tests"],
        "footer_l": "Zero Unencrypted Disk Artifacts",
        "footer_r": "v2.0 Archive Format"
    },
    {
        "id": "appsec",
        "title": "VerySecureWebsite",
        "cmd": "cat ~/projects/appsec.py",
        "badge": "APPLICATION SECURITY LAB",
        "badge_color": "#ff7b72",
        "badge_bg": "rgba(255, 123, 114, 0.15)",
        "desc": "Educational security research laboratory and vulnerability testbed demonstrating practical exploit mechanics and automated verification for BOLA/IDOR, BFLA, and XSS.",
        "tags": ["Python", "Flask", "Pytest", "AppSec", "BOLA/IDOR", "XSS Labs"],
        "footer_l": "Automated Pytest Verifiers",
        "footer_r": "Security Research"
    },
    {
        "id": "cyberlabs",
        "title": "CyberLabs",
        "cmd": "cat ~/projects/cyberlabs.sh",
        "badge": "OFFENSIVE SECURITY",
        "badge_color": "#f2cc60",
        "badge_bg": "rgba(242, 204, 96, 0.15)",
        "desc": "Hands-on offensive security research repository tracking practical exploitation, web vulnerabilities, and network penetration testing across PortSwigger and Bandit.",
        "tags": ["PortSwigger Labs", "Bandit OTW", "Burp Suite", "Web Pentesting"],
        "footer_l": "Web Security & Network Labs",
        "footer_r": "Security Research"
    },
    {
        "id": "tabzero",
        "title": "tabzero.",
        "cmd": "cat ~/projects/tabzero.kt",
        "badge": "MINDFUL TECH & ATTENTION",
        "badge_color": "#22d3ee",
        "badge_bg": "rgba(34, 211, 238, 0.15)",
        "desc": "Mindful digital living ecosystem. Cross-platform extension & native Android APK replacing infinite scrolling with calm nature sanctuaries and dynamic weather focus nudges.",
        "tags": ["Android APK", "Chrome / Firefox", "Local-First", "Focus Engine"],
        "footer_l": "v1.0.2 Public Release",
        "footer_r": "100% Offline & Private"
    }
]

W = 410
H = 260
TITLEBAR_H = 34
PAD = 20
BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
TEXT = "#e6edf3"
DESC_COLOR = "#8b949e"

def render_card(p):
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        '<style>',
        '@keyframes cardIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }',
        '.card { animation: cardIn 0.5s ease-out both; }',
        '@media (prefers-reduced-motion: reduce) { .card { animation: none !important; opacity: 1 !important; transform: none !important; } }',
        '</style>',
        f'<defs><linearGradient id="cbg_{p["id"]}" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
        f'<g class="card">',
        f'<rect width="{W}" height="{H}" rx="12" fill="url(#cbg_{p["id"]})"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
    ]

    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*14}" cy="{TITLEBAR_H/2}" r="4.5" fill="{dotcol}"/>')
    parts.append(f'<text x="{PAD + 52}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="11">{html.escape(p["cmd"])}</text>')

    badge_text = p["badge"]
    badge_w = len(badge_text) * 6.5 + 14
    badge_x = W - PAD - badge_w
    parts.append(f'<rect x="{badge_x:.1f}" y="{TITLEBAR_H + 14}" width="{badge_w:.1f}" height="20" rx="4" fill="{p["badge_bg"]}"/>')
    parts.append(f'<text x="{badge_x + badge_w/2:.1f}" y="{TITLEBAR_H + 28}" fill="{p["badge_color"]}" font-size="9" font-weight="700" text-anchor="middle">{badge_text}</text>')

    parts.append(f'<text x="{PAD}" y="{TITLEBAR_H + 30}" fill="{TEXT}" font-size="18" font-weight="700">{html.escape(p["title"])}</text>')

    words = p["desc"].split(" ")
    lines = []
    cur = []
    for w in words:
        if sum(len(x) for x in cur) + len(cur) + len(w) > 46:
            lines.append(" ".join(cur))
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(" ".join(cur))

    desc_y = TITLEBAR_H + 56
    for idx, line in enumerate(lines[:3]):
        parts.append(f'<text x="{PAD}" y="{desc_y + idx*18}" fill="{DESC_COLOR}" font-size="11.5">{html.escape(line)}</text>')

    tag_y = H - 56
    cur_tag_x = PAD
    for tag in p["tags"][:4]:
        tw = len(tag) * 6.8 + 12
        parts.append(f'<rect x="{cur_tag_x:.1f}" y="{tag_y}" width="{tw:.1f}" height="20" rx="4" fill="#161b22" stroke="{FRAME}" stroke-width="0.8"/>')
        parts.append(f'<text x="{cur_tag_x + tw/2:.1f}" y="{tag_y + 14}" fill="{TEXT}" font-size="10" text-anchor="middle">{html.escape(tag)}</text>')
        cur_tag_x += tw + 6

    foot_y = H - 16
    parts.append(f'<line x1="{PAD}" y1="{H-32}" x2="{W-PAD}" y2="{H-32}" stroke="{FRAME}" stroke-opacity="0.4"/>')
    parts.append(f'<text x="{PAD}" y="{foot_y}" fill="{MUTED}" font-size="10">{html.escape(p["footer_l"])}</text>')
    parts.append(f'<text x="{W-PAD}" y="{foot_y}" fill="{p["badge_color"]}" font-size="10" font-weight="600" text-anchor="end">{html.escape(p["footer_r"])}</text>')

    parts.append('</g></svg>')
    return "".join(parts)

def main():
    for p in PROJECTS:
        card_svg = render_card(p)
        out_file = os.path.join(OUT_DIR, f"card-{p['id']}.svg")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(card_svg)
        print(f"Rendered {out_file}")

if __name__ == "__main__":
    main()
