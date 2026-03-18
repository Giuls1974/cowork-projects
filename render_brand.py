"""
Up2YOU – Brand Video (15s · 30fps · 1280×720 → 1920×1080)
Stile fedele alla brand identity Up2You dal PDF presentazione.

Scenes:
  0- 90  Opening     : teal BG + archi decorativi + logo u2y
 75-195  Tagline     : "Soluzioni innovative per le tue performance ESG"
180-315  Solutions   : 4 card colorate ESG / Carbon / Cert / Formazione
295-390  Social proof: 450+ clienti · B Corp · 50+ esperti
370-450  Closing     : CTA teal + u2y.io
"""

import os, math, subprocess, shutil
from PIL import Image, ImageDraw, ImageFont

# ── Config ────────────────────────────────────────────────────────────────────
FPS        = 30
DURATION   = 15
TOTAL      = FPS * DURATION   # 450
W, H       = 1280, 720
FRAMES_DIR = "/sessions/brave-gallant-brahmagupta/up2you-video/frames_brand"
OUTPUT     = "/sessions/brave-gallant-brahmagupta/mnt/outputs/up2you-brand.mp4"

os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

# ── Brand Palette (dal PDF Up2You) ────────────────────────────────────────────
TEAL_DARK   = (13,  76,  60)    # #0D4C3C  sfondo principale slide 1/8
TEAL_MID    = (14,  90,  70)    # #0E5A46
TEAL_LIGHT  = (22, 140, 105)    # #168C69  accenti/cerchi
MINT        = (46, 196, 160)    # #2EC4A0  cerchi decorativi chiari
WHITE       = (255, 255, 255)
OFF_WHITE   = (240, 250, 245)
LIGHT_GREEN = (180, 240, 215)   # testo secondario su teal

# Colori solution cards
ESG_BG      = (250, 228, 220)   # salmone chiaro
ESG_ACC     = (192,  80,  64)   # rosso/salmone scuro
CARB_BG     = (214, 238, 248)   # azzurro chiaro
CARB_ACC    = ( 50, 140, 180)   # azzurro scuro
CERT_BG     = (245, 240, 195)   # giallo chiaro
CERT_ACC    = (160, 130,  30)   # oro scuro
FORM_BG     = (230, 220, 250)   # viola chiaro
FORM_ACC    = (100,  70, 180)   # viola scuro

# ── Font ──────────────────────────────────────────────────────────────────────
FP_BOLD = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
FP_MED  = "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
FP_REG  = "/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf"
FA_PATH = "/usr/share/fonts/truetype/font-awesome/fontawesome-webfont.ttf"

_fc = {}
def fnt(size, bold=False, med=False):
    k = (size, bold, med)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FP_BOLD if bold else (FP_MED if med else FP_REG), size)
    return _fc[k]

def fa_fnt(size):
    k = ('fa', size)
    if k not in _fc: _fc[k] = ImageFont.truetype(FA_PATH, size)
    return _fc[k]

# ── Math ──────────────────────────────────────────────────────────────────────
def clamp(v, lo=0.0, hi=1.0): return max(lo, min(hi, v))
def lerp(a, b, t):             return a + (b - a) * clamp(t)
def interp(x, x0, x1, y0, y1):
    return lerp(y0, y1, (x - x0) / (x1 - x0)) if x1 != x0 else y1

def spring(frame, damp=200, stiff=100):
    if frame <= 0: return 0.0
    t  = frame / FPS
    d2 = (damp / 2) ** 2
    sm = stiff
    if d2 > sm:
        r   = math.sqrt(max(d2 - sm, 1e-9))
        A   = damp / 2
        val = 1 - math.exp(-A * t) * (math.cosh(r * t) + A / max(r, 1e-9) * math.sinh(r * t))
    else:
        w0  = math.sqrt(sm)
        zet = damp / (2 * w0)
        wd  = math.sqrt(max(sm - (damp/2)**2, 1e-9))
        val = 1 - math.exp(-zet * w0 * t) * (math.cos(wd * t) + zet * w0 / wd * math.sin(wd * t))
    return clamp(val)

def fi(f, s, d=18): return clamp(interp(f, s, s + d, 0, 1))
def fo(f, s, d=18): return clamp(interp(f, s, s + d, 1, 0))

