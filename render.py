"""
Up2YOU – Bilancio di Sostenibilità – YouTube B2B Ad
30 s · 30 fps · 1280×720 (upscaled to 1920×1080 by FFmpeg)
Fast Python (Pillow) + FFmpeg renderer
"""

import os, math, subprocess, shutil
from PIL import Image, ImageDraw, ImageFont

FA_PATH = "/usr/share/fonts/truetype/font-awesome/fontawesome-webfont.ttf"
# FontAwesome glyphs used as icons
FA_ROBOT  = '\uf2db'   # fa-microchip  → AI
FA_CHECK  = '\uf058'   # fa-check-circle → Standards
FA_USERS  = '\uf0c0'   # fa-users → Team

# ── Config ────────────────────────────────────────────────────────────────────
FPS        = 30
DURATION   = 15
TOTAL      = FPS * DURATION        # 450
W, H       = 1280, 720
FRAMES_DIR = "/sessions/brave-gallant-brahmagupta/up2you-video/frames"
OUTPUT     = "/sessions/brave-gallant-brahmagupta/mnt/outputs/up2you-ad.mp4"

os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

# ── Palette ───────────────────────────────────────────────────────────────────
BG     = (6, 14, 26)
GREEN  = (0, 196, 122)
GREEN2 = (0, 120, 80)
WHITE  = (255, 255, 255)
GRAY   = (139, 155, 180)
DARK_G = (10, 34, 22)

# ── Fonts (scaled for 1280×720) ───────────────────────────────────────────────
FP_BOLD = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
FP_MED  = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
FP_REG  = "/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf"

_font_cache = {}
def fnt(size, bold=False, medium=False):
    key = (size, bold, medium)
    if key not in _font_cache:
        path = FP_BOLD if bold else (FP_MED if medium else FP_REG)
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]

def fa(size):
    key = ('fa', size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(FA_PATH, size)
    return _font_cache[key]

def draw_fa_icon(img, glyph, cx, cy, size, color, alpha=1.0):
    """Draw a FontAwesome icon centred at (cx, cy)."""
    f   = fa(size)
    bb  = f.getbbox(glyph)
    iw  = bb[2] - bb[0]
    ih  = bb[3] - bb[1]
    x   = cx - iw // 2 - bb[0]
    y   = cy - ih // 2 - bb[1]
    tmp = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((x, y), glyph, font=f, fill=(*color, int(255 * alpha)))
    img.paste(tmp, mask=tmp)

# ── Math helpers ──────────────────────────────────────────────────────────────
def clamp(v, lo=0.0, hi=1.0): return max(lo, min(hi, v))
def lerp(a, b, t):             return a + (b - a) * clamp(t)
def interp(x, x0, x1, y0, y1):
    if x1 == x0: return y1
    return lerp(y0, y1, (x - x0) / (x1 - x0))

def spring(frame, damping=200, stiffness=100, mass=1):
    """Returns progress [0,1] for an overdamped spring."""
    if frame <= 0: return 0.0
    t  = frame / FPS
    d2 = (damping / (2 * mass)) ** 2
    sm = stiffness / mass
    if d2 > sm:
        r = math.sqrt(d2 - sm)
        A = damping / (2 * mass)
        val = 1 - math.exp(-A * t) * (math.cosh(r * t) + (A / max(r, 1e-9)) * math.sinh(r * t))
    else:
        w0  = math.sqrt(sm)
        wd  = math.sqrt(max(sm - d2, 1e-9))
        zet = damping / (2 * mass * w0)
        val = 1 - math.exp(-zet * w0 * t) * (math.cos(wd * t) + (zet * w0 / wd) * math.sin(wd * t))
    return clamp(val)

def fade_in(f, start, dur=18):  return clamp(interp(f, start, start + dur, 0, 1))
def fade_out(f, start, dur=18): return clamp(interp(f, start, start + dur, 1, 0))

# ── Drawing helpers ───────────────────────────────────────────────────────────
def paste_alpha(img, tmp): img.paste(tmp, mask=tmp)

def text_w(txt, f): b = f.getbbox(txt); return b[2] - b[0]
def text_h(txt, f): b = f.getbbox(txt); return b[3] - b[1]

def draw_text(img, txt, x, y, f, color, alpha=1.0):
    if alpha <= 0: return
    tmp = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((x, y), txt, font=f, fill=(*color, int(255 * alpha)))
    paste_alpha(img, tmp)

def draw_text_cx(img, txt, y, f, color, alpha=1.0, dy=0):
    if alpha <= 0: return
    x = (W - text_w(txt, f)) // 2
    draw_text(img, txt, x, y + int(dy), f, color, alpha)

def draw_rect(img, x, y, w, h, color, alpha=1.0):
    if alpha <= 0: return
    tmp = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(tmp).rectangle([x, y, x + w, y + h], fill=(*color, int(255 * alpha)))
    paste_alpha(img, tmp)

def draw_rrect(img, x, y, w, h, r, fill, fill_a, border=None, border_a=0.0):
    if fill_a <= 0 and border_a <= 0: return
    tmp = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d   = ImageDraw.Draw(tmp)
    if fill_a > 0:
        d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=(*fill, int(255 * fill_a)))
    if border and border_a > 0:
        d.rounded_rectangle([x, y, x + w, y + h], radius=r,
                             outline=(*border, int(255 * border_a)), width=2)
    paste_alpha(img, tmp)

