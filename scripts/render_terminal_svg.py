#!/usr/bin/env python3
"""
Generate an authentic, high-resolution SVG terminal window matching the 'svg-terminal' UI.
"""
import os
import html
import xml.etree.ElementTree as ET

W = 840
H = 620
PAD_X = 26
TITLEBAR_H = 36

# Color scheme inspired by Tokyo Night / Catppuccin / GitHub Dark
BG = "#0d1117"
FRAME_BORDER = "#30363d"
HEADER_BORDER = "#21262d"
MUTED = "#6e7681"
TEXT_DIM = "#8b949e"
TEXT_LIGHT = "#c9d1d9"
TEXT_WHITE = "#f0f6fc"

PROMPT_USER = "#58a6ff"
PROMPT_HOST = "#79c0ff"
CMD_COLOR = "#f0f6fc"
GREEN = "#39d353"
CYAN = "#38bdf8"
YELLOW = "#e3b341"
PURPLE = "#bc8cff"

DOT_COLORS = [
    "#ff5f56", "#ffbd2e", "#27c93f", "#58a6ff",
    "#bc8cff", "#ff79c6", "#39d353", "#79c0ff"
]

PALETTE_BLOCKS = [
    "#ff5f56", "#ffbd2e", "#27c93f", "#58a6ff",
    "#bc8cff", "#ff79c6", "#f1fa8c", "#38bdf8",
    "#39d353", "#f0883e", "#e6edf3", "#6e7681"
]

