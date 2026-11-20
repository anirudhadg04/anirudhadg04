#!/usr/bin/env python3
"""
Convert the prepped photo into a monochrome ASCII-art SVG that scans & types
itself in like a Linux terminal session, ending with a live blinking cursor.
"""
from PIL import Image, ImageEnhance
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-prepped.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "anirudha-ascii.svg")

W, H = 840, 880
PAD = 20
TITLEBAR_H = 34
STATUS_H = 36
ART_W = 800
ART_H = H - TITLEBAR_H - STATUS_H - PAD * 2

COLS = 120
ROWS = 62
CELL_W = ART_W / COLS
CELL_H = ART_H / ROWS

RAMP = " .`:-=+*#%@"

im = Image.open(SRC).convert("L")
im = ImageEnhance.Contrast(im).enhance(1.45)
im = ImageEnhance.Brightness(im).enhance(1.02)
im = im.resize((COLS, ROWS), Image.Resampling.LANCZOS)
px = im.load()

WHITE_FLOOR = 0.86
GAMMA = 1.15

rows_txt = []
for y in range(ROWS):
    chars = []
    for x in range(COLS):
        lum = px[x, y] / 255.0
        lum = pow(lum, GAMMA)
        if lum >= WHITE_FLOOR:
            chars.append(" ")
            continue
        idx = int((1.0 - lum) * (len(RAMP) - 1) + 0.5)
        idx = max(0, min(len(RAMP) - 1, idx))
        chars.append(RAMP[idx])
    rows_txt.append("".join(chars))

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"
INK = "#58a6ff"
CURSOR = "#58a6ff"

ROW_DUR = 4.0 / ROWS
STAGGER = ROW_DUR

parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">'
)
parts.append('<defs>'
             f'<linearGradient id="abg" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
             f'</linearGradient></defs>')

parts.append(f'<rect width="{W}" height="{H}" rx="12" fill="url(#abg)"/>')
parts.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>')

parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>')
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" text-anchor="middle">anirudhadg04@github: ~$ ./portrait.sh</text>')

art_top = TITLEBAR_H + PAD
font_size = CELL_H * 0.90

for ry, line in enumerate(rows_txt):
    y = art_top + ry * CELL_H + CELL_H * 0.76
    row_y = art_top + ry * CELL_H
    delay = ry * STAGGER
    safe = html.escape(line)
    text = (f'<text xml:space="preserve" x="{PAD}" y="{y:.1f}" fill="{INK}" '
            f'font-size="{font_size:.1f}" textLength="{ART_W:.1f}" lengthAdjust="spacing">{safe}</text>')

    parts.append(
        f'<clipPath id="ar{ry}"><rect x="{PAD}" y="{row_y:.1f}" height="{CELL_H:.2f}" width="0">'
        f'<animate attributeName="width" from="0" to="{ART_W:.1f}" begin="{delay:.3f}s" '
        f'dur="{ROW_DUR:.2f}s" fill="freeze"/></rect></clipPath>'
    )
    parts.append(f'<g clip-path="url(#ar{ry})">{text}</g>')
    parts.append(
        f'<rect y="{row_y+1:.1f}" width="{CELL_W:.1f}" height="{CELL_H-2:.1f}" fill="{CURSOR}" opacity="0">'
        f'<animate attributeName="x" from="{PAD}" to="{PAD+ART_W:.1f}" begin="{delay:.3f}s" dur="{ROW_DUR:.2f}s" fill="freeze"/>'
        f'<set attributeName="opacity" to="0.85" begin="{delay:.3f}s"/>'
        f'<set attributeName="opacity" to="0" begin="{delay+ROW_DUR:.3f}s"/></rect>'
    )

status_line_y = H - STATUS_H - PAD * 0.5
status_y = status_line_y + 22
parts.append(f'<line x1="0" y1="{status_line_y:.1f}" x2="{W}" y2="{status_line_y:.1f}" stroke="{FRAME}"/>')
parts.append(f'<text x="{PAD}" y="{status_y:.1f}" fill="{TITLE_TEXT}" font-size="13">'
             f'anirudhadg04@github:~$ whoami <tspan fill="#e6edf3" font-weight="700">Anirudha DG</tspan></text>')

cursor_x = PAD + len("anirudhadg04@github:~$ whoami Anirudha DG ") * 8
parts.append(f'<rect x="{cursor_x:.1f}" y="{status_y-13:.1f}" width="8" height="15" fill="#39d353">'
             f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/></rect>')

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print("Wrote SVG:", OUT, len(svg), "bytes (840x880)")