# ── Draw helpers ──────────────────────────────────────────────────────────────
def paste(img, tmp): img.paste(tmp, mask=tmp)

def tw(t, f): b = f.getbbox(t); return b[2] - b[0]
def th(t, f): b = f.getbbox(t); return b[3] - b[1]

def txt(img, text, x, y, f, color, alpha=1.0):
    if alpha <= 0: return
    tmp = Image.new("RGBA", img.size, (0,0,0,0))
    ImageDraw.Draw(tmp).text((x, y), text, font=f, fill=(*color, int(255*alpha)))
    paste(img, tmp)

def txt_cx(img, text, y, f, color, alpha=1.0, dy=0):
    if alpha <= 0: return
    x = (W - tw(text, f)) // 2
    txt(img, text, x, y + int(dy), f, color, alpha)

def rect(img, x, y, w, h, color, alpha=1.0):
    if alpha <= 0: return
    tmp = Image.new("RGBA", img.size, (0,0,0,0))
    ImageDraw.Draw(tmp).rectangle([x, y, x+w, y+h], fill=(*color, int(255*alpha)))
    paste(img, tmp)

def rrect(img, x, y, w, h, r, fill, fa_=1.0, border=None, ba=0.0):
    if fa_ <= 0 and ba <= 0: return
    tmp = Image.new("RGBA", img.size, (0,0,0,0))
    d   = ImageDraw.Draw(tmp)
    if fa_ > 0: d.rounded_rectangle([x,y,x+w,y+h], radius=r, fill=(*fill, int(255*fa_)))
    if border and ba > 0:
        d.rounded_rectangle([x,y,x+w,y+h], radius=r, outline=(*border, int(255*ba)), width=2)
    paste(img, tmp)

def arc_deco(img, cx, cy, r_outer, r_inner, color, alpha=1.0):
    """Ring segment used as decoration (like the circles in Up2You slides)."""
    if alpha <= 0: return
    tmp = Image.new("RGBA", img.size, (0,0,0,0))
    d   = ImageDraw.Draw(tmp)
    a   = int(255 * alpha)
    d.ellipse([cx-r_outer, cy-r_outer, cx+r_outer, cy+r_outer], fill=(*color, a))
    d.ellipse([cx-r_inner, cy-r_inner, cx+r_inner, cy+r_inner], fill=(0,0,0,0))
    paste(img, tmp)

def fa_icon(img, glyph, cx, cy, size, color, alpha=1.0):
    if alpha <= 0: return
    f  = fa_fnt(size)
    bb = f.getbbox(glyph)
    x  = cx - (bb[2]-bb[0])//2 - bb[0]
    y  = cy - (bb[3]-bb[1])//2 - bb[1]
    txt(img, glyph, x, y, f, color, alpha)

# ── Background ────────────────────────────────────────────────────────────────
def draw_bg_teal(img, frame, alpha=1.0):
    """Animated teal gradient background matching Up2You slide 1/8."""
    if alpha <= 0: return
    d = ImageDraw.Draw(img)
    d.rectangle([0,0,W,H], fill=TEAL_DARK)
    # Moving inner glow
    cx = int(W * (0.55 + 0.08 * math.sin(frame * 0.010)))
    cy = int(H * (0.42 + 0.07 * math.cos(frame * 0.008)))
    for step in range(6, 0, -1):
        t   = step / 6
        rad = int(min(W,H) * 0.65 * t)
        col = tuple(int(TEAL_DARK[i] + (TEAL_MID[i]-TEAL_DARK[i]) * (1-t)) for i in range(3))
        a   = int(70 * (1-t) * alpha)
        tmp = Image.new("RGBA", img.size, (0,0,0,0))
        ImageDraw.Draw(tmp).ellipse([cx-rad, cy-rad, cx+rad, cy+rad], fill=(*col, a))
        paste(img, tmp)

def draw_bg_white(img, frame, alpha=1.0):
    """White/light background for solutions scene."""
    if alpha <= 0: return
    tmp = Image.new("RGBA", img.size, (0,0,0,0))
    ImageDraw.Draw(tmp).rectangle([0,0,W,H], fill=(248,252,250, int(255*alpha)))
    paste(img, tmp)