def generate_svg():
    lines_svg = []
    
    # SVG Header
    lines_svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, \'Liberation Mono\', monospace">'
    )
    
    # CSS Styles & Animations
    lines_svg.append('''<style>
@keyframes blink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: 0; } }
@keyframes termFadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
.term-window { animation: termFadeIn 0.4s ease-out both; }
.cursor { animation: blink 1s infinite; }
@media (prefers-reduced-motion: reduce) {
  .term-window { animation: none !important; opacity: 1 !important; transform: none !important; }
  .cursor { animation: none !important; opacity: 1 !important; }
}
</style>''')

    # Terminal Background and Window Border
    lines_svg.append(f'<g class="term-window">')
    lines_svg.append(f'<rect width="{W}" height="{H}" rx="10" fill="{BG}" />')
    lines_svg.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="none" stroke="{FRAME_BORDER}" stroke-width="1" />')
    
    # Titlebar line
    lines_svg.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{HEADER_BORDER}" stroke-width="1" />')
    
    # Window controls (red, yellow, green)
    lines_svg.append(f'<circle cx="20" cy="{TITLEBAR_H/2}" r="5" fill="#ff5f56" />')
    lines_svg.append(f'<circle cx="36" cy="{TITLEBAR_H/2}" r="5" fill="#ffbd2e" />')
    lines_svg.append(f'<circle cx="52" cy="{TITLEBAR_H/2}" r="5" fill="#27c93f" />')
    
    # Titlebar text
    titlebar_text = "anirudha@terminal &#8212; bash"
    lines_svg.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" text-anchor="middle">{titlebar_text}</text>')
    
    # Content Area
    y = TITLEBAR_H + 26
    LINE_HEIGHT = 19
    
    def draw_prompt(cmd, cur_y):
        return (
            f'<text x="{PAD_X}" y="{cur_y}" font-size="13">'
            f'<tspan fill="{PROMPT_USER}">anirudha</tspan>'
            f'<tspan fill="{MUTED}">@</tspan>'
            f'<tspan fill="{PROMPT_HOST}">github</tspan>'
            f'<tspan fill="{MUTED}">:~$ </tspan>'
            f'<tspan fill="{CMD_COLOR}">{html.escape(cmd)}</tspan>'
            f'</text>'
        )

    # Command 1: cat /etc/motd
    lines_svg.append(draw_prompt("cat /etc/motd", y))
    y += LINE_HEIGHT + 3
    
    # ASCII Box
    box_w = 788
    lines_svg.append(f'<rect x="{PAD_X}" y="{y}" width="{box_w}" height="48" rx="4" fill="#161b22" stroke="{MUTED}" stroke-dasharray="4 4" stroke-width="0.8" />')
    lines_svg.append(f'<text x="{PAD_X + 16}" y="{y + 20}" fill="{TEXT_WHITE}" font-size="13" font-weight="700">ANIRUDHA DG (@anirudhadg04)</text>')
    lines_svg.append(f'<text x="{PAD_X + 16}" y="{y + 37}" fill="{TEXT_DIM}" font-size="12">Student &amp; Developer &#183; Exploring Web Application Security Testing &amp; Software Security</text>')
    y += 48 + LINE_HEIGHT + 6
    
    # Command 2: neofetch --distro anirudha
    lines_svg.append(draw_prompt("neofetch --distro anirudha", y))
    y += LINE_HEIGHT + 2
    
    lines_svg.append(f'<text x="{PAD_X}" y="{y}" fill="{GREEN}" font-size="13" font-weight="700">dev@github</text>')
    y += 14
    lines_svg.append(f'<text x="{PAD_X}" y="{y}" fill="{FRAME_BORDER}" font-size="12">----------</text>')
    y += LINE_HEIGHT
    
    fields = [
        ("Role", "Student & Developer"),
        ("Focus", "Web Application Security Testing"),
        ("Practice", "CTF Challenges & Security Lab Methodologies"),
        ("Languages", "Python, C / C++, TypeScript, SQL"),
        ("Security", "Burp Suite, Wireshark, Nmap, Kali Linux"),
        ("Frameworks", "OWASP Top 10 Methodology, Web Crypto API"),
        ("Contact", "anirudhaworks365@gmail.com")
    ]
    
    for label, val in fields:
        lbl_str = f"{label}:"
        lines_svg.append(
            f'<text x="{PAD_X}" y="{y}" font-size="12.5">'
            f'<tspan fill="{CYAN}" font-weight="700">{lbl_str:<13}</tspan>'
            f'<tspan fill="{TEXT_LIGHT}"> {html.escape(val)}</tspan>'
            f'</text>'
        )
        y += LINE_HEIGHT - 1
        
    y += 6
    
    # Palette dots separator (matching screenshot)
    for i, col in enumerate(DOT_COLORS):
        cx = PAD_X + 6 + i * 20
        lines_svg.append(f'<circle cx="{cx}" cy="{y}" r="4" fill="{col}" />')
    y += LINE_HEIGHT + 4
    
    # Command 3: ./projects.sh --list
    lines_svg.append(draw_prompt("./projects.sh --list", y))
    y += LINE_HEIGHT + 2
    
    projects = [
        {
            "name": "SecureBox",
            "badge": "[in development]",
            "badge_color": YELLOW,
            "desc": "Client-side document encryption &amp; archive containers using Web Crypto AES-256-GCM &amp; SHA-256.",
            "url": "https://github.com/anirudhadg04/SecureBox"
        },
        {
            "name": "VerySecureWebsite",
            "badge": "[in development]",
            "badge_color": YELLOW,
            "desc": "Intentionally vulnerable educational lab for learning AppSec (BOLA/IDOR, BFLA, XSS) with Pytest.",
            "url": "https://github.com/anirudhadg04/VerySecureWebsite"
        },
        {
            "name": "tabzero",
            "badge": "[hackathon]",
            "badge_color": GREEN,
            "desc": "Digital wellness ecosystem built with @NyNehalJois (Manifest V3 Extension + Android App).",
            "url": "https://github.com/anirudhadg04/tabzero"
        },
        {
            "name": "Vachana",
            "badge": "[in development]",
            "badge_color": PURPLE,
            "desc": "Solo, voice-first exploration connected to Vachana literature.",
            "url": None
        }
    ]
    
    for p in projects:
        url_text = f' <tspan fill="{MUTED}">({p["url"]})</tspan>' if p["url"] else ''
        lines_svg.append(
            f'<text x="{PAD_X}" y="{y}" font-size="12.5">'
            f'<tspan fill="{GREEN}">&#x25b8; </tspan>'
            f'<tspan fill="{TEXT_WHITE}" font-weight="700">{html.escape(p["name"])} </tspan>'
            f'<tspan fill="{p["badge_color"]}">{html.escape(p["badge"])}</tspan>'
            f'{url_text}'
            f'</text>'
        )
        y += 16
        lines_svg.append(
            f'<text x="{PAD_X + 16}" y="{y}" fill="{TEXT_DIM}" font-size="11.5">'
            f'{p["desc"]}'
            f'</text>'
        )
        y += LINE_HEIGHT + 2
        
    y += 2
    
    # Command 4: palette
    lines_svg.append(draw_prompt("palette", y))
    y += LINE_HEIGHT - 1
    
    lines_svg.append(f'<text x="{PAD_X}" y="{y}" fill="{MUTED}" font-size="12">theme: </text>')
    swatch_x = PAD_X + 54
    for col in PALETTE_BLOCKS:
        lines_svg.append(f'<rect x="{swatch_x}" y="{y - 10}" width="16" height="12" rx="2" fill="{col}" />')
        swatch_x += 20
        
    y += LINE_HEIGHT + 8
    
    # Final active prompt with blinking cursor
    lines_svg.append(
        f'<text x="{PAD_X}" y="{y}" font-size="13">'
        f'<tspan fill="{PROMPT_USER}">anirudha</tspan>'
        f'<tspan fill="{MUTED}">@</tspan>'
        f'<tspan fill="{PROMPT_HOST}">github</tspan>'
        f'<tspan fill="{MUTED}">:~$ </tspan>'
        f'<tspan fill="{GREEN}" class="cursor">&#x2588;</tspan>'
        f'</text>'
    )
    
    lines_svg.append('</g></svg>')
    return "".join(lines_svg)

if __name__ == "__main__":
    content = generate_svg()
    ET.fromstring(content)
    out_dir = os.path.dirname(__file__)
    out_path = os.path.join(out_dir, "terminal.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("terminal.svg generated and verified successfully!")
