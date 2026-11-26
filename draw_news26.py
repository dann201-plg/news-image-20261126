"""Draw the 26 November 2026 news image (make.fun news-image-20261126).

One-page newspaper front page: 40 verified stories, PIL text and layout,
three AI editorial-illustration heroes saved as repo assets and composited
here, charts and the map drawn by the program. Deterministic: same input
bytes in, same PNG bytes out.
"""

import json
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
CREAM = (248, 242, 228)
PAPER = (255, 252, 244)
NAVY = (22, 38, 78)
NAVY_LIGHT = (52, 72, 120)
GOLD = (194, 154, 43)
GOLD_LIGHT = (232, 205, 120)
RED = (169, 40, 45)
INK = (28, 28, 28)
GREY = (96, 96, 96)
LINE = (200, 190, 165)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF_I = "DejaVuSerif-Italic.ttf"


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, fnt, max_w):
    """Truncate with an ellipsis so the text fits max_w."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    ell = "\u2026"
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if draw.textlength(text[:mid] + ell, font=fnt) <= max_w:
            lo = mid
        else:
            hi = mid - 1
    return text[:lo].rstrip() + ell


def section_label(draw, x, y, text):
    draw.text((x, y), text, font=font(SERIF_B, 13), fill=NAVY)
    draw.line([(x, y + 19), (x + 52, y + 19)], fill=GOLD, width=3)


def draw_header(draw, data):
    draw.rectangle([0, 0, W, 88], fill=NAVY)
    draw.text((24, 10), "THE WORLD ON ONE PAGE", font=font(SERIF_B, 12),
              fill=GOLD_LIGHT)
    draw.text((24, 26), data["date_long"].upper(), font=font(SERIF_B, 36),
              fill=(255, 255, 255))
    draw.text((24, 66), data["subtitle"], font=font(SERIF, 12),
              fill=(205, 210, 225))
    badge = "40 STORIES"
    bw = int(draw.textlength(badge, font=font(SERIF_B, 16))) + 28
    draw.rounded_rectangle([W - 24 - bw, 26, W - 24, 62], radius=18,
                           fill=GOLD)
    draw.text((W - 24 - bw + 14, 35), badge, font=font(SERIF_B, 16),
              fill=NAVY)


def draw_main(draw, data):
    img = Image.open(os.path.join(ASSETS, "hero-tariffs.png")).convert("RGB")
    img = ImageOps.fit(img, (470, 196), Image.LANCZOS)
    canvas.paste(img, (24, 98))
    draw.rectangle([24, 98, 494, 294], outline=NAVY, width=2)

    x = 512
    draw.text((x, 96), "MAIN STORY", font=font(SERIF_B, 12), fill=RED)
    head = data["main"]["headline"]
    lines = wrap(draw, head, font(SERIF_B, 27), 488)
    y = 116
    for line in lines:
        draw.text((x, y), line, font=font(SERIF_B, 27), fill=NAVY)
        y += 33
    sub = data["main"]["subhead"]
    lines = wrap(draw, sub, font(SERIF, 14), 488)
    y += 4
    for line in lines:
        draw.text((x, y), line, font=font(SERIF, 14), fill=INK)
        y += 19
    # Small program-drawn tariff bar: China up to 20%, 14 partners.
    cy = 252
    draw.text((x, cy), "PROPOSED TARIFFS", font=font(SERIF_B, 11),
              fill=GREY)
    draw.rectangle([x, cy + 18, x + 300, cy + 34], outline=GREY, width=1)
    draw.rectangle([x, cy + 18, x + 240, cy + 34], fill=RED)
    draw.text((x + 310, cy + 16), "CHINA UP TO 20%", font=font(SERIF_B, 13),
              fill=RED)
    for i in range(14):
        dx = x + i * 13
        draw.ellipse([dx, cy + 42, dx + 8, cy + 50], fill=GOLD)
    draw.text((x + 190, cy + 40), "14 PARTNERS", font=font(SERIF_B, 11),
              fill=NAVY)


def pictogram_nikkei(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=NAVY)
    pts = [(x0 + 14, y1 - 22), (x0 + 55, y1 - 48), (x0 + 95, y1 - 38),
           (x0 + 135, y1 - 66), (x0 + 175, y1 - 58), (x0 + 215, y1 - 92)]
    draw.line(pts, fill=GOLD_LIGHT, width=4, joint="curve")
    draw.ellipse([pts[-1][0] - 6, pts[-1][1] - 6, pts[-1][0] + 6,
                  pts[-1][1] + 6], fill=RED)
    draw.line([(x0 + 14, y1 - 14), (x1 - 14, y1 - 14)], fill=(255, 255, 255),
              width=2)


def pictogram_kim(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(232, 222, 196))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for r, col in ((52, NAVY_LIGHT), (38, NAVY), (24, GOLD)):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=3)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED)
    for ang in (0, 60, 120):
        import math
        a = math.radians(ang)
        x2 = cx + int(52 * math.cos(a))
        y2 = cy + int(52 * math.sin(a))
        draw.line([(cx, cy), (x2, y2)], fill=GOLD, width=2)


def draw_featured(draw, data):
    section_label(draw, 24, 308, "FOUR TO WATCH")
    cards = data["featured"]
    cw, gap = 238, 8
    for i, card in enumerate(cards):
        x = 24 + i * (cw + gap)
        y = 330
        box = (x, y, x + cw, y + 118)
        if i == 0:
            img = Image.open(os.path.join(ASSETS, "hero-bok.png")).convert("RGB")
            img = ImageOps.fit(img, (cw, 118), Image.LANCZOS)
            canvas.paste(img, (x, y))
        elif i == 1:
            pictogram_nikkei(draw, box)
        elif i == 2:
            img = Image.open(os.path.join(ASSETS, "hero-macys.png")).convert("RGB")
            img = ImageOps.fit(img, (cw, 118), Image.LANCZOS)
            canvas.paste(img, (x, y))
        else:
            pictogram_kim(draw, box)
        draw.rectangle(box, outline=NAVY, width=1)
        ty = y + 128
        lines = wrap(draw, card["headline"], font(SERIF_B, 15), cw)[:3]
        for line in lines:
            draw.text((x, ty), line, font=font(SERIF_B, 15), fill=NAVY)
            ty += 19
        sub_f = font(SERIF, 11)
        lines = wrap(draw, card["subhead"], sub_f, cw)
        if len(lines) > 2:
            lines = lines[:2]
            lines[1] = fit(draw, lines[1], sub_f, cw)
        for line in lines:
            draw.text((x, ty), line, font=sub_f, fill=INK)
            ty += 14


def draw_numbers(draw):
    section_label(draw, 24, 540, "THE DAY IN NUMBERS")
    items = [
        ("14", "TARIFF PARTNERS"),
        ("3.25%", "BANK OF KOREA RATE"),
        ("+1.3%", "NIKKEI REBOUND"),
        ("31", "DEAD IN CAIRO FIRE"),
        ("100,000", "UK VETERANS WARNED"),
        ("18 YRS", "SINCE 26/11 MUMBAI"),
    ]
    cw = 976 // 6
    for i, (val, lab) in enumerate(items):
        x = 24 + i * cw
        draw.text((x, 564), val, font=font(SERIF_B, 24), fill=RED)
        for j, ln in enumerate(wrap(draw, lab, font(SERIF_B, 10), cw - 8)):
            draw.text((x, 592 + j * 12), ln, font=font(SERIF_B, 10),
                      fill=GREY)
        if i:
            draw.line([(x - 8, 564), (x - 8, 612)], fill=LINE, width=1)


def draw_map(draw):
    section_label(draw, 24, 624, "WHERE IT HAPPENED")
    x0, y0, x1, y1 = 24, 646, 504, 716
    draw.rectangle([x0, y0, x1, y1], fill=PAPER, outline=LINE, width=1)
    blobs = [
        [(36, 664), (80, 650), (120, 658), (112, 682), (76, 692),
         (48, 686)],
        [(98, 694), (116, 692), (124, 706), (108, 714), (96, 704)],
        [(238, 658), (264, 652), (278, 664), (258, 676), (240, 670)],
        [(244, 680), (272, 676), (284, 692), (266, 710), (248, 698)],
        [(288, 650), (356, 646), (398, 658), (394, 682), (348, 688),
         (310, 680), (286, 664)],
        [(376, 696), (406, 694), (410, 706), (380, 710)],
    ]
    for blob in blobs:
        draw.polygon(blob, fill=(214, 206, 184))
    dots = [
        (62, 672), (100, 668), (244, 660), (264, 688), (316, 676),
        (364, 654), (372, 660), (388, 662),
    ]
    for dx, dy in dots:
        draw.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=GOLD,
                     outline=NAVY, width=1)


def draw_timeline(draw):
    section_label(draw, 520, 624, "THE DAY IN UTC \u2014 WIB")
    rows = [
        ("02:00 WIB", "UCL kick-off \u2014 20:00 CET Wed"),
        ("04:00 WIB", "Dow closes, erasing 1,100-pt plunge"),
        ("08:15 WIB", "Yoon perjury ruling due in Seoul"),
        ("NOON LONDON", "Tube strike begins"),
        ("19:11 WIB", "Progress 97 cargo docking due at ISS"),
    ]
    y = 648
    for t, ev in rows:
        draw.text((520, y), t, font=font(SERIF_B, 12), fill=NAVY)
        draw.text((620, y), fit(draw, ev, font(SERIF, 12), 380),
                  font=font(SERIF, 12), fill=INK)
        y += 14


def draw_one_liners(draw, data):
    section_label(draw, 24, 726, "THE REST OF THE DAY \u2014 35 STORIES")
    items = data["one_liners"]
    cols = [items[0:12], items[12:24], items[24:35]]
    tag_f = font(SERIF_B, 13)
    txt_f = font(SERIF, 13)
    for ci, col in enumerate(cols):
        x = 24 + ci * 331
        y = 746
        for it in col:
            tag = it["tag"] + " \u00b7 "
            tw = draw.textlength(tag, font=tag_f)
            draw.text((x, y), tag, font=tag_f, fill=NAVY)
            rest = fit(draw, it["headline"], txt_f, 313 - tw)
            draw.text((x + tw, y), rest, font=txt_f, fill=INK)
            y += 13.5


def draw_footer(draw, data):
    y = 916
    draw.line([(24, y - 4), (1000, y - 4)], fill=NAVY, width=2)
    draw.text((24, y), "40 STORIES \u00b7 8 REGIONS \u00b7 12 FIELDS",
              font=font(SERIF_B, 13), fill=NAVY)
    pt = "PRESS TIME 02:00 UTC 26 NOV"
    draw.text((1000 - draw.textlength(pt, font=font(SERIF_B, 11)), y + 2),
              pt, font=font(SERIF_B, 11), fill=GREY)
    draw.text((24, y + 20),
              "Scenes are drawn illustrations, not photographs.",
              font=font(SERIF, 11), fill=GREY)
    dc = ("DATE CHECK \u2014 Left out: Houthi Ras Tanura claim 16:59 UTC "
          "25 Nov (23:59 WIB, 1 min before 26 Nov); Shenzhou-24/Tiangong "
          "(24\u201325 Nov); Colombia peace 10 yrs (24 Nov); BepiColombo "
          "(21/25 Nov); Huang reinstatement (24 Nov); Huawei verdict "
          "(25 Nov); Kospi plunge (25 Nov). Macy's postponement announced "
          "Wed 25 Nov \u2014 the storm hits NYC Thu 26 Nov. UCL kicked off "
          "20:00 CET Wed = 02:00 WIB Thu; US evening news after 00:00 WIB "
          "Thu. Yoon ruling preview only \u2014 outcome not verified. "
          "Progress 97 docking due 19:11 WIB, not yet docked.")
    box = (24, 952, 1000, 1020)
    draw.rectangle(box, outline=RED, width=2)
    lines = wrap(draw, dc, font(SERIF, 11), 952)[:4]
    ly = 956
    for line in lines:
        draw.text((32, ly), line, font=font(SERIF, 11), fill=INK)
        ly += 15


def build():
    global canvas
    with open(os.path.join(HERE, "stories-20261126.json")) as fh:
        data = json.load(fh)
    canvas = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(canvas)
    draw_header(draw, data)
    draw_main(draw, data)
    draw_featured(draw, data)
    draw_numbers(draw)
    draw_map(draw)
    draw_timeline(draw)
    draw_one_liners(draw, data)
    draw_footer(draw, data)
    out = os.path.join(HERE, "entry.png")
    canvas.save(out, format="PNG")
    return out


if __name__ == "__main__":
    print(build())