# ── Background (fast solid + one gradient circle) ─────────────────────────────
def draw_bg(img, frame):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, H], fill=BG)
    # single soft radial blob
    cx = int(W * (0.5 + 0.16 * math.sin(frame * 0.012)))
    cy = int(H * (0.45 + 0.12 * math.cos(frame * 0.009)))
    for step in range(8, 0, -1):
        t   = step / 8
        rad = int(min(W, H) * 0.55 * t)
        a   = int(45 * (1 - t))
        col = tuple(int(BG[i] + (DARK_G[i] - BG[i]) * (1 - t)) for i in range(3))
        tmp = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(tmp).ellipse([cx - rad, cy - rad, cx + rad, cy + rad],
                                    fill=(*col, a))
        paste_alpha(img, tmp)

# ── Scene 1 · HOOK  (f 0→90, ~3s) ────────────────────────────────────────────
def s1_hook(img, gf):
    lf = gf
    fo = fade_out(gf, 68, 22)
    if fo <= 0: return
    f1 = fnt(52, bold=True)
    f2 = fnt(50, bold=True)

    p1 = spring(lf);      op1 = clamp(interp(p1, 0, 0.4, 0, fo)); dy1 = lerp(40, 0, p1)
    p2 = spring(lf - 18); op2 = clamp(interp(p2, 0, 0.4, 0, fo)); dy2 = lerp(40, 0, p2)

    draw_text_cx(img, "La sostenibilità è un obbligo.", 235, f1, WHITE, op1, dy1)
    draw_text_cx(img, "Falla diventare un vantaggio.", 305, f2, GREEN, op2, dy2)

    # accent bar
    bar_w = int(interp(lf, 35, 65, 0, 90))
    if bar_w > 0:
        draw_rect(img, (W - bar_w) // 2, 390, bar_w, 3, GREEN, fo)

# ── Scene 2 · PROBLEM  (removed – too short for 15s) ─────────────────────────
def s2_problem(img, gf): pass   # scene removed for 15s cut

# ── Scene 3 · SOLUTION  (f 60→185, ~2s–6.2s) ────────────────────────────────
def s3_solution(img, gf):
    lf = gf - 60
    fi = fade_in(gf, 60);   fo = fade_out(gf, 162, 23)
    al = min(fi, fo)
    if al <= 0: return
    f_badge = fnt(13, medium=True)
    f_title = fnt(50, bold=True)
    f_sub   = fnt(18, medium=True)
    f_chip  = fnt(13, bold=True)

    # Badge
    p0 = spring(lf); op0 = clamp(interp(p0, 0, 0.4, 0, al))
    badge = "UP2YOU"
    bw, bh = text_w(badge, f_badge) + 44, 32
    bx = (W - bw) // 2; by = 165 + int(lerp(20, 0, 1 - p0))
    draw_rrect(img, bx, by, bw, bh, 16, GREEN, op0 * 0.12, GREEN, op0 * 0.45)
    draw_text(img, badge, bx + 22, by + 7, f_badge, GREEN, op0)

    # Title
    p1 = spring(lf - 18); op1 = clamp(interp(p1, 0, 0.4, 0, al))
    draw_text_cx(img, "Bilancio di Sostenibilità", 218, f_title, WHITE, op1, lerp(35, 0, p1))

    # Subtitle
    p2 = spring(lf - 36); op2 = clamp(interp(p2, 0, 0.4, 0, al))
    draw_text_cx(img, "Con intelligenza artificiale integrata", 295, f_sub, GREEN, op2, lerp(30, 0, p2))

    # Chips
    p3 = spring(lf - 54); op3 = clamp(interp(p3, 0, 0.4, 0, al))
    if op3 > 0:
        stds   = ["VSME", "GRI", "ESRS", "CSRD"]
        cw, ch = 78, 30
        gap    = 12
        total  = len(stds) * cw + (len(stds) - 1) * gap
        sx     = (W - total) // 2
        dy     = int(lerp(18, 0, p3))
        for s in stds:
            draw_rrect(img, sx, 363 + dy, cw, ch, 6, WHITE, op3 * 0.05, WHITE, op3 * 0.20)
            draw_text(img, s, sx + (cw - text_w(s, f_chip)) // 2, 369 + dy, f_chip, WHITE, op3)
            sx += cw + gap

# ── Scene 4 · BENEFITS  (f 155→300, ~5.2s–10s) ──────────────────────────────
BENS = [
    (FA_ROBOT, "AI Integrata",     "-40% tempo nella\nraccolta dati"),
    (FA_CHECK, "Standard Europei", "VSME · GRI · ESRS\ndirettiva CSRD"),
    (FA_USERS, "Team Dedicato",    "Specialisti ESG\nper ogni fase"),
]

def s4_benefits(img, gf):
    lf = gf - 155
    fi = fade_in(gf, 155);  fo = fade_out(gf, 272, 28)
    al = min(fi, fo)
    if al <= 0: return
    f_lbl   = fnt(14, medium=True)
    f_title = fnt(20, bold=True)
    f_desc  = fnt(16)
    icon_sz = 32

    p0 = spring(lf); op0 = clamp(interp(p0, 0, 0.4, 0, al))
    draw_text_cx(img, "I VANTAGGI DELLA NOSTRA SOLUZIONE", 130, f_lbl, GREEN, op0, lerp(20, 0, p0))

    cw, ch = 358, 200
    gap    = 22
    total  = 3 * cw + 2 * gap
    sx0    = (W - total) // 2

    for i, (icon_glyph, title, desc) in enumerate(BENS):
        delay = 18 + i * 22
        p = spring(lf - delay)
        op = clamp(interp(p, 0, 0.5, 0, al))
        if op <= 0: continue
        cx_card = sx0 + i * (cw + gap)
        cy_card = 192
        dx = int(lerp(55, 0, p))
        draw_rrect(img, cx_card + dx, cy_card, cw, ch, 14, GREEN, op * 0.07, GREEN, op * 0.28)
        # FA icon in a small green circle
        icon_cx = cx_card + dx + 38
        icon_cy = cy_card + 44
        draw_fa_icon(img, icon_glyph, icon_cx, icon_cy, icon_sz, GREEN, op)
        draw_text(img, title, cx_card + dx + 18, cy_card + 76, f_title, WHITE, op)
        for j, line in enumerate(desc.split("\n")):
            draw_text(img, line, cx_card + dx + 18, cy_card + 110 + j * 28, f_desc, GRAY, op)

# ── Scene 5 · SOCIAL PROOF  (f 265→370, ~8.8s–12.3s) ────────────────────────
def s5_social(img, gf):
    lf = gf - 265
    fi = fade_in(gf, 265);  fo = fade_out(gf, 348, 22)
    al = min(fi, fo)
    if al <= 0: return
    f_q   = fnt(19)
    f_num = fnt(70, bold=True)
    f_lbl = fnt(18, medium=True)

    p0 = spring(lf); op0 = clamp(interp(p0, 0, 0.4, 0, al))
    draw_text_cx(img, '"Up2YOU ci ha permesso di rafforzare il nostro', 190, f_q, GRAY, op0, lerp(20, 0, p0))
    draw_text_cx(img, 'percorso verso la sostenibilità."',               228, f_q, GRAY, op0, lerp(20, 0, p0))

    for i, (num, suf, lbl, delay, px) in enumerate([
        (450, "+", "Aziende clienti",   20, W // 2 - 240),
        (180, "+", "Bilanci realizzati", 40, W // 2 + 60),
    ]):
        p  = spring(lf - delay); op = clamp(interp(p, 0, 0.4, 0, al))
        dy = int(lerp(35, 0, p))
        count = int(num * min(1.0, interp(lf, delay, delay + 45, 0, 1)))
        val_str = str(count) + suf
        draw_text(img, val_str, px, 300 + dy, f_num, GREEN, op)
        draw_text(img, lbl,     px, 388 + dy, f_lbl, WHITE,  op)

# ── Scene 6 · CTA  (f 340→450, ~11.3s–15s) ──────────────────────────────────
def s6_cta(img, gf):
    lf = gf - 340
    al = fade_in(gf, 340)
    if al <= 0: return
    f_title = fnt(46, bold=True)
    f_sub   = fnt(18, medium=True)
    f_btn   = fnt(24, bold=True)

    p0 = spring(lf);      op0 = clamp(interp(p0, 0, 0.4, 0, al))
    p1 = spring(lf - 18); op1 = clamp(interp(p1, 0, 0.4, 0, al))
    p2 = spring(lf - 36, damping=15, stiffness=200)
    op2 = clamp(interp(p2, 0, 0.4, 0, al))
    pulse = 1 + 0.018 * math.sin(lf * 0.12)

    draw_text_cx(img, "Semplifica il tuo",             200, f_title, WHITE, op0, lerp(40, 0, p0))
    draw_text_cx(img, "Bilancio di Sostenibilità ESG", 262, f_title, WHITE, op0, lerp(40, 0, p0))
    draw_text_cx(img, "Team dedicato · AI integrata · Standard europei",
                 336, f_sub, GRAY, op1, lerp(30, 0, p1))

    # CTA button
    btn  = "u2y.io"
    bw   = int((text_w(btn, f_btn) + 88) * pulse)
    bh   = int(52 * pulse)
    bx   = (W - bw) // 2; by = 400
    # glow
    draw_rrect(img, bx - 8, by - 8, bw + 16, bh + 16, (bh + 16) // 2, GREEN, op2 * 0.16)
    draw_rrect(img, bx, by, bw, bh, bh // 2, GREEN, op2)
    tw = text_w(btn, f_btn); th = text_h(btn, f_btn)
    draw_text(img, btn, bx + (bw - tw) // 2, by + (bh - th) // 2 - 2, f_btn, (0, 0, 0), op2)

# ── Render loop ───────────────────────────────────────────────────────────────
print(f"Rendering {TOTAL} frames at {W}×{H} …")
for gf in range(TOTAL):
    img = Image.new("RGBA", (W, H), (*BG, 255))
    draw_bg(img, gf)

    if gf < 92:     s1_hook(img, gf)
    if 50  <= gf < 190: s3_solution(img, gf)
    if 140 <= gf < 310: s4_benefits(img, gf)
    if 255 <= gf < 375: s5_social(img, gf)
    if 330 <= gf:        s6_cta(img, gf)

    img.convert("RGB").save(f"{FRAMES_DIR}/frame_{gf:04d}.png", optimize=False)

    if gf % 90 == 0:
        pct = gf * 100 // TOTAL
        print(f"  {gf}/{TOTAL}  ({pct}%)")

print("Frames done. Encoding …")
subprocess.run([
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", f"{FRAMES_DIR}/frame_%04d.png",
    "-vf", "scale=1920:1080:flags=lanczos",
    "-c:v", "libx264", "-preset", "fast", "-crf", "18",
    "-pix_fmt", "yuv420p", "-movflags", "+faststart",
    OUTPUT,
], check=True)

print(f"✓  Video → {OUTPUT}")
shutil.rmtree(FRAMES_DIR)
print("✓  Frames cleaned up")
