"""Case 26, The Winning Ticket: hand-painted colour plates for the detailed colour version (art_color.py 26).
Same coordinates as art_case26.py; the village-green summer fair is painted (sky, hedges, grass, bunting, striped tea
stall, wicker hamper). The anonymous queue figures stay faceless and IDENTICAL (one soft slate colour) so the picture
never tells who stood where."""
import math
import dkit
from dkit import C, PAL, shade, mix, K, Wt
import bwkit as B

SKY = C(196, 224, 240); SKY2 = C(244, 236, 214); GRASS = C(156, 196, 120); GRASS2 = C(132, 176, 100); HEDGE = C(96, 144, 86)
STRIPE = C(226, 110, 104); CANVAS = C(252, 246, 232); WICKER = C(214, 170, 104); WICKER_DK = C(160, 118, 64); ANON = C(170, 182, 198)
BUNT = [C(228, 122, 112), C(246, 206, 112), C(130, 178, 212), C(152, 198, 142), C(238, 168, 190)]

def green(k, w, h, y=60):
    k.vgrad(14, y, w - 14, h - 14, SKY, SKY2, steps=10)
    for cx, cy, r in ((70, y + 12, 40), (150, y + 8, 34), (360, y + 10, 44), (460, y + 6, 36)): k.circle(cx, cy, r, lw=0.6, fill=HEDGE)
    k.vgrad(14, 14, w - 14, y, GRASS2, GRASS, steps=6); k.line([(14, y), (w - 14, y)], lw=0.9, amp=0.1)
    for i in range(40): k.line([(20 + i * 12, 20 + (i * 7) % 30), (22 + i * 12, 26 + (i * 7) % 30)], lw=0.4, amp=0, color=GRASS2)

def bunting(k, w, y=340):
    for i in range(9):
        k.shape([(30 + i * 52, y), (56 + i * 52, y - 18), (82 + i * 52, y)], lw=0.6, fill=BUNT[i % 5], amp=0.2)
    k.line([(14, y), (w - 14, y)], lw=0.6, amp=0.3)

def _ticket(k, x, y, s, ang=0, num=True):
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a); R = lambda u, v: (x + u * ca - v * sa, y + u * sa + v * ca)
    pts = [R(-s / 2, -s * 0.25), R(s / 2, -s * 0.25), R(s / 2, s * 0.25), R(-s / 2, s * 0.25)]
    k.shape(pts, lw=0.9, fill=C(250, 214, 120), amp=0); k.line([R(s * 0.22, -s * 0.25), R(s * 0.22, s * 0.25)], lw=0.4, amp=0)
    if num: k.text(*R(-s * 0.12, -s * 0.06), "No. 47", size=max(5, s * 0.16), font="Ink-Plex", color=C(150, 50, 44))

def _hamper(k, x, y, w):
    h = w * 0.55; k.rect(x - w / 2, y, w, h, lw=1.3, fill=WICKER)
    for j in range(1, 6): k.line([(x - w / 2, y + j * h / 6), (x + w / 2, y + j * h / 6)], lw=0.4, amp=0.1, color=WICKER_DK)
    for j in range(1, 10): k.line([(x - w / 2 + j * w / 10, y), (x - w / 2 + j * w / 10, y + h)], lw=0.3, amp=0.1, color=WICKER_DK)
    k.shape(k.arcpts(x, y + h, w * 0.4, h * 0.5, 0, 180, 18), lw=2.0, fill=None, amp=0)
    k.shape([(x - w * 0.12, y + h * 0.35), (x + w * 0.12, y + h * 0.35), (x, y + h * 0.62)], lw=0.8, fill=C(200, 60, 70), amp=0)   # ribbon bow

def _anon(k, x, y, h):
    with k.tint(ANON, hatch=shade(ANON, 0.8)):
        k.circle(x, y + h * 0.86, h * 0.11, lw=0.9, fill=Wt)
        k.shape([(x - h * 0.13, y + h * 0.18), (x + h * 0.13, y + h * 0.18), (x + h * 0.09, y + h * 0.72), (x - h * 0.09, y + h * 0.72)], lw=0.9, fill=Wt, amp=0)
    for lx in (-0.05, 0.05): k.line([(x + h * lx, y + h * 0.18), (x + h * lx, y)], lw=1.2, amp=0, color=shade(ANON, 0.6))

def _stall(k, x, y, w):
    k.rect(x, y, w, 70, lw=1.2, fill=C(186, 140, 96)); k.text(x + w / 2, y + 30, "TEAS", size=14, font="Ink-Plex", color=CANVAS)
    k.shape([(x - 10, y + 130), (x + w + 10, y + 130), (x + w, y + 110), (x, y + 110)], lw=1.0, fill=CANVAS, amp=0)
    for j in range(5):
        if j % 2 == 0:
            u0, u1 = j / 5, (j + 1) / 5
            k.shape([(x + w * u0, y + 110), (x + w * u1, y + 110), (x - 10 + (w + 20) * u1, y + 130), (x - 10 + (w + 20) * u0, y + 130)], lw=0, fill=STRIPE, stroke=False, amp=0)
    k.line([(x + 4, y + 70), (x + 4, y + 110)], lw=1.4, amp=0, color=C(120, 86, 60)); k.line([(x + w - 4, y + 70), (x + w - 4, y + 110)], lw=1.4, amp=0, color=C(120, 86, 60))
    with k.tint(PAL.teapot): k.teapot(x + w * 0.3, y + 70, 22)

import art_case26 as _A
QX = _A.QX

def hook_plate(k, w, h):
    B.full_open(k, w, h); green(k, w, h); bunting(k, w); _stall(k, 20, 60, 80); [k.anon(x, 60, 110) for x in QX]; k.big_hamper(440, 60, 90); k.unclip()
def fair_plate(k, w, h):
    B.plate_open(k, w, h); green(k, w, h); bunting(k, w)
    k.rect(226, 290, 160, 24, lw=0.8, fill=CANVAS); k.text(306, 298, "SUMMER FAIR \u00b7 RAFFLE", size=12, font="Ink-Plex", color=C(150, 50, 44)); k.unclip()
def queue_plate(k, w, h):
    B.plate_open(k, w, h); green(k, w, h); bunting(k, w); _stall(k, 20, 60, 80)
    for x in QX: k.anon(x, 60, 120)
    k.text(240, 30, "5 people, one behind the other", size=10, font="Ink-Kalam", color=PAL.navy); k.unclip()
def clues_plate(k, w, h): B.plate_open(k, w, h); green(k, w, h); bunting(k, w); _stall(k, 300, 60, 180); k.unclip()
def conf_plate(k, w, h): B.plate_open(k, w, h); green(k, w, h); bunting(k, w); _stall(k, 360, 60, 130); k.unclip()
def _p(k, pw, h):
    green(k, pw, h, y=50); _stall(k, 300, 50, 160)

def apply(A):
    B.InkBW.ticket = _ticket; B.InkBW.big_hamper = _hamper; B.InkBW.anon = _anon; A._stall = _stall
    A.hook_plate, A.fair_plate, A.queue_plate, A.clues_plate, A.conf_plate = hook_plate, fair_plate, queue_plate, clues_plate, conf_plate
    A.lineup_plate = B.lineup_plate_fn([_p, _p, _p, _p], [n for n, _ in A.CAST])