# ── Decorative arcs (brand signature) ────────────────────────────────────────
def draw_arcs(img, frame, alpha=1.0):
    """Large ring arcs in corners – the distinctive Up2You visual signature."""
    if alpha <= 0: return
    # Top-right
    arc_deco(img, W + 40, -50,  220, 150, TEAL_LIGHT, alpha * 0.55)
    arc_deco(img, W + 80, -80,  310, 225, MINT,        alpha * 0.25)
    # Bottom-left
    arc_deco(img, -40,  H + 40, 200, 140, TEAL_LIGHT,  alpha * 0.50)
    arc_deco(img, -80,  H + 80, 300, 215, MINT,         alpha * 0.22)

# ── U2Y Logo (text-based recreation) ─────────────────────────────────────────
def draw_logo(img, x, y, scale=1.0, alpha=1.0, color=WHITE):
    """Draws 'u2y' + 'up2you' stacked, mimicking Up2You's wordmark."""
    if alpha <= 0: return
    f_top = fnt(int(28*scale), bold=True)
    f_bot = fnt(int(13*scale), med=True)
    txt(img, "u2y",    x, y,           f_top, color, alpha)
    txt(img, "up2you", x, y + int(28*scale) + 2, f_bot, color, alpha)

# ══════════════════════════════════════════════════════════════════════════════
# Scene 1 · OPENING  (f 0 → 100)
# ══════════════════════════════════════════════════════════════════════════════
def scene_opening(img, gf):
    lf = gf
    fade = fo(gf, 78, 22)
    if fade <= 0: return

    p_bg  = spring(lf, damp=200)
    p_arc = spring(lf - 8, damp=200)
    p_log = spring(lf - 20, damp=200)

    alpha_bg  = clamp(interp(p_bg,  0, 0.3, 0, fade))
    alpha_arc = clamp(interp(p_arc, 0, 0.3, 0, fade))
    alpha_log = clamp(interp(p_log, 0, 0.4, 0, fade))

    draw_bg_teal(img, lf, alpha_bg)
    draw_arcs(img, lf, alpha_arc)
    draw_logo(img, 48, 40, scale=1.2, alpha=alpha_log)

# ══════════════════════════════════════════════════════════════════════════════
# Scene 2 · TAGLINE  (f 70 → 200)
# ══════════════════════════════════════════════════════════════════════════════
def scene_tagline(img, gf):
    lf = gf - 70
    al = min(fi(gf, 70, 20), fo(gf, 175, 25))
    if al <= 0: return

    draw_bg_teal(img, gf, al)
    draw_arcs(img, gf, al * 0.85)

    # Logo top-left
    p_log = spring(lf, damp=200)
    draw_logo(img, 48, 40, scale=1.1, alpha=clamp(interp(p_log,0,0.4,0,al)))

    # Main headline – split into two lines
    f_h1 = fnt(58, bold=True)
    f_h2 = fnt(56, bold=True)
    f_sub = fnt(20, med=True)

    p1 = spring(lf - 5,  damp=200)
    p2 = spring(lf - 18, damp=200)
    p3 = spring(lf - 34, damp=200)

    dy1 = lerp(45, 0, p1)
    dy2 = lerp(45, 0, p2)
    dy3 = lerp(30, 0, p3)

    op1 = clamp(interp(p1, 0, 0.4, 0, al))
    op2 = clamp(interp(p2, 0, 0.4, 0, al))
    op3 = clamp(interp(p3, 0, 0.4, 0, al))

    txt_cx(img, "Soluzioni innovative per",          260, f_h1, WHITE,      op1, dy1)
    txt_cx(img, "le tue performance ESG",             330, f_h2, WHITE,      op2, dy2)
    txt_cx(img, "Rendi la sostenibilità il tuo vantaggio competitivo.", 420, f_sub, LIGHT_GREEN, op3, dy3)

# ══════════════════════════════════════════════════════════════════════════════
# Scene 3 · SOLUTIONS  (f 180 → 315)
# ══════════════════════════════════════════════════════════════════════════════
SOLUTIONS = [
    ("ESG\nmanagement",        ESG_BG,  ESG_ACC,  "\uf200"),  # fa-pie-chart
    ("Carbon\nmanagement",     CARB_BG, CARB_ACC, "\uf06c"),  # fa-leaf
    ("Certificazioni\ne iniziative", CERT_BG, CERT_ACC, "\uf091"),  # fa-trophy
    ("Formazione e\ncoinvolgimento", FORM_BG, FORM_ACC, "\uf19d"),  # fa-graduation-cap
]

