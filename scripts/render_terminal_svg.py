#!/usr/bin/env python3
"""
Generate an authentic, high-resolution SVG terminal window matching the purple full-width UI.
"""
import os
import html
import xml.etree.ElementTree as ET

W = 880
H = 696
PAD_X = 36
TITLEBAR_H = 36

# Premium Purple Theme Palette
BG_TOP = "#120c22"
BG_BOTTOM = "#090613"
FRAME_BORDER = "#48326d"
HEADER_BORDER = "#281a44"
TITLE_TEXT = "#a998c9"

PROMPT_USER = "#c084fc"
PROMPT_AT = "#7e6c9b"
PROMPT_HOST = "#e9d5ff"
PROMPT_PATH = "#a855f7"
PROMPT_CMD = "#f5f3ff"

HEADER_NAME = "#f3e8ff"
HEADER_ROLE = "#c4b5fd"
HEADER_TYPING = "#a78bfa"

BODY_TEXT = "#e2ddf0"
TEXT_MUTED = "#9d91b8"
KEY_TEXT = "#c084fc"

PROJ_LINK = "#d8b4fe"
PROJ_LINK_HOVER = "#ffffff"
BADGE_DEV = "#e9d5ff"
BADGE_HACK = "#34d399"
BULLET = "#c084fc"

DIVIDER = "#342252"
CURSOR = "#c084fc"

def generate_svg():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace">
<style>
  @keyframes blink {{ 0%, 49% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}
  @keyframes termFadeIn {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  .term-window {{ animation: termFadeIn 0.4s ease-out both; }}
  .cursor {{ animation: blink 1s infinite; fill: {CURSOR}; }}
  .term-text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace; }}
  .prompt-user {{ fill: {PROMPT_USER}; font-weight: 700; }}
  .prompt-at {{ fill: {PROMPT_AT}; }}
  .prompt-host {{ fill: {PROMPT_HOST}; }}
  .prompt-path {{ fill: {PROMPT_PATH}; font-weight: 700; }}
  .prompt-cmd {{ fill: {PROMPT_CMD}; font-weight: 600; }}
  .proj-link {{ fill: {PROJ_LINK}; font-weight: 700; text-decoration: underline; }}
  .proj-link:hover {{ fill: {PROJ_LINK_HOVER}; }}
  .proj-badge {{ fill: {BADGE_DEV}; font-size: 12px; }}
  .desc-txt {{ fill: {TEXT_MUTED}; font-size: 12.5px; }}
  .val-txt {{ fill: {BODY_TEXT}; font-size: 13.5px; }}
  .key-txt {{ fill: {KEY_TEXT}; font-weight: 600; font-size: 13.5px; }}
  .bullet {{ fill: {BULLET}; }}
  @media (prefers-reduced-motion: reduce) {{
    .term-window {{ animation: none !important; opacity: 1 !important; transform: none !important; }}
    .cursor {{ animation: none !important; opacity: 1 !important; }}
    #typingClip rect {{ width: 680px !important; }}
  }}
</style>
<defs>
  <linearGradient id="termBg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="{BG_TOP}" />
    <stop offset="100%" stop-color="{BG_BOTTOM}" />
  </linearGradient>
  <radialGradient id="ambientGlow" cx="20%" cy="10%" r="65%">
    <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.10" />
    <stop offset="100%" stop-color="#8b5cf6" stop-opacity="0" />
  </radialGradient>
  <clipPath id="typingClip">
    <rect x="{PAD_X}" y="127" width="0" height="24">
      <animate attributeName="width" from="0" to="680" dur="2.2s" fill="freeze" begin="0.2s" />
    </rect>
  </clipPath>
</defs>

<!-- Window Frame -->
<g class="term-window">
<rect width="{W}" height="{H}" rx="12" fill="url(#termBg)" />
<rect width="{W}" height="{H}" rx="12" fill="url(#ambientGlow)" />
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{FRAME_BORDER}" stroke-width="1.2" />

