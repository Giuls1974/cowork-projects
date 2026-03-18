"""
Genera loghi B Corp e UN Global Compact come PNG bianchi su trasparente
per uso su sfondo teal scuro nel video Up2YOU.
Ricostruzione fedele dai loghi ufficiali visti nelle immagini allegate.
"""
import cairosvg, os

OUT = "/sessions/brave-gallant-brahmagupta/up2you-video/logos"
os.makedirs(OUT, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# 1. B CORP CERTIFIED  — tag verticale bianco su trasparente
#    Shape: rettangolo con angoli superiori arrotondati + semicerchio in basso
#    "CERTIFIED" in cima (lettere spaziate), grande "B" al centro,
#    "CORPORATION" in basso
# ─────────────────────────────────────────────────────────────────────────────
bcorp_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 300">
  <defs>
    <clipPath id="tag">
      <path d="M10,0 H190 Q200,0 200,10 V210 Q200,240 170,260
               Q140,280 100,290 Q60,280 30,260 Q0,240 0,210 V10 Q0,0 10,0 Z"/>
    </clipPath>
  </defs>

  <!-- Tag background (white, fully visible) -->
  <path d="M10,0 H190 Q200,0 200,10 V210 Q200,240 170,260
           Q140,280 100,290 Q60,280 30,260 Q0,240 0,210 V10 Q0,0 10,0 Z"
        fill="white"/>

  <!-- Dark header band -->
  <rect x="0" y="0" width="200" height="55" clip-path="url(#tag)" fill="#1a1a1a"/>

  <!-- CERTIFIED text in header -->
  <text x="100" y="38"
        font-family="Arial Black, Arial, sans-serif"
        font-size="16" font-weight="900" letter-spacing="3.5"
        text-anchor="middle" fill="white">CERTIFIED</text>

  <!-- Big B -->
  <text x="100" y="195"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="155" font-weight="900"
        text-anchor="middle" fill="#1a1a1a">B</text>

  <!-- CORPORATION text at bottom -->
  <text x="100" y="265"
        font-family="Arial, Helvetica, sans-serif"
        font-size="14.5" font-weight="700" letter-spacing="2.5"
        text-anchor="middle" fill="#1a1a1a">CORPORATION</text>
</svg>
"""

# White-on-transparent version (invert: dark→white, white→transparent)
bcorp_white_svg = bcorp_svg \
    .replace('fill="white"/>', 'fill="none"/>') \
    .replace('fill="#1a1a1a"', 'fill="white"') \
    .replace('fill="white">', 'fill="none">')   \

# Re-write cleanly
bcorp_white_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 340">
  <defs>
    <!-- Tag shape: rounded rect, flat top, semicircle bottom -->
    <clipPath id="tag-clip">
      <path d="M16,0 H204 Q220,0 220,16 V240
               Q220,300 110,338
               Q0,300 0,240 V16 Q0,0 16,0 Z"/>
    </clipPath>
  </defs>

  <!-- Tag body: white border only (transparent fill for teal BG) -->
  <path d="M16,0 H204 Q220,0 220,16 V240
           Q220,300 110,338
           Q0,300 0,240 V16 Q0,0 16,0 Z"
        fill="none" stroke="white" stroke-width="4"/>

  <!-- Hole at top (punch hole) -->
  <circle cx="110" cy="0" r="10" fill="none" stroke="white" stroke-width="3"/>

  <!-- CERTIFIED header band (clipped) -->
  <rect x="0" y="0" width="220" height="62" clip-path="url(#tag-clip)" fill="white"/>

  <!-- CERTIFIED text — dark teal on white band -->
  <text x="110" y="43"
        font-family="'Arial Black', 'Franklin Gothic Heavy', Arial, sans-serif"
        font-size="17" font-weight="900" letter-spacing="4"
        text-anchor="middle" fill="#0D4C3C">CERTIFIED</text>

  <!-- Thin separator line -->
  <line x1="20" y1="62" x2="200" y2="62" stroke="white" stroke-width="1.5" opacity="0.6"/>

  <!-- Big B — bold rounded sans-serif, white -->
  <text x="110" y="235"
        font-family="'Arial Black', 'Franklin Gothic Heavy', Impact, Arial, sans-serif"
        font-size="185" font-weight="900"
        text-anchor="middle" fill="white">B</text>

  <!-- Bottom separator -->
  <line x1="20" y1="250" x2="200" y2="250" stroke="white" stroke-width="1.5" opacity="0.6"/>

  <!-- CORPORATION bottom text -->
  <text x="110" y="296"
        font-family="'Arial Black', Arial, sans-serif"
        font-size="15" font-weight="700" letter-spacing="3"
        text-anchor="middle" fill="white">CORPORATION</text>
</svg>
"""

cairosvg.svg2png(bytestring=bcorp_white_svg.encode(),
                 write_to=f"{OUT}/bcorp.png",
                 output_width=110, output_height=170)

print("✓ B Corp logo → bcorp.png")

# ─────────────────────────────────────────────────────────────────────────────
# 2. UN GLOBAL COMPACT — globe + circular text + olive branches + wordmark
#    Fedelmente dal logo ufficiale: globo navy con trama, testo arcuato,
#    rami d'ulivo sotto, "United Nations / Global Compact" a destra
#    → versione WHITE su trasparente per sfondo teal
# ─────────────────────────────────────────────────────────────────────────────
ungc_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 170">

  <!-- ── EMBLEM (left, centred at 90,85) ─────────────────────── -->
  <g transform="translate(90,82)">

    <!-- Outer ring with "UN GLOBAL COMPACT" text -->
    <circle cx="0" cy="0" r="76" fill="none" stroke="white" stroke-width="2.5"/>

    <!-- Circular text: UN GLOBAL COMPACT -->
    <defs>
      <path id="top-arc" d="M -68,0 A 68,68 0 0,1 68,0"/>
    </defs>
    <text font-family="Arial, Helvetica, sans-serif" font-size="11.5"
          font-weight="700" letter-spacing="3.2" fill="white">
      <textPath href="#top-arc" startOffset="8%">UN GLOBAL COMPACT</textPath>
    </text>

    <!-- Globe body -->
    <circle cx="0" cy="0" r="54" fill="none" stroke="white" stroke-width="2.5"/>

    <!-- Meridians (vertical arcs) -->
    <ellipse cx="0" cy="0" rx="18" ry="54" fill="none" stroke="white" stroke-width="1.5"/>
    <ellipse cx="0" cy="0" rx="36" ry="54" fill="none" stroke="white" stroke-width="1.5"/>
    <line x1="0" y1="-54" x2="0" y2="54" stroke="white" stroke-width="1.5"/>

    <!-- Parallels (horizontal lines) -->
    <line x1="-54" y1="0" x2="54" y2="0" stroke="white" stroke-width="1.5"/>
    <ellipse cx="0" cy="0" rx="54" ry="18" fill="none" stroke="white" stroke-width="1.2"/>
    <ellipse cx="0" cy="0" rx="54" ry="36" fill="none" stroke="white" stroke-width="1.2"/>

    <!-- Olive branch LEFT (mirrored) -->
    <!-- Stem -->
    <path d="M -8,58 Q -25,68 -45,62" fill="none" stroke="white" stroke-width="2" stroke-linecap="round"/>
    <path d="M -8,58 Q -30,75 -55,72" fill="none" stroke="white" stroke-width="2" stroke-linecap="round"/>
    <!-- Leaves left branch -->
    <ellipse cx="-20" cy="60" rx="7" ry="3.5" fill="white" transform="rotate(-35 -20 60)"/>
    <ellipse cx="-30" cy="65" rx="7" ry="3.5" fill="white" transform="rotate(-45 -30 65)"/>
    <ellipse cx="-40" cy="68" rx="7" ry="3.5" fill="white" transform="rotate(-55 -40 68)"/>
    <ellipse cx="-48" cy="67" rx="7" ry="3.5" fill="white" transform="rotate(-65 -48 67)"/>
    <ellipse cx="-16" cy="66" rx="6" ry="3" fill="white" transform="rotate(-25 -16 66)"/>
    <ellipse cx="-35" cy="72" rx="6" ry="3" fill="white" transform="rotate(-50 -35 72)"/>
    <ellipse cx="-50" cy="70" rx="6" ry="3" fill="white" transform="rotate(-70 -50 70)"/>

    <!-- Olive branch RIGHT -->
    <path d="M 8,58 Q 25,68 45,62" fill="none" stroke="white" stroke-width="2" stroke-linecap="round"/>
    <path d="M 8,58 Q 30,75 55,72" fill="none" stroke="white" stroke-width="2" stroke-linecap="round"/>
    <!-- Leaves right branch -->
    <ellipse cx="20" cy="60" rx="7" ry="3.5" fill="white" transform="rotate(35 20 60)"/>
    <ellipse cx="30" cy="65" rx="7" ry="3.5" fill="white" transform="rotate(45 30 65)"/>
    <ellipse cx="40" cy="68" rx="7" ry="3.5" fill="white" transform="rotate(55 40 68)"/>
    <ellipse cx="48" cy="67" rx="7" ry="3.5" fill="white" transform="rotate(65 48 67)"/>
    <ellipse cx="16" cy="66" rx="6" ry="3" fill="white" transform="rotate(25 16 66)"/>
    <ellipse cx="35" cy="72" rx="6" ry="3" fill="white" transform="rotate(50 35 72)"/>
    <ellipse cx="50" cy="70" rx="6" ry="3" fill="white" transform="rotate(70 50 70)"/>

    <!-- Centre join of branches -->
    <circle cx="0" cy="60" r="3" fill="white"/>

  </g>

  <!-- ── VERTICAL DIVIDER ─────────────────────────────────────── -->
  <line x1="178" y1="22" x2="178" y2="148" stroke="white" stroke-width="1.8" opacity="0.5"/>

  <!-- ── WORDMARK (right) ─────────────────────────────────────── -->
  <text x="200" y="72"
        font-family="'Arial Black', Arial, sans-serif"
        font-size="38" font-weight="900"
        fill="white">United Nations</text>
  <text x="200" y="118"
        font-family="Arial, Helvetica, sans-serif"
        font-size="38" font-weight="400"
        fill="white">Global Compact</text>

</svg>
"""

cairosvg.svg2png(bytestring=ungc_svg.encode(),
                 write_to=f"{OUT}/ungc.png",
                 output_width=490, output_height=149)

print("✓ UN Global Compact logo → ungc.png")

# Verify
for f in ["bcorp.png", "ungc.png"]:
    size = os.path.getsize(f"{OUT}/{f}")
    print(f"  {f}: {size:,} bytes")