def scene_solutions(img, gf):
    lf = gf - 180
    al = min(fi(gf, 180, 20), fo(gf, 290, 25))
    if al <= 0: return

    draw_bg_white(img, gf, al)

    # Section label
    f_lbl  = fnt(14, med=True)
    f_card = fnt(16, bold=True)
    f_desc = fnt(12)
    f_logo = fnt(12, bold=True)

    p0 = spring(lf, damp=200)
    op0 = clamp(interp(p0, 0, 0.4, 0, al))
    dy0 = lerp(20, 0, p0)

    # "Le nostre soluzioni su misura" header
    f_h = fnt(28, bold=True)
    DARK_TEXT = (30, 30, 50)
    txt_cx(img, "Le nostre soluzioni su misura", 60, f_h, DARK_TEXT, op0, dy0)
    txt_cx(img, "per la tua azienda",            100, f_h, DARK_TEXT, op0, dy0)

    # 4 solution cards
    cw, ch = 276, 230
    gap    = 16
    total  = 4 * cw + 3 * gap
    sx0    = (W - total) // 2

    for i, (title, bg, acc, icon_g) in enumerate(SOLUTIONS):
        delay = 12 + i * 18
        p  = spring(lf - delay, damp=200)
        op = clamp(interp(p, 0, 0.5, 0, al))
        if op <= 0: continue

        cx = sx0 + i * (cw + gap)
        cy = 160
        dy = int(lerp(40, 0, p))

        rrect(img, cx, cy+dy, cw, ch, 16, bg, op)

        # Icon
        fa_icon(img, icon_g, cx + 36, cy + dy + 36, 28, acc, op)

        # Title (multiline)
        lines = title.split('\n')
        for j, line in enumerate(lines):
            f_t = fnt(18, bold=True)
            txt(img, line, cx + 16, cy + dy + 65 + j*24, f_t, acc, op)

        # Up2You logo watermark on card
        txt(img, "up2you", cx + 16, cy + dy + ch - 26, fnt(10, bold=True), acc, op * 0.5)

    # Bottom: u2y logo
    draw_logo(img, 48, H - 65, scale=0.85, alpha=op0 * 0.6, color=(80, 120, 100))