<!-- Title Bar -->
<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{HEADER_BORDER}" stroke-width="1" />
<circle cx="20" cy="18" r="5" fill="#ff5f56" />
<circle cx="36" cy="18" r="5" fill="#ffbd2e" />
<circle cx="52" cy="18" r="5" fill="#27c93f" />
<text x="{W / 2}" y="22" fill="{TITLE_TEXT}" font-size="12.5" text-anchor="middle" class="term-text">anirudha@dev: ~ (portfolio)</text>

<g class="term-text">
  <!-- Section 1: whoami -->
  <text x="{PAD_X}" y="68" font-size="14">
    <tspan class="prompt-user">anirudha</tspan><tspan class="prompt-at">@</tspan><tspan class="prompt-host">dev</tspan><tspan class="prompt-path">:~$ </tspan>
    <tspan class="prompt-cmd">whoami</tspan>
  </text>
  <text x="{PAD_X}" y="98" fill="{HEADER_NAME}" font-size="25" font-weight="800" letter-spacing="0.5">Anirudha DG</text>
  <text x="{PAD_X}" y="120" fill="{HEADER_ROLE}" font-size="14" font-weight="500">Student &amp; Developer</text>
  
  <!-- Animated Typing Introduction -->
  <g clip-path="url(#typingClip)">
    <text x="{PAD_X}" y="142" fill="{HEADER_TYPING}" font-size="13.5" font-weight="600">&gt; Exploring Web Application Security Testing &amp; Software Security</text>
  </g>

  <!-- Section 2: cat about.txt -->
  <text x="{PAD_X}" y="178" font-size="14">
    <tspan class="prompt-user">anirudha</tspan><tspan class="prompt-at">@</tspan><tspan class="prompt-host">dev</tspan><tspan class="prompt-path">:~$ </tspan>
    <tspan class="prompt-cmd">cat about.txt</tspan>
  </text>
  <text x="{PAD_X}" y="200" class="val-txt">Student and developer studying software architecture, systems</text>
  <text x="{PAD_X}" y="219" class="val-txt">interaction, and security boundaries. Focused on web application</text>
  <text x="{PAD_X}" y="238" class="val-txt">security, vulnerability research, and exploit mechanics through CTF</text>
  <text x="{PAD_X}" y="257" class="val-txt">challenges, personal projects, and intentionally vulnerable labs.</text>

  <!-- Section 3: ls ~/projects -->
  <text x="{PAD_X}" y="290" font-size="14">
    <tspan class="prompt-user">anirudha</tspan><tspan class="prompt-at">@</tspan><tspan class="prompt-host">dev</tspan><tspan class="prompt-path">:~$ </tspan>
    <tspan class="prompt-cmd">ls ~/projects</tspan>
  </text>
  
  <!-- Project 1: SecureBox -->
  <text x="{PAD_X}" y="312" font-size="14">
    <tspan class="bullet">&#x25b8; </tspan>
    <a href="https://github.com/anirudhadg04/SecureBox" xlink:href="https://github.com/anirudhadg04/SecureBox" target="_blank" class="proj-link">SecureBox</a>
    <tspan class="proj-badge"> [in dev]</tspan>
  </text>
  <text x="{PAD_X + 18}" y="330" class="desc-txt">Client-side document encryption (AES-256-GCM / SHA-256 integrity)</text>

  <!-- Project 2: VerySecureWebsite -->
  <text x="{PAD_X}" y="352" font-size="14">
    <tspan class="bullet">&#x25b8; </tspan>
    <a href="https://github.com/anirudhadg04/VerySecureWebsite" xlink:href="https://github.com/anirudhadg04/VerySecureWebsite" target="_blank" class="proj-link">VerySecureWebsite</a>
    <tspan class="proj-badge"> [in dev]</tspan>
  </text>
  <text x="{PAD_X + 18}" y="370" class="desc-txt">Intentionally vulnerable app for studying BOLA/IDOR, BFLA, XSS &amp; Pytest</text>

  <!-- Project 3: tabzero -->
  <text x="{PAD_X}" y="392" font-size="14">
    <tspan class="bullet">&#x25b8; </tspan>
    <a href="https://github.com/anirudhadg04/tabzero" xlink:href="https://github.com/anirudhadg04/tabzero" target="_blank" class="proj-link">tabzero</a>
    <tspan fill="{BADGE_HACK}" font-size="12px" font-weight="600"> [hackathon]</tspan>
  </text>
  <text x="{PAD_X + 18}" y="410" class="desc-txt">Cross-platform digital wellness tool (Manifest V3 + Android app)</text>

  <!-- Project 4: Vachana -->
  <text x="{PAD_X}" y="432" font-size="14">
    <tspan class="bullet">&#x25b8; </tspan>
    <a href="https://github.com/anirudhadg04" xlink:href="https://github.com/anirudhadg04" target="_blank" class="proj-link">Vachana</a>
    <tspan class="proj-badge"> [in dev]</tspan>
  </text>
  <text x="{PAD_X + 18}" y="450" class="desc-txt">Solo, voice-first computational exploration of Vachana literature</text>

  <!-- Section 4: cat toolkit.txt -->
  <text x="{PAD_X}" y="484" font-size="14">
    <tspan class="prompt-user">anirudha</tspan><tspan class="prompt-at">@</tspan><tspan class="prompt-host">dev</tspan><tspan class="prompt-path">:~$ </tspan>
    <tspan class="prompt-cmd">cat toolkit.txt</tspan>
  </text>
  <text x="{PAD_X}" y="506" font-size="13.5">
    <tspan class="key-txt">Languages:  </tspan><tspan class="val-txt">Python, C, TypeScript, SQL</tspan>
  </text>
  <text x="{PAD_X}" y="526" font-size="13.5">
    <tspan class="key-txt">Security:   </tspan><tspan class="val-txt">Kali Linux, Burp Suite, Wireshark, Nmap, OWASP Top 10</tspan>
  </text>
  <text x="{PAD_X}" y="546" font-size="13.5">
    <tspan class="key-txt">Web &amp; Sys:  </tspan><tspan class="val-txt">Web Crypto API, REST APIs, Linux systems</tspan>
  </text>

  <!-- Section 5: contact list -->
  <text x="{PAD_X}" y="580" font-size="14">
    <tspan class="prompt-user">anirudha</tspan><tspan class="prompt-at">@</tspan><tspan class="prompt-host">dev</tspan><tspan class="prompt-path">:~$ </tspan>
    <tspan class="prompt-cmd">contact --list</tspan>
  </text>
  <text x="{PAD_X}" y="602" font-size="13.5">
    <tspan class="key-txt">GitHub:     </tspan>
    <a href="https://github.com/anirudhadg04" target="_blank" class="proj-link">https://github.com/anirudhadg04</a>
  </text>
  <text x="{PAD_X}" y="622" font-size="13.5">
    <tspan class="key-txt">Email:      </tspan>
    <a href="mailto:anirudhaworks365@gmail.com" class="proj-link">anirudhaworks365@gmail.com</a>
  </text>

  <!-- Bottom Divider Line -->
  <line x1="{PAD_X}" y1="644" x2="{W - PAD_X}" y2="644" stroke="{DIVIDER}" stroke-width="1.2" />

  <!-- Final active prompt without motto -->
  <text x="{PAD_X}" y="668" font-size="14">
    <tspan class="prompt-user">anirudha</tspan><tspan class="prompt-at">@</tspan><tspan class="prompt-host">dev</tspan><tspan class="prompt-path">:~$ </tspan>
    <tspan class="cursor">&#x2588;</tspan>
  </text>

</g>
</g>
</svg>'''

if __name__ == "__main__":
    content = generate_svg()
    ET.fromstring(content)
    out_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(out_dir, "terminal.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("terminal.svg generated and verified successfully at", out_path)