# ══════════════════════════════════════════════════════════════════════════════
# Scene 4 · SOCIAL PROOF  (f 290 → 385)
# ══════════════════════════════════════════════════════════════════════════════
def scene_proof(img, gf):
    lf = gf - 290
    al = min(fi(gf, 290, 20), fo(gf, 363, 22))
    if al <= 0: return

    draw_bg_teal(img, gf, al)
    draw_arcs(img, gf, al * 0.7)
    draw_logo(img, 48, 40, scale=1.1, alpha=al * 0.9)

    f_num  = fnt(80, bold=True)
    f_lbl  = fnt(20, med=True)
    f_sub  = fnt(15)
    f_cert = fnt(13, bold=True)

    p0 = spring(lf,      damp=200)
    p1 = spring(lf - 18, damp=200)
    p2 = spring(lf - 36, damp=200)

    # 450+ counter left
    op0 = clamp(interp(p0, 0, 0.4, 0, al))
    count450 = int(450 * min(1.0, interp(lf, 0, 50, 0, 1)))
    num_txt = str(count450) + "+"
    x_l = W//2 - 280
    txt(img, num_txt,         x_l, 240 + int(lerp(35,0,p0)), f_num, MINT,  op0)
    txt(img, "Clienti Up2You",x_l, 330 + int(lerp(30,0,p0)), f_lbl, WHITE, op0)

    # 50+ counter right
    op1 = clamp(interp(p1, 0, 0.4, 0, al))
    count50 = int(50 * min(1.0, interp(lf, 18, 68, 0, 1)))
    num_txt2 = str(count50) + "+"
    x_r = W//2 + 60
    txt(img, num_txt2,         x_r, 240 + int(lerp(35,0,p1)), f_num, MINT,  op1)
    txt(img, "Esperti nel team",x_r, 330 + int(lerp(30,0,p1)), f_lbl, WHITE, op1)

    # B Corp badge text
    op2 = clamp(interp(p2, 0, 0.4, 0, al))
    rrect(img, W//2 - 120, 400 + int(lerp(20,0,p2)), 240, 40, 20,
          TEAL_LIGHT, op2 * 0.3, MINT, op2 * 0.6)
    cert_t = "Certified B Corp  ·  UN Global Compact"
    txt(img, cert_t, W//2 - tw(cert_t, f_cert)//2, 412 + int(lerp(20,0,p2)), f_cert, WHITE, op2)

# ══════════════════════════════════════════════════════════════════════════════
# Scene 5 · CLOSING CTA  (f 365 → 450)
# ══════════════════════════════════════════════════════════════════════════════
def scene_closing(img, gf):
    lf = gf - 365
    al = fi(gf, 365, 20)
    if al <= 0: return

    draw_bg_teal(img, gf, al)
    draw_arcs(img, gf, al)

    p0 = spring(lf,      damp=200)
    p1 = spring(lf - 16, damp=200)
    p2 = spring(lf - 32, damp=15, stiff=200)

    f_t1  = fnt(38, bold=True)
    f_t2  = fnt(36, bold=True)
    f_sub = fnt(17, med=True)
    f_url = fnt(28, bold=True)

    op0 = clamp(interp(p0, 0, 0.4, 0, al))
    op1 = clamp(interp(p1, 0, 0.4, 0, al))
    op2 = clamp(interp(p2, 0, 0.4, 0, al))

    txt_cx(img, "Rendi la sostenibilità",         240, f_t1, WHITE,       op0, lerp(40,0,p0))
    txt_cx(img, "il tuo vantaggio competitivo.",  295, f_t2, WHITE,       op0, lerp(40,0,p0))
    txt_cx(img, "Percorso guidato · Tecnologie proprietarie · Team certificato",
                370, f_sub, LIGHT_GREEN, op1, lerp(28,0,p1))

    # CTA button
    pulse = 1 + 0.02 * math.sin(lf * 0.13)
    btn   = "www.u2y.io"
    bw    = int((tw(btn, f_url) + 80) * pulse)
    bh    = int(54 * pulse)
    bx    = (W - bw) // 2
    by    = 430

    rrect(img, bx-6, by-6, bw+12, bh+12, (bh+12)//2, MINT, op2*0.18)
    rrect(img, bx,   by,   bw,    bh,    bh//2,       MINT, op2)
    btn_tw = tw(btn, f_url)
    btn_th = th(btn, f_url)
    txt(img, btn, bx + (bw-btn_tw)//2, by + (bh-btn_th)//2 - 2, f_url, TEAL_DARK, op2)

    # Logo top-left
    draw_logo(img, 48, 40, scale=1.1, alpha=al)

# ══════════════════════════════════════════════════════════════════════════════
# Render loop
# ══════════════════════════════════════════════════════════════════════════════
print(f"Rendering {TOTAL} frames at {W}×{H} — Up2YOU Brand Video …")

for gf in range(TOTAL):
    img = Image.new("RGBA", (W, H), (*TEAL_DARK, 255))

    if gf < 105:
        scene_opening(img, gf)

    if 65 <= gf < 205:
        scene_tagline(img, gf)

    if 175 <= gf < 320:
        scene_solutions(img, gf)

    if 285 <= gf < 390:
        scene_proof(img, gf)

    if 360 <= gf:
        scene_closing(img, gf)

    img.convert("RGB").save(f"{FRAMES_DIR}/frame_{gf:04d}.png", optimize=False)

    if gf % 90 == 0:
        print(f"  {gf}/{TOTAL} ({gf*100//TOTAL}%)")

print("Frames done. Encoding …")
subprocess.run([
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", f"{FRAMES_DIR}/frame_%04d.png",
    "-vf", "scale=1920:1080:flags=lanczos",
    "-c:v", "libx264", "-preset", "fast", "-crf", "17",
    "-pix_fmt", "yuv420p", "-movflags", "+faststart",
    OUTPUT,
], check=True)

print(f"✓  Brand video → {OUTPUT}")
shutil.rmtree(FRAMES_DIR)
print("✓  Frames cleaned up")
