#!/usr/bin/env python3
"""
PCARS Theme — Asset Generator
WiFi Pineapple Pager (480x222 display)

Pineapple Computer Access Retrieval System
Dark steel-blue structural frame, near-black content areas, surgical accent colors.
Supersampled rendering at 3x with LANCZOS downscale for clean anti-aliased edges.

Usage: python3 generate_pcars_assets.py
"""

import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ─── Configuration ───────────────────────────────────────────────────────────

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
SS = 3  # Supersample factor (render at 3x, downscale for anti-aliasing)

# ─── PCARS Palette ────────────────────────────────────────────────────────────
# PCARS-style: deep navy-black base, dark frame bars, bright blue edge glow.

# Backgrounds — deep navy-black
BG        = (4, 6, 16)            # Deep navy-black — primary background
PANEL     = (8, 14, 30)           # Dark navy panel — behind text/content
PANEL_L   = (12, 20, 40)          # Lighter panel — active/hover areas

# Structural Frame — dark navy body with bright edge glow
FRAME     = (16, 36, 72)          # Frame bar body — dark navy blue
FRAME_D   = (10, 26, 52)          # Darker frame variant
FRAME_L   = (24, 55, 105)         # Frame edge highlight
FRAME_T   = (14, 32, 62)          # Frame teal-shifted variant

# Edge Glow — bright blue accents (PCARS accent)
EDGE      = (40, 120, 220)        # Primary bright edge line
EDGE_L    = (60, 150, 245)        # Lighter edge glow / bloom

# Accent Colors — functional, used sparingly
AMBER     = (255, 153, 0)         # Warm accent — labels, indicators
ORANGE    = (204, 102, 0)         # Secondary warm accent
PEACH     = (255, 180, 120)       # Tertiary — warm accent
GOLD      = (218, 178, 56)        # Warm data accent

# Cool Accents
CYAN      = (0, 195, 215)         # Primary highlight / selected state
TEAL      = (0, 155, 175)         # Secondary highlight
BLUE      = (58, 128, 225)        # Info / data text
LT_BLUE   = (115, 175, 250)      # Light data readout

# Functional
RED       = (215, 48, 38)         # Alert / error
MAGENTA   = (175, 58, 138)       # PineAP / attack
YELLOW    = (225, 195, 55)        # Warning
GREEN     = (75, 195, 75)         # Success / enabled
PURPLE    = (135, 78, 195)       # Misc accent

# Neutrals
WHITE     = (215, 220, 230)       # Primary text
SOFT_W    = (175, 180, 190)       # Secondary text
GRAY      = (95, 100, 110)       # Disabled text
DARK_GRAY = (24, 30, 48)         # Borders / subtle separators
DIM       = (38, 44, 58)         # Dimmed elements

T = (0, 0, 0, 0)  # Transparent

# Section Identity Colors (from dashboard columns, for inner menu theming)
SEC_ALERTS     = (210, 75, 60)     # Coral-red — matches ALERTS dashboard column
SEC_ALERTS_D   = (160, 50, 40)     # Dark coral
SEC_PAYLOADS   = (225, 175, 55)    # Amber-gold — matches PAYLOADS dashboard column
SEC_PAYLOADS_D = (170, 130, 35)    # Dark amber
SEC_RECON      = (40, 200, 80)     # Borg green — matches RECON dashboard column
SEC_RECON_D    = (20, 130, 45)     # Dark Borg green
SEC_PINEAP     = (170, 90, 190)    # Purple — matches PINEAP dashboard column
SEC_PINEAP_D   = (110, 55, 130)    # Dark purple
SEC_SETTINGS   = (90, 140, 220)    # Blue — matches SETTINGS dashboard column
SEC_SETTINGS_D = (50, 90, 155)     # Dark blue
SEC_POWER      = (60, 60, 75)      # Neutral gray-blue — system menu
SEC_POWER_D    = (35, 35, 48)      # Dark neutral


# ─── Core Drawing Utilities ──────────────────────────────────────────────────

def _c(color, alpha=255):
    """Color tuple with alpha."""
    if len(color) == 4:
        return color
    return (*color, alpha)


def ensure_dir(path):
    os.makedirs(os.path.join(ASSETS_DIR, path), exist_ok=True)


def save(img, path):
    full = os.path.join(ASSETS_DIR, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    img.save(full, "PNG", optimize=True)


def new(w, h, bg=None):
    """New RGBA image."""
    if bg is None:
        return Image.new("RGBA", (w, h), T)
    return Image.new("RGBA", (w, h), _c(bg))


def ss_start(w, h, bg=None):
    """Start supersampled drawing. Returns (image, draw) at SS*w x SS*h."""
    img = new(w * SS, h * SS, bg)
    return img, ImageDraw.Draw(img)


def ss_finish(img, w, h):
    """Downscale supersampled image to target size."""
    return img.resize((w, h), Image.LANCZOS)


def _draw_organic_plasma(w, h, seed=42, color=(255, 255, 255)):
    """Draw an organic plasma ball with irregular lightning arcs.

    Returns a w x h RGBA image (already downsampled from supersample).
    """
    import random as _rand
    rng = _rand.Random(seed)

    ws, hs = w * SS, h * SS
    img = Image.new("RGBA", (ws, hs), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = ws // 2, hs // 2
    r_outer = min(ws, hs) // 2 - 4 * SS

    # Outer ring with slight organic wobble
    for i in range(3):
        ox = rng.randint(-SS // 2, SS // 2)
        oy = rng.randint(-SS // 2, SS // 2)
        d.ellipse([cx - r_outer + ox, cy - r_outer + oy,
                    cx + r_outer + ox, cy + r_outer + oy],
                  outline=_c(color, 160 + i * 30), width=2 * SS)

    # Inner glow ring
    r_glow = r_outer - 3 * SS
    d.ellipse([cx - r_glow, cy - r_glow, cx + r_glow, cy + r_glow],
              outline=_c(color, 40), width=2 * SS)

    # 4-6 bolts at irregular angles
    num_bolts = rng.randint(4, 6)
    angles = []
    angle = rng.uniform(0, 360)
    for _ in range(num_bolts):
        angles.append(angle)
        angle += rng.uniform(35, 120)

    for bolt_deg in angles:
        ba = math.radians(bolt_deg)
        r_start = int(r_outer * rng.uniform(0.05, 0.12))
        r_end = int(r_outer * rng.uniform(0.60, 0.92))

        # 5-8 zigzag segments
        num_segs = rng.randint(5, 8)
        pts = []
        for seg in range(num_segs + 1):
            t = seg / num_segs
            r_at = r_start + (r_end - r_start) * t
            if seg == 0:
                jitter = 0
            else:
                max_jitter = 6 * SS * t * rng.uniform(0.3, 2.0)
                jitter = rng.uniform(-max_jitter, max_jitter)
            angle_wobble = rng.uniform(-0.15, 0.15) if seg > 0 else 0
            a = ba + angle_wobble
            bx = int(cx + r_at * math.cos(a) + jitter * math.cos(a + 1.57))
            by = int(cy + r_at * math.sin(a) + jitter * math.sin(a + 1.57))
            pts.append((bx, by))

        thickness = rng.choice([1, 2, 2, 3]) * SS
        # Glow
        d.line(pts, fill=_c(color, 60), width=thickness + 2 * SS, joint="curve")
        # Main bolt
        d.line(pts, fill=_c(color, 200), width=thickness, joint="curve")
        # Bright core
        if thickness > SS:
            d.line(pts, fill=_c(color, 255), width=max(SS, thickness - SS), joint="curve")

        # Fork branch — 40% chance
        if rng.random() < 0.4 and len(pts) > 3:
            fork_idx = rng.randint(2, len(pts) - 2)
            fork_start = pts[fork_idx]
            fork_angle = ba + rng.uniform(-1.0, 1.0)
            fork_len = int(r_outer * rng.uniform(0.1, 0.25))
            fork_pts = [fork_start]
            for fs in range(rng.randint(2, 3)):
                ft = (fs + 1) / 3
                fr = fork_len * ft
                fj = rng.uniform(-4, 4) * SS
                fx = int(fork_start[0] + fr * math.cos(fork_angle) + fj * math.cos(fork_angle + 1.57))
                fy = int(fork_start[1] + fr * math.sin(fork_angle) + fj * math.sin(fork_angle + 1.57))
                fork_pts.append((fx, fy))
            d.line(fork_pts, fill=_c(color, 140), width=SS, joint="curve")

    # Center dot
    cr = 4 * SS
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=_c(color, 220))
    cr2 = 2 * SS
    d.ellipse([cx - cr2, cy - cr2, cx + cr2, cy + cr2], fill=_c(color, 255))

    return img.resize((w, h), Image.LANCZOS)


def glow(img, radius=4, intensity=0.6):
    """Add glow behind bright pixels."""
    blur = img.filter(ImageFilter.GaussianBlur(radius=radius))
    if intensity < 1.0:
        bands = blur.split()
        alpha = bands[3].point(lambda p: int(p * intensity))
        blur = Image.merge("RGBA", (*bands[:3], alpha))
    result = Image.new("RGBA", img.size, T)
    result = Image.alpha_composite(result, blur)
    result = Image.alpha_composite(result, img)
    return result


def pill(d, xy, fill, direction="right", s=SS):
    """PCARS pill shape — rectangle with semicircular end(s)."""
    x0, y0, x1, y1 = [v * s for v in xy] if s > 1 else xy
    h = y1 - y0
    r = h // 2
    fc = _c(fill)

    if direction == "both":
        d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fc)
    elif direction == "right":
        d.rectangle([x0, y0, x1 - r, y1], fill=fc)
        d.ellipse([x1 - h, y0, x1, y1], fill=fc)
    elif direction == "left":
        d.rectangle([x0 + r, y0, x1, y1], fill=fc)
        d.ellipse([x0, y0, x0 + h, y1], fill=fc)


def rrect(d, xy, fill=None, outline=None, radius=4, width=1, s=SS):
    """Rounded rectangle with optional supersample scaling."""
    x0, y0, x1, y1 = [v * s for v in xy] if s > 1 else xy
    r = radius * s if s > 1 else radius
    w = width * s if s > 1 else width
    d.rounded_rectangle([x0, y0, x1, y1], radius=r,
                        fill=_c(fill) if fill else None,
                        outline=_c(outline) if outline else None,
                        width=w)


def pcars_elbow(d, x, y, bar_w, bar_h, side_w, side_h, fill, corner="tl", s=SS):
    """Draw PCARS elbow — the signature L-junction with rounded outer corner."""
    x, y, bar_w, bar_h, side_w, side_h = [v * s for v in (x, y, bar_w, bar_h, side_w, side_h)]
    fc = _c(fill)
    r = min(side_w, bar_h) + max(side_w, bar_h) // 3

    if corner == "tl":
        d.rectangle([x + r, y, x + bar_w, y + bar_h], fill=fc)
        d.rectangle([x, y + r, x + side_w, y + side_h], fill=fc)
        d.pieslice([x, y, x + r * 2, y + r * 2], 180, 270, fill=fc)
        d.rectangle([x, y, x + side_w, y + r], fill=fc)
        d.rectangle([x, y, x + r, y + bar_h], fill=fc)

    elif corner == "bl":
        d.rectangle([x + r, y + side_h - bar_h, x + bar_w, y + side_h], fill=fc)
        d.rectangle([x, y, x + side_w, y + side_h - r], fill=fc)
        d.pieslice([x, y + side_h - r * 2, x + r * 2, y + side_h], 90, 180, fill=fc)
        d.rectangle([x, y + side_h - r, x + side_w, y + side_h], fill=fc)
        d.rectangle([x, y + side_h - bar_h, x + r, y + side_h], fill=fc)

    elif corner == "tr":
        d.rectangle([x, y, x + bar_w - r, y + bar_h], fill=fc)
        d.rectangle([x + bar_w - side_w, y + r, x + bar_w, y + side_h], fill=fc)
        d.pieslice([x + bar_w - r * 2, y, x + bar_w, y + r * 2], 270, 360, fill=fc)
        d.rectangle([x + bar_w - side_w, y, x + bar_w, y + r], fill=fc)
        d.rectangle([x + bar_w - r, y, x + bar_w, y + bar_h], fill=fc)

    elif corner == "br":
        d.rectangle([x, y + side_h - bar_h, x + bar_w - r, y + side_h], fill=fc)
        d.rectangle([x + bar_w - side_w, y, x + bar_w, y + side_h - r], fill=fc)
        d.pieslice([x + bar_w - r * 2, y + side_h - r * 2, x + bar_w, y + side_h], 0, 90, fill=fc)
        d.rectangle([x + bar_w - side_w, y + side_h - r, x + bar_w, y + side_h], fill=fc)
        d.rectangle([x + bar_w - r, y + side_h - bar_h, x + bar_w, y + side_h], fill=fc)


def data_blocks(d, x, y, w, h, colors=None, gap=2, count=None, s=SS):
    """Decorative data readout blocks — subtle colored segments."""
    import random
    if colors is None:
        colors = [FRAME_L, FRAME, FRAME_D, EDGE, FRAME_L]
    x, y, w, h, gap = [v * s for v in (x, y, w, h, gap)]
    if count is None:
        count = max(3, w // ((8 * s) + gap))
    min_w = 5 * s

    cx = x
    remaining = w
    for i in range(count):
        if remaining <= min_w:
            break
        bw = random.randint(min_w, max(min_w + 1, remaining // max(1, count - i)))
        if i == count - 1:
            bw = remaining
        d.rectangle([cx, y, cx + bw - gap, y + h], fill=_c(colors[i % len(colors)]))
        cx += bw
        remaining -= bw


def scanlines(d, x, y, w, h, color=CYAN, spacing=4, alpha=4, s=SS):
    """Very subtle horizontal scanlines."""
    x, y, w, h, spacing = [v * s for v in (x, y, w, h, spacing)]
    c = _c(color, alpha)
    for sy in range(y, y + h, spacing):
        d.line([(x, sy), (x + w, sy)], fill=c, width=1)


# ─── PCARS Screen Background Template ────────────────────────────────────────

def pcars_frame_bg(w, h, top_h=26, **_kwargs):
    """Solid frosty-black background with clean top bar for status icons.
    No sidebars, no bottom bars, no elbows — LVGL-style minimalism.
    Returns a supersampled image — call ss_finish() on result.
    """
    img, d = ss_start(w, h, BG)
    s = SS

    # ── Clean top bar — solid dark panel for status icons ──
    d.rectangle([0, 0, w * s, top_h * s], fill=_c(PANEL))

    # Subtle 1px separator line below status bar
    d.rectangle([0, (top_h - 1) * s, w * s, top_h * s], fill=_c(EDGE, 35))

    return img


def pcars_section_bg(w, h, section_color, section_dark=None, top_h=26,
                     sidebar_w=6, bottom_h=4):
    """PCARS section background with colored structural identity.

    Each section gets three identifying elements:
    1. Left edge bar — sidebar_w px wide, section accent color, full content height
    2. Top separator — 1px, section-colored (alpha 50)
    3. Bottom strip — bottom_h px, section dark color (alpha 40)

    Returns a supersampled image — call ss_finish() on result.
    """
    if section_dark is None:
        section_dark = tuple(max(int(c * 0.5), 0) for c in section_color)

    img, d = ss_start(w, h, BG)
    s = SS

    # Status bar (same as generic)
    d.rectangle([0, 0, w * s, top_h * s], fill=_c(PANEL))

    # Section-colored separator line below status bar
    d.rectangle([0, (top_h - 1) * s, w * s, top_h * s],
                fill=_c(section_color, 50))

    # Left sidebar bar — PCARS structural accent
    bar_top = top_h * s
    bar_bot = (h - bottom_h) * s
    bar_right = sidebar_w * s
    d.rectangle([0, bar_top, bar_right, bar_bot], fill=_c(section_color))

    # Bottom accent strip
    d.rectangle([0, (h - bottom_h) * s, w * s, h * s],
                fill=_c(section_dark, 40))
    # Brighter 1px line at top of bottom strip
    d.rectangle([0, (h - bottom_h) * s, w * s, (h - bottom_h + 1) * s],
                fill=_c(section_color, 25))

    return img


# ─── Dashboard ───────────────────────────────────────────────────────────────

def gen_dashboard():
    """Main dashboard — dark columns with colored accent bars + full-color active state.
    Inactive: near-black column, section-colored icon/label, thin accent bar at bottom.
    Active: full section-color via highlight recolor_palette, black icon/text.
    """
    ensure_dir("dashboard")

    W, H = 480, 222
    TOP_BAR = 26       # status bar height
    COL_W = 96         # 480 / 5 = 96px per column
    COL_H = H - TOP_BAR  # 196px column height
    s = SS

    col_accents = [SEC_ALERTS, SEC_PAYLOADS, SEC_RECON, SEC_PINEAP, SEC_SETTINGS]

    ACCENT_H = 3       # thin colored accent bar at very bottom
    LABEL_H = 28       # label area at bottom of column

    # ── Background: dark base + top bar + 5 dark columns + colored accent bars ──
    img, d = ss_start(W, H, BG)

    # Top bar
    d.rectangle([0, 0, W * s, TOP_BAR * s], fill=_c(PANEL))
    d.rectangle([0, (TOP_BAR - 1) * s, W * s, TOP_BAR * s], fill=_c(EDGE, 25))

    # Draw 5 near-black columns with thin section accent at bottom
    for ci in range(5):
        cx = ci * COL_W
        accent = col_accents[ci]

        # Very subtle section tint over dark base
        col_tint = tuple(min(int(BG[i] + accent[i] * 0.05), 255) for i in range(3))
        d.rectangle([cx * s, TOP_BAR * s, (cx + COL_W) * s, H * s],
                    fill=_c(col_tint, 255))

        # Thin colored accent bar at very bottom
        d.rectangle([cx * s, (H - ACCENT_H) * s, (cx + COL_W) * s, H * s],
                    fill=_c(accent, 110))

        # 1px dark separator between columns
        if ci > 0:
            d.rectangle([cx * s, TOP_BAR * s, (cx + 1) * s, H * s],
                        fill=_c(BG, 255))

    result = ss_finish(img, W, H)
    save(result, "dashboard/pcars_bg.png")

    # ── Menu item panel — transparent (columns are in background) ──
    img = new(COL_W, COL_H)
    save(img, "dashboard/item_bg.png")

    # ── Highlight — white for recolor_palette per-section tinting (96x196) ──
    hw, hh = COL_W, COL_H
    img, d = ss_start(hw, hh)

    # Full column fill — white body (recolor_palette maps white → section color)
    d.rectangle([0, 0, hw * s, hh * s], fill=_c((255, 255, 255), 245))

    # Slightly dimmer label area at bottom for depth
    d.rectangle([0, (hh - LABEL_H) * s, hw * s, hh * s],
                fill=_c((220, 220, 220), 235))

    # Thin bright line above label area
    d.rectangle([0, (hh - LABEL_H) * s, hw * s, (hh - LABEL_H + 1) * s],
                fill=_c((255, 255, 255), 255))

    result = ss_finish(img, hw, hh)
    save(result, "dashboard/highlight.png")

    # ── Breadcrumb dots (hollow + filled) ──
    dot_size = 8
    # Hollow dot — outline circle
    img, d = ss_start(dot_size, dot_size)
    d.ellipse([1 * s, 1 * s, (dot_size - 1) * s, (dot_size - 1) * s],
              outline=_c((255, 255, 255), 255), width=2 * s)
    result = ss_finish(img, dot_size, dot_size)
    save(result, "dashboard/dot_hollow.png")

    # Filled dot — solid circle
    img, d = ss_start(dot_size, dot_size)
    d.ellipse([1 * s, 1 * s, (dot_size - 1) * s, (dot_size - 1) * s],
              fill=_c((255, 255, 255), 255))
    result = ss_finish(img, dot_size, dot_size)
    save(result, "dashboard/dot_filled.png")

    # ── Nav Icons — all 64x64 ──
    ICON_SIZE = 64

    # Payloads Icon — TOS Type 2 Phaser (classic series, side profile facing right)
    rw, rh = ICON_SIZE, ICON_SIZE
    img, d = ss_start(rw, rh)
    wc = _c((255, 255, 255), 255)
    wd = _c((255, 255, 255), 160)
    wdim = _c((255, 255, 255), 80)
    wfill = _c((255, 255, 255), 45)

    # TOS Type 2 — boxy upper body, cylindrical emitter, pistol grip
    # The body is blocky/angular, emitter is a cylinder with pointed tip

    # Main body (boxy upper section)
    body_pts = [
        (8, 14),    # rear top-left of body
        (44, 10),   # front top (slight upward taper)
        (44, 28),   # front of body before emitter
        (32, 32),   # underside step where grip meets
        (34, 56),   # grip bottom-front
        (22, 58),   # grip bottom-rear (flat base)
        (20, 32),   # grip top-rear
        (8, 30),    # rear bottom of body
    ]
    scaled = [(x * s, y * s) for x, y in body_pts]
    d.polygon(scaled, fill=wfill, outline=wc)
    for i in range(len(scaled)):
        j = (i + 1) % len(scaled)
        d.line([scaled[i], scaled[j]], fill=wc, width=2 * s)

    # Type 1 phaser on top (the small unit that sits on the body)
    type1_pts = [
        (14, 14),   # rear-left of type 1
        (38, 10),   # front-right of type 1
        (38, 6),    # top front
        (14, 8),    # top rear
    ]
    t1_scaled = [(x * s, y * s) for x, y in type1_pts]
    d.polygon(t1_scaled, fill=_c((255, 255, 255), 35), outline=wd)
    for i in range(len(t1_scaled)):
        j = (i + 1) % len(t1_scaled)
        d.line([t1_scaled[i], t1_scaled[j]], fill=wd, width=1 * s)
    # Grid/mesh texture on type 1 (the emitter grid)
    for gx in range(18, 36, 4):
        d.line([(gx * s, 7 * s), (gx * s, 13 * s)], fill=wdim, width=1 * s)

    # Emitter nozzle — cylinder extending from front of body
    # Cylinder body
    d.rectangle([44 * s, 15 * s, 56 * s, 25 * s], fill=wfill, outline=wc)
    d.line([(44 * s, 15 * s), (56 * s, 15 * s)], fill=wc, width=2 * s)
    d.line([(44 * s, 25 * s), (56 * s, 25 * s)], fill=wc, width=2 * s)
    d.line([(56 * s, 15 * s), (56 * s, 25 * s)], fill=wc, width=2 * s)
    # Cylinder rings (detail lines)
    for rx in [47, 50, 53]:
        d.line([(rx * s, 15 * s), (rx * s, 25 * s)], fill=wdim, width=1 * s)

    # Emitter tip — pointed
    d.polygon([(56 * s, 16 * s), (63 * s, 20 * s), (56 * s, 24 * s)],
              fill=wfill, outline=wc)
    d.line([(56 * s, 16 * s), (63 * s, 20 * s)], fill=wc, width=2 * s)
    d.line([(63 * s, 20 * s), (56 * s, 24 * s)], fill=wc, width=2 * s)

    # Emitter glow dot
    d.ellipse([61 * s, 18 * s, 65 * s, 22 * s], fill=wc)

    # Body detail — horizontal accent line
    d.line([(10 * s, 22 * s), (44 * s, 20 * s)], fill=wd, width=1 * s)

    # Dial/knob on top rear — small circle
    d.ellipse([10 * s, 4 * s, 16 * s, 10 * s], outline=wd, width=1 * s)
    d.ellipse([12 * s, 6 * s, 14 * s, 8 * s], fill=wc)

    # Trigger guard
    d.arc([22 * s, 34 * s, 34 * s, 44 * s],
          start=0, end=180, fill=wd, width=1 * s)

    # Grip texture — vertical ridges (TOS style)
    for gy in range(38, 55, 3):
        d.line([(23 * s, gy * s), (33 * s, (gy + 1) * s)], fill=wdim, width=1 * s)

    result = ss_finish(img, rw, rh)
    save(result, "dashboard/payloads.png")

    # Recon Icon — use the alerts_original icon (moved from alerts section), minimal padding
    alerts_orig = os.path.join(ASSETS_DIR, "dashboard", "alerts_original.png")
    if os.path.exists(alerts_orig):
        icon = Image.open(alerts_orig).convert("RGBA")
        bbox = icon.getbbox()
        if bbox:
            icon = icon.crop(bbox)
        target = int(ICON_SIZE * 0.90)
        iw, ih = icon.size
        sc = min(target / iw, target / ih)
        nw, nh = int(iw * sc), int(ih * sc)
        icon = icon.resize((nw, nh), Image.LANCZOS)
        result = new(ICON_SIZE, ICON_SIZE)
        result.paste(icon, ((ICON_SIZE - nw) // 2, (ICON_SIZE - nh) // 2), icon)
        save(result, "dashboard/recon.png")
    else:
        img = new(ICON_SIZE, ICON_SIZE)
        d = ImageDraw.Draw(img)
        d.ellipse([4, 4, 60, 60], outline=(255, 255, 255, 180), width=2)
        save(img, "dashboard/recon.png")

    # Alerts Icon — Subspace Antenna (bold dish with strong signal arcs)
    rw, rh = ICON_SIZE, ICON_SIZE
    img, d = ss_start(rw, rh)
    wc = _c((255, 255, 255), 255)
    wd = _c((255, 255, 255), 180)
    wdim = _c((255, 255, 255), 100)

    # Support mast — thick angled line from bottom-right to dish center
    mast_bx, mast_by = 46, 58
    dish_cx, dish_cy = 22, 32
    d.line([(mast_bx * s, mast_by * s), (dish_cx * s, dish_cy * s)],
           fill=wc, width=3 * s)

    # Base platform — solid horizontal bar at bottom
    d.rounded_rectangle(
        [34 * s, 55 * s, 58 * s, 60 * s],
        radius=2 * s, fill=wc
    )

    # Parabolic dish — bold thick arc
    dish_r = 20
    d.arc([(dish_cx - dish_r) * s, (dish_cy - dish_r) * s,
           (dish_cx + dish_r) * s, (dish_cy + dish_r) * s],
          start=145, end=295, fill=wc, width=4 * s)

    # Feed horn — larger dot at focal point
    fx, fy = dish_cx + 10, dish_cy - 3
    d.ellipse([(fx - 3) * s, (fy - 3) * s, (fx + 3) * s, (fy + 3) * s],
              fill=wc)
    # Strut from dish to feed horn
    d.line([(dish_cx * s, dish_cy * s), (fx * s, fy * s)],
           fill=wc, width=2 * s)

    # Signal arcs — 4 arcs radiating outward, bolder, wider sweep
    for arc_r, arc_a in [(9, 220), (15, 180), (21, 140), (27, 100)]:
        d.arc([(fx - arc_r) * s, (fy - arc_r) * s,
               (fx + arc_r) * s, (fy + arc_r) * s],
              start=275, end=345, fill=_c((255, 255, 255), arc_a),
              width=2 * s)

    result = ss_finish(img, rw, rh)
    save(result, "dashboard/alerts.png")

    # PineAP Icon — stellar map / star chart (moved from recon)
    pw, ph = ICON_SIZE, ICON_SIZE
    img, d = ss_start(pw, ph)
    wc = _c((255, 255, 255), 255)
    wdim = _c((255, 255, 255), 140)

    # Grid lines (faint)
    for gx in [16, 32, 48]:
        d.line([(gx * s, 4 * s), (gx * s, 60 * s)], fill=wdim, width=1 * s)
    for gy in [16, 32, 48]:
        d.line([(4 * s, gy * s), (60 * s, gy * s)], fill=wdim, width=1 * s)

    # Stars — scattered dots of varying size
    for sx, sy in [(12, 10), (50, 14), (26, 28), (44, 42), (10, 52)]:
        d.ellipse([sx * s, sy * s, (sx + 5) * s, (sy + 5) * s], fill=wc)
    for sx, sy in [(36, 12), (18, 44), (52, 30), (8, 30), (40, 54)]:
        d.ellipse([sx * s, sy * s, (sx + 3) * s, (sy + 3) * s], fill=wc)
    for sx, sy in [(22, 18), (46, 22), (14, 38), (34, 48), (56, 48), (28, 8), (54, 56)]:
        d.ellipse([sx * s, sy * s, (sx + 2) * s, (sy + 2) * s], fill=wc)

    # Constellation lines
    d.line([(14 * s, 12 * s), (28 * s, 30 * s)], fill=wdim, width=1 * s)
    d.line([(28 * s, 30 * s), (46 * s, 44 * s)], fill=wdim, width=1 * s)
    d.line([(52 * s, 16 * s), (28 * s, 30 * s)], fill=wdim, width=1 * s)

    # Outer border — thicker to match other icons
    d.rounded_rectangle(
        [2 * s, 2 * s, 62 * s, 62 * s],
        radius=4 * s, outline=wc, width=4 * s
    )

    result = ss_finish(img, pw, ph)
    save(result, "dashboard/pineap.png")

    # Settings Icon — combadge (chevron arrowhead over oval)
    rw, rh = ICON_SIZE, ICON_SIZE
    img, d = ss_start(rw, rh)
    wc = _c((255, 255, 255), 255)
    wd = _c((255, 255, 255), 160)
    wdim = _c((255, 255, 255), 60)

    # Horizontal oval (backing plate) — centered, wider than tall
    oval_cx, oval_cy = 32, 38
    oval_rx, oval_ry = 24, 12
    d.ellipse([(oval_cx - oval_rx) * s, (oval_cy - oval_ry) * s,
               (oval_cx + oval_rx) * s, (oval_cy + oval_ry) * s],
              fill=_c((255, 255, 255), 35), outline=wd, width=2 * s)

    # Chevron/arrowhead — sharp point at top, two swept wings, point at bottom
    # Top point
    tx, ty = 32, 4
    # Left wing tip
    lx, ly = 10, 44
    # Right wing tip
    rx, ry = 54, 44
    # Inner notch (bottom center of chevron)
    nx, ny = 32, 36
    # Bottom point
    bx, by = 32, 56

    # Draw chevron as two filled triangles (left half + right half)
    # Left half: top → left wing → inner notch
    d.polygon([(tx * s, ty * s), (lx * s, ly * s), (nx * s, ny * s)],
              fill=_c((255, 255, 255), 50), outline=wc)
    # Right half: top → right wing → inner notch
    d.polygon([(tx * s, ty * s), (rx * s, ry * s), (nx * s, ny * s)],
              fill=_c((255, 255, 255), 50), outline=wc)
    # Bottom spike: inner notch left → bottom point → inner notch right
    d.polygon([(nx * s - 6 * s, ny * s), (bx * s, by * s), (nx * s + 6 * s, ny * s)],
              fill=_c((255, 255, 255), 50), outline=wc)

    # Thicken the outline edges for clarity at small size
    d.line([(tx * s, ty * s), (lx * s, ly * s)], fill=wc, width=2 * s)
    d.line([(tx * s, ty * s), (rx * s, ry * s)], fill=wc, width=2 * s)
    d.line([(lx * s, ly * s), (nx * s, ny * s)], fill=wc, width=2 * s)
    d.line([(rx * s, ry * s), (nx * s, ny * s)], fill=wc, width=2 * s)
    d.line([(nx * s - 6 * s, ny * s), (bx * s, by * s)], fill=wc, width=2 * s)
    d.line([(nx * s + 6 * s, ny * s), (bx * s, by * s)], fill=wc, width=2 * s)

    result = ss_finish(img, rw, rh)
    save(result, "dashboard/settings.png")

    # Resize alerts icon — 15% padding
    alerts_path = os.path.join(ASSETS_DIR, "dashboard", "alerts.png")
    if os.path.exists(alerts_path):
        icon = Image.open(alerts_path).convert("RGBA")
        inner = int(ICON_SIZE * 0.85)
        icon = icon.resize((inner, inner), Image.LANCZOS)
        result = new(ICON_SIZE, ICON_SIZE)
        pad = (ICON_SIZE - inner) // 2
        result.paste(icon, (pad, pad), icon)
        result.save(alerts_path, "PNG", optimize=True)

    # Shrink pineap icon by 15% — re-render on padded canvas
    pineap_path = os.path.join(ASSETS_DIR, "dashboard", "pineap.png")
    if os.path.exists(pineap_path):
        icon = Image.open(pineap_path).convert("RGBA")
        inner = int(ICON_SIZE * 0.85)
        icon = icon.resize((inner, inner), Image.LANCZOS)
        result = new(ICON_SIZE, ICON_SIZE)
        pad = (ICON_SIZE - inner) // 2
        result.paste(icon, (pad, pad), icon)
        save(result, "dashboard/pineap.png")

    # ── Labels — crisp text, centered in column-width image ──
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 14)

    label_names = ["ALERTS", "PAYLOADS", "RECON", "PINEAP", "SETTINGS"]
    for label in label_names:
        bbox = font.getbbox(label)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        # Full column-width image — text centered within, x=0 in JSON
        img = Image.new("RGBA", (COL_W, th + 4), T)
        d = ImageDraw.Draw(img)
        tx = (COL_W - tw) // 2 - bbox[0]
        ty = 2 - bbox[1]
        d.text((tx, ty), label, fill=(255, 255, 255, 255), font=font)
        # Threshold alpha — remove anti-aliasing for crisp edges
        r, g, b, a = img.split()
        a = a.point(lambda p: 255 if p > 96 else 0)
        img = Image.merge("RGBA", (r, g, b, a))
        save(img, f"dashboard/label_{label.lower()}.png")

    # ── Deck labels — subtle section identifiers below main labels ──
    deck_font = ImageFont.truetype(font_path, 10)
    deck_map = [
        ("alerts", "DECK 1"), ("payloads", "DECK 2"), ("recon", "DECK 3"),
        ("pineap", "DECK 4"), ("settings", "DECK 5"),
    ]
    for section, deck_text in deck_map:
        bbox = deck_font.getbbox(deck_text)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        img = Image.new("RGBA", (COL_W, th + 4), T)
        d = ImageDraw.Draw(img)
        tx = (COL_W - tw) // 2 - bbox[0]
        ty = 2 - bbox[1]
        d.text((tx, ty), deck_text, fill=(255, 255, 255, 255), font=deck_font)
        r, g, b, a = img.split()
        a = a.point(lambda p: 255 if p > 96 else 0)
        img = Image.merge("RGBA", (r, g, b, a))
        save(img, f"dashboard/deck_{section}.png")


# ─── Status Bar ──────────────────────────────────────────────────────────────

def gen_statusbar():
    """Status bar icons — clean, minimal indicators on dark background."""
    ensure_dir("statusbar")
    s = SS

    # ── Battery (38x20) — segmented bars ──
    bat_specs = [
        ("dashboard_battery_charge_25", 1, YELLOW),
        ("dashboard_battery_charge_50", 2, EDGE),
        ("dashboard_battery_charge_75", 3, CYAN),
        ("dashboard_battery_charge_100", 4, GREEN),
        ("dashboard_battery_full", 4, GREEN),
        ("dashboard_battery_text", 0, GRAY),
    ]
    for name, segs, color in bat_specs:
        img, d = ss_start(38, 20)
        rrect(d, (0, 2, 33, 18), outline=DARK_GRAY, radius=2, width=1)
        d.rectangle([34*s, 7*s, 37*s, 13*s], fill=_c(DARK_GRAY))
        for si in range(4):
            sx = (2 + si * 8) * s
            if si < segs:
                d.rectangle([sx, 4*s, sx + 6*s, 16*s], fill=_c(color))
            else:
                d.rectangle([sx, 4*s, sx + 6*s, 16*s], fill=_c(DARK_GRAY, 30))
        save(ss_finish(img, 38, 20), f"statusbar/{name}.png")

    # ── Brightness (20x20) ──
    for name, level in [("dashboard_brightness_2", 2), ("dashboard_brightness_3", 3),
                        ("dashboard_brightness_5", 5), ("dashboard_brightness_7", 7),
                        ("dashboard_brightness_8", 8)]:
        img, d = ss_start(20, 20)
        frac = level / 8.0
        col = _c((int(60 + frac * 155), int(60 + frac * 155), int(80 + frac * 130)))
        d.ellipse([7*s, 7*s, 13*s, 13*s], fill=col)
        rays = min(level, 8)
        for r in range(rays):
            a = (r * 360 / 8) * math.pi / 180
            x1, y1 = 10*s + int(4*s * math.cos(a)), 10*s + int(4*s * math.sin(a))
            x2, y2 = 10*s + int(8*s * math.cos(a)), 10*s + int(8*s * math.sin(a))
            d.line([(x1, y1), (x2, y2)], fill=col, width=s)
        save(ss_finish(img, 20, 20), f"statusbar/{name}.png")

    # ── Bluetooth (20x20) ──
    img, d = ss_start(20, 20)
    pts = [(10, 2), (15, 6), (5, 14), (10, 18), (15, 14), (5, 6)]
    for i in range(len(pts) - 1):
        d.line([(pts[i][0]*s, pts[i][1]*s), (pts[i+1][0]*s, pts[i+1][1]*s)],
               fill=_c(BLUE), width=s)
    d.line([(10*s, 2*s), (10*s, 18*s)], fill=_c(BLUE), width=s)
    save(ss_finish(img, 20, 20), "statusbar/bluetooth.png")

    # ── Volume (variable width x 20) ──
    def speaker(d, color, s):
        d.polygon([(3*s, 7*s), (6*s, 7*s), (10*s, 3*s),
                   (10*s, 17*s), (6*s, 13*s), (3*s, 13*s)], fill=_c(color))

    for name, ww, waves in [("volume_low", 17, 1), ("volume_medium", 17, 2),
                            ("volume_high", 21, 3)]:
        img, d = ss_start(ww, 20)
        speaker(d, SOFT_W, s)
        for i in range(1, waves + 1):
            r = (3 + i * 3) * s
            d.arc([10*s, (10 - r // s)*s, 10*s + r*2, (10 + r // s)*s],
                  -50, 50, fill=_c(SOFT_W), width=s)
        save(ss_finish(img, ww, 20), f"statusbar/{name}.png")

    # ── Mute (20x20) ──
    img, d = ss_start(20, 20)
    speaker(d, GRAY, s)
    d.line([(2*s, 3*s), (17*s, 17*s)], fill=_c(RED), width=2*s)
    save(ss_finish(img, 20, 20), "statusbar/mute.png")

    # ── Vibrate (24x17) ──
    img, d = ss_start(24, 17)
    rrect(d, (7, 1, 17, 16), outline=SOFT_W, radius=2, width=1)
    d.arc([1*s, 4*s, 7*s, 13*s], 100, 260, fill=_c(SOFT_W), width=s)
    d.arc([17*s, 4*s, 23*s, 13*s], 280, 80, fill=_c(SOFT_W), width=s)
    save(ss_finish(img, 24, 17), "statusbar/vibrate.png")

    # ── GHz indicators (20x20 or 20x22) ──
    ghz = [("ghz_2", "2", EDGE, 20), ("ghz_5", "5", CYAN, 20),
           ("ghz_6", "6", TEAL, 20), ("ghz_25", "25", EDGE, 20),
           ("ghz_26", "26", EDGE, 22), ("ghz_56", "56", CYAN, 20),
           ("ghz_256", "A", GREEN, 20), ("ghz_off", "-", GRAY, 20)]
    for name, _label, color, hh in ghz:
        img, d = ss_start(20, hh)
        rrect(d, (0, 0, 19, hh - 1), fill=(color[0], color[1], color[2], 30),
              outline=color, radius=3, width=1)
        save(ss_finish(img, 20, hh), f"statusbar/{name}.png")

    # ── GPS (21x21) ──
    img, d = ss_start(21, 21)
    cx, cy = 10*s, 10*s
    d.ellipse([cx-7*s, cy-7*s, cx+7*s, cy+7*s], outline=_c(CYAN), width=s)
    d.ellipse([cx-3*s, cy-3*s, cx+3*s, cy+3*s], fill=_c(CYAN))
    for dx, dy, dx2, dy2 in [(0, -9, 0, -4), (0, 4, 0, 9), (-9, 0, -4, 0), (4, 0, 9, 0)]:
        d.line([(cx+dx*s, cy+dy*s), (cx+dx2*s, cy+dy2*s)], fill=_c(CYAN), width=s)
    save(ss_finish(img, 21, 21), "statusbar/gps.png")

    # ── Database (21x19) ──
    img, d = ss_start(21, 19)
    for cy in [3, 8, 13]:
        d.ellipse([3*s, cy*s, 18*s, (cy+5)*s], outline=_c(FRAME_L), width=s)
    d.line([(3*s, 5*s), (3*s, 15*s)], fill=_c(FRAME_L), width=s)
    d.line([(18*s, 5*s), (18*s, 15*s)], fill=_c(FRAME_L), width=s)
    save(ss_finish(img, 21, 19), "statusbar/database.png")

    # ── PCAP (20x21) ──
    img, d = ss_start(20, 21)
    rrect(d, (2, 0, 17, 20), outline=TEAL, radius=2, width=1)
    for ly in [5, 9, 13]:
        d.line([(5*s, ly*s), (14*s, ly*s)], fill=_c(TEAL), width=s)
    save(ss_finish(img, 20, 21), "statusbar/pcap.png")

    # ── Wigle (28x21) ──
    img, d = ss_start(28, 21)
    d.ellipse([4*s, 1*s, 24*s, 20*s], outline=_c(TEAL), width=s)
    d.ellipse([10*s, 1*s, 18*s, 20*s], outline=_c(TEAL), width=s)
    d.line([(4*s, 10*s), (24*s, 10*s)], fill=_c(TEAL), width=s)
    save(ss_finish(img, 28, 21), "statusbar/wigle.png")


# ─── Spinner ─────────────────────────────────────────────────────────────────

def gen_spinner():
    """Loading spinner — warp core pulse rings."""
    ensure_dir("spinner")
    s = SS
    W, H = 220, 156

    for frame in range(1, 5):
        img, d = ss_start(W, H)
        cx, cy = W * s // 2, H * s // 2
        ba = (frame - 1) * 90  # rotation angle

        # Outer ring — dim structural
        r1 = min(cx, cy) - 6 * s
        d.arc([cx - r1, cy - r1, cx + r1, cy + r1],
              0, 360, fill=_c(FRAME_D, 60), width=2 * s)

        # Sweeping arc — bright, rotates per frame
        d.arc([cx - r1, cy - r1, cx + r1, cy + r1],
              ba, ba + 90, fill=_c(CYAN, 200), width=3 * s)
        # Trail
        d.arc([cx - r1, cy - r1, cx + r1, cy + r1],
              ba - 30, ba, fill=_c(CYAN, 80), width=2 * s)

        # Middle ring — pulsing
        r2 = r1 - 16 * s
        pulse_alpha = [120, 180, 220, 160][frame - 1]
        d.arc([cx - r2, cy - r2, cx + r2, cy + r2],
              0, 360, fill=_c(EDGE, pulse_alpha), width=2 * s)

        # Inner ring — counter-rotating sweep
        r3 = r2 - 14 * s
        ba2 = 360 - ba  # counter-rotate
        d.arc([cx - r3, cy - r3, cx + r3, cy + r3],
              ba2, ba2 + 60, fill=_c(LT_BLUE, 160), width=2 * s)

        # Center core — pulsing dot
        pr = (4 + frame) * s
        d.ellipse([cx - pr, cy - pr, cx + pr, cy + pr],
                  fill=_c(CYAN, 80 + frame * 30))
        # Bright center pip
        d.ellipse([cx - 3 * s, cy - 3 * s, cx + 3 * s, cy + 3 * s],
                  fill=_c(WHITE, 200))

        result = ss_finish(img, W, H)
        result = glow(result, radius=3, intensity=0.3)
        save(result, f"spinner/spinner{frame}.png")


# ─── Boot Animation ──────────────────────────────────────────────────────────

def gen_boot():
    """Boot animation — PCARS warp initialization.
    Stars start sharp, progressively streak into warp trails with blue glow.
    All text WHITE. 16 frames total (8 messages × 2 frames each).
    Doubled frame count so one full loop fills the entire boot time.
    """
    ensure_dir("boot_animation")
    import random
    random.seed(42)  # deterministic star field

    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    bold_path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
    try:
        font_lg = ImageFont.truetype(bold_path, 20)
        font_sm = ImageFont.truetype(font_path, 12)
    except Exception:
        font_lg = ImageFont.load_default()
        font_sm = font_lg

    W, H = 480, 222
    vcx, vcy = W // 2, H // 2  # vanishing point (screen center)

    # Star field — random positions with brightness
    stars = []
    for _ in range(80):
        sx = random.randint(5, W - 5)
        sy = random.randint(5, H - 5)
        bright = random.randint(100, 255)
        size = random.choice([1, 1, 1, 2, 2, 3])  # mostly small
        stars.append((sx, sy, bright, size))

    # Subtle structural light beams (diagonal streaks in background)
    beams = []
    for _ in range(8):
        bx = random.randint(0, W)
        by = random.randint(0, H)
        angle = random.uniform(-0.3, 0.3)  # near-horizontal
        length = random.randint(60, 200)
        bright = random.randint(15, 40)
        beams.append((bx, by, angle, length, bright))

    # Messages — 8 messages now (doubled from 4), final always definitive
    random.seed(int(random.random() * 10000))
    status_pool = [
        "CHARGING PINEAPPLE THRUSTERS",
        "INITIALIZING WARP CORE",
        "CALIBRATING SIGNAL ARRAYS",
        "ENGAGING STEALTH PROTOCOLS",
        "PINEAP ENGINE PRIMING",
        "SCANNING SUBSPACE FREQUENCIES",
        "ARMING PAYLOAD BANKS",
        "SYNCING TACTICAL SYSTEMS",
        "LOADING ATTACK VECTORS",
        "BRIDGING SIGNAL HARMONICS",
        "MODULATING SHIELD FREQUENCY",
        "ALIGNING SENSOR PALETTES",
        "COFFEE... BLACK",
    ]
    diag_pool = [
        "PCARS v2.0 // MAIN REACTOR STARTUP",
        "MT7628AN 580MHz // CORE STABLE",
        "WARP CORE ALIGNED // TRI-BAND 6E",
        "SHIELD HARMONICS CALIBRATED",
        "PINEAP v8 // WEAPONS HOT",
        "RF SUBSYSTEMS NOMINAL",
        "TACTICAL DISPLAY ONLINE",
        "RECON ARRAYS SYNCHRONIZED",
        "DEFLECTOR GRID ACTIVE",
        "ALL STATIONS REPORTING",
        "NAVIGATIONAL ARRAY LOCKED",
        "COMM BADGES SYNCED",
    ]
    random.shuffle(status_pool)
    random.shuffle(diag_pool)
    status_lines = status_pool[:8]
    diag_lines = diag_pool[:8]
    status_lines[7] = "ALL SYSTEMS OPERATIONAL"
    diag_lines[7] = "WIFI PINEAPPLE PAGER ONLINE"

    NUM_MSGS = 8
    FRAMES_PER_MSG = 2
    TOTAL_FRAMES = NUM_MSGS * FRAMES_PER_MSG  # 16

    # 16 frames: 8 messages × 2 frames each
    frame_num = 0
    for msg_idx in range(NUM_MSGS):
        for sub in range(FRAMES_PER_MSG):
            frame_num += 1
            progress = frame_num / float(TOTAL_FRAMES)  # 0.0625 → 1.0

            # Warp: frame 1 static, frame 2 gets visible drift, smooth accel to full
            if frame_num <= 1:
                warp = 0.0
            elif frame_num == 2:
                warp = 0.03  # just enough for visible star drift
            else:
                # Smooth acceleration from frame 3 to 16
                t = (frame_num - 2) / (TOTAL_FRAMES - 2)  # 0→1 over frames 3-16
                warp = 0.03 + 0.97 * (t ** 2.2)

            # ── Star/beam layer (will be blurred) ──
            bg_layer = Image.new("RGBA", (W, H), (*BG, 255))
            sd = ImageDraw.Draw(bg_layer)

            # Light beams — get longer and blurrier with warp
            for bx, by, angle, length, bright in beams:
                beam_len = int(length * (1 + warp * 4))
                import math as _math
                ex = bx + int(_math.cos(angle) * beam_len)
                ey = by + int(_math.sin(angle) * beam_len)
                beam_bright = int(bright * (1 + warp * 3))
                sd.line([(bx, by), (ex, ey)],
                        fill=(80, 120, 200, min(beam_bright, 100)), width=1)

            # Stars — dots → streaks radiating from vanishing point
            streak_max = int(warp * 120)  # 0px → 120px streaks

            for sx, sy, bright, sz in stars:
                if streak_max < 2:
                    # Sharp pinpoint star
                    if sz == 1:
                        sd.point([(sx, sy)], fill=(255, 255, 255, bright))
                    else:
                        sd.ellipse([sx - sz // 2, sy - sz // 2,
                                    sx + sz // 2, sy + sz // 2],
                                   fill=(255, 255, 255, bright))
                else:
                    # Streak along ray from vanishing point through star
                    dx = sx - vcx
                    dy = sy - vcy
                    dist = max(1.0, (dx * dx + dy * dy) ** 0.5)
                    ndx = dx / dist
                    ndy = dy / dist
                    # Streak length proportional to distance from center
                    slen = int(streak_max * (dist / (W * 0.5)))
                    ex = sx + int(ndx * slen)
                    ey = sy + int(ndy * slen)
                    # Streak gets brighter as warp increases
                    sb = min(255, int(bright * (1 + warp * 0.8)))
                    # Blue-shift: stars go from white → deep blue as they streak
                    blue_t = min(1.0, warp * 1.5)
                    # Final frames go fully saturated blue
                    if warp > 0.8:
                        final_t = (warp - 0.8) / 0.2  # 0→1 over last 20% of warp
                        sr = int(200 * (1 - blue_t * 0.5) + 100 * blue_t)
                        sr = int(sr * (1 - final_t * 0.7))  # crush red
                        sg = int(220 * (1 - blue_t * 0.3) + 160 * blue_t)
                        sg = int(sg * (1 - final_t * 0.4))  # reduce green
                        sbb = 255
                    else:
                        sr = int(200 * (1 - blue_t * 0.5) + 100 * blue_t)
                        sg = int(220 * (1 - blue_t * 0.3) + 160 * blue_t)
                        sbb = 255
                    sd.line([(sx, sy), (ex, ey)],
                            fill=(sr, sg, sbb, sb), width=max(1, sz))

            # Progressive motion blur on star/beam layer
            blur_r = warp * 5.0  # 0 → 5px blur radius
            if blur_r > 0.5:
                bg_layer = bg_layer.filter(
                    ImageFilter.GaussianBlur(radius=blur_r))

            # Blue glow layer — composited on top of blurred stars
            if warp > 0.1:
                glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                gd = ImageDraw.Draw(glow_layer)
                # Glow intensity ramps up, extra strong in final frames
                glow_mult = 1.0
                if warp > 0.8:
                    glow_mult = 1.0 + 2.0 * ((warp - 0.8) / 0.2)  # 1.0 → 3.0
                for sx, sy, bright, sz in stars:
                    if streak_max >= 2:
                        dx = sx - vcx
                        dy = sy - vcy
                        dist = max(1.0, (dx * dx + dy * dy) ** 0.5)
                        ndx = dx / dist
                        ndy = dy / dist
                        slen = int(streak_max * (dist / (W * 0.5)))
                        ex = sx + int(ndx * slen)
                        ey = sy + int(ndy * slen)
                        glow_a = int(min(120, warp * 120 * glow_mult))
                        gd.line([(sx, sy), (ex, ey)],
                                fill=(60, 120, 255, glow_a),
                                width=max(2, sz + 2))
                # Blur the glow for soft bloom
                glow_layer = glow_layer.filter(
                    ImageFilter.GaussianBlur(radius=max(2, warp * 6)))
                bg_layer = Image.alpha_composite(bg_layer, glow_layer)

            # Final blue blast — full-frame blue wash on last 3 frames
            if warp > 0.7:
                blast_t = (warp - 0.7) / 0.3  # 0→1 over final 30%
                blast_a = int(blast_t * 45)  # up to alpha 45 blue overlay
                blue_wash = Image.new("RGBA", (W, H), (20, 60, 200, blast_a))
                bg_layer = Image.alpha_composite(bg_layer, blue_wash)

            # ── Compose final frame ──
            result = bg_layer

            # Draw text sharp on top — ALL WHITE
            td = ImageDraw.Draw(result)

            # ── Progress dots — 5 section-colored dots, fill as boot progresses ──
            dot_colors = [SEC_ALERTS, SEC_PAYLOADS, SEC_RECON, SEC_PINEAP, SEC_SETTINGS]
            # msg_idx thresholds at which each dot fills
            dot_thresholds = [0, 1, 3, 4, 5]
            dot_r = 4  # radius
            dot_spacing = 20  # center-to-center
            dot_y = H // 2 - 44  # above status text
            dot_start_x = W // 2 - (4 * dot_spacing) // 2  # center 5 dots

            for di in range(5):
                dx = dot_start_x + di * dot_spacing
                if msg_idx >= dot_thresholds[di]:
                    # Filled dot — section color
                    td.ellipse([dx - dot_r, dot_y - dot_r,
                                dx + dot_r, dot_y + dot_r],
                               fill=(*dot_colors[di], 255))
                else:
                    # Hollow dot — dim outline
                    td.ellipse([dx - dot_r, dot_y - dot_r,
                                dx + dot_r, dot_y + dot_r],
                               outline=(*GRAY, 120), width=1)

            # Main status line — centered, WHITE
            txt = status_lines[msg_idx]
            bbox = td.textbbox((0, 0), txt, font=font_lg)
            tw = bbox[2] - bbox[0]
            td.text(((W - tw) // 2, H // 2 - 20), txt,
                    fill=_c(WHITE), font=font_lg)

            # Diagnostic line — soft white
            diag = diag_lines[msg_idx]
            bbox = td.textbbox((0, 0), diag, font=font_sm)
            tw = bbox[2] - bbox[0]
            td.text(((W - tw) // 2, H // 2 + 6), diag,
                    fill=_c(SOFT_W), font=font_sm)

            # Frame counter — bottom right
            counter = f"INIT {msg_idx + 1}/{NUM_MSGS}"
            bbox = td.textbbox((0, 0), counter, font=font_sm)
            tw = bbox[2] - bbox[0]
            td.text((W - tw - 8, H - 22), counter,
                    fill=_c(GRAY), font=font_sm)

            save(result, f"boot_animation/init-{frame_num}.png")


# ─── Keyboard ────────────────────────────────────────────────────────────────

def gen_keyboard():
    """Keyboard layouts — dark keys on near-black background with labels."""
    ensure_dir("keyboard")
    s = SS
    W, H = 480, 222

    # Fonts for key labels (supersampled)
    try:
        kb_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 14 * s)
        kb_font_sm = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 10 * s)
    except Exception:
        kb_font = ImageFont.load_default()
        kb_font_sm = kb_font

    KEY_LABEL_COLOR = _c(EDGE)  # Bright PCARS blue for key text

    # Display labels for special keys
    SPECIAL = {
        "backspace": "\u2190", "capslock": "\u21e7", "done": "\u2713",
        "symbols_toggle": "#$", "space": "\u2423",
    }

    def draw_key_label(d, x, y, kw, kh, label):
        """Draw centered text label on a key at display coords."""
        display = SPECIAL.get(label, label)
        font = kb_font_sm if len(display) > 1 else kb_font
        cx = (x + kw // 2) * s
        cy = (y + kh // 2) * s
        bbox = font.getbbox(display)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        tx = cx - tw // 2
        ty = cy - th // 2 - bbox[1]
        d.text((tx, ty), display, fill=KEY_LABEL_COLOR, font=font)

    def draw_kb(d, rows, start_y=59, key_w=47, key_h=31, cols=None):
        max_cols = cols or max(len(row) for row in rows)
        total = max_cols * key_w
        x_off = (W - total) // 2
        for ri, row in enumerate(rows):
            y = start_y + ri * key_h
            for ci, key in enumerate(row):
                x = x_off + ci * key_w
                rrect(d, (x + 1, y + 1, x + key_w - 2, y + key_h - 2),
                       fill=PANEL, outline=DARK_GRAY, radius=3, width=1)
                draw_key_label(d, x, y, key_w, key_h, key)

    def draw_input_area(d):
        rrect(d, (8, 6, 472, 50), fill=PANEL, outline=DARK_GRAY, radius=3)
        d.rectangle([8*s, 6*s, 472*s, 8*s], fill=_c(FRAME_L))

    def draw_fn_row(d):
        """Bottom function row — individual keys matching JSON positions."""
        y, kh, kw = 183, 31, 47
        keys = [
            (7, kw, "symbols_toggle"),
            (54, kw, "-"),
            (101, kw, "'"),
            (148, 188, "space"),
            (336, kw, "/"),
            (383, kw, "?"),
            (430, kw, "done"),
        ]
        for x, w, label in keys:
            rrect(d, (x, y, x + w - 1, y + kh - 1),
                   fill=PANEL, outline=DARK_GRAY, radius=3, width=1)
            draw_key_label(d, x, y, w, kh, label)

    # QWERTY lowercase — 10 keys per row matching JSON
    img, d = ss_start(W, H, BG)
    draw_input_area(d)
    draw_kb(d, [list("1234567890"), list("qwertyuiop"),
                list("asdfghjkl") + ["backspace"],
                ["capslock"] + list("zxcvbnm,.")])
    draw_fn_row(d)
    save(ss_finish(img, W, H), "keyboard/keyboard_layout_lower.png")

    # QWERTY uppercase
    img, d = ss_start(W, H, BG)
    draw_input_area(d)
    draw_kb(d, [list("1234567890"), list("QWERTYUIOP"),
                list("ASDFGHJKL") + ["backspace"],
                ["capslock"] + list("ZXCVBNM,.")])
    draw_fn_row(d)
    save(ss_finish(img, W, H), "keyboard/keyboard_layout_upper.png")

    # Symbols — rows match JSON: 10 keys each
    img, d = ss_start(W, H, BG)
    draw_input_area(d)
    draw_kb(d, [list("1234567890"), list("!@#$%^&*()"),
                list("~<>+=:;[]") + ["backspace"],
                ["capslock"] + list("_\"`{}|\\,.")])
    draw_fn_row(d)
    save(ss_finish(img, W, H), "keyboard/keyboard_layout_symbols.png")

    # Numeric — 3 keys per row, key_w=47, matching JSON positions
    img, d = ss_start(W, H, BG)
    draw_input_area(d)
    draw_kb(d, [list("789"), list("456"), list("123"),
                ["done", "0", "backspace"]],
            start_y=59, key_w=47, key_h=31)
    save(ss_finish(img, W, H), "keyboard/keyboard_layout_numeric.png")

    # IP — 5 cols, key_w=77 stride, key_h=56 stride, matching JSON
    img, d = ss_start(W, H, BG)
    draw_input_area(d)
    draw_kb(d, [["0", "1", "2", "3", "done"],
                ["/", "4", "5", "6", "backspace"],
                [".", "7", "8", "9"]],
            start_y=57, key_w=77, key_h=56, cols=5)
    save(ss_finish(img, W, H), "keyboard/keyboard_layout_ip.png")

    # Hex — 6 cols, key_w=77 stride, key_h=56 stride, matching JSON
    img, d = ss_start(W, H, BG)
    draw_input_area(d)
    draw_kb(d, [["0", "1", "2", "3", "4", "done"],
                ["5", "6", "7", "8", "9", "backspace"],
                list("ABCDEF")],
            start_y=57, key_w=77, key_h=56)
    save(ss_finish(img, W, H), "keyboard/keyboard_layout_hex.png")

    # Key highlight (47x31) — white glow
    img, d = ss_start(47, 31)
    rrect(d, (0, 0, 46, 30), fill=(SOFT_W[0], SOFT_W[1], SOFT_W[2], 30),
          outline=SOFT_W, radius=3, width=1)
    result = ss_finish(img, 47, 31)
    result = glow(result, radius=2, intensity=0.25)
    save(result, "keyboard/_key-bg.png")

    # Spacebar (188x31)
    img, d = ss_start(188, 31)
    rrect(d, (0, 0, 187, 30), fill=(SOFT_W[0], SOFT_W[1], SOFT_W[2], 30),
          outline=SOFT_W, radius=3, width=1)
    result = ss_finish(img, 188, 31)
    result = glow(result, radius=2, intensity=0.25)
    save(result, "keyboard/_spacebar-4x.png")

    # Hex key (75x54)
    img, d = ss_start(75, 54)
    rrect(d, (0, 0, 74, 53), fill=(SOFT_W[0], SOFT_W[1], SOFT_W[2], 30),
          outline=SOFT_W, radius=3, width=1)
    result = ss_finish(img, 75, 54)
    result = glow(result, radius=2, intensity=0.25)
    save(result, "keyboard/_hex-bg.png")


# ─── Dialogs ────────────────────────────────────────────────────────────────

def gen_dialogs():
    """Dialog backgrounds — dark panels with subtle frame accents."""

    def make_dialog(w, h, accent=EDGE):
        """Dark dialog with thin accent bars at top and bottom."""
        img, d = ss_start(w, h)
        s = SS
        # Main panel — near-black
        rrect(d, (0, 0, w-1, h-1), fill=BG, outline=DARK_GRAY, radius=5, width=1)

        # Top bar — dark steel blue with thin accent strip
        pill(d, (0, 0, int(w * 0.38), 10), FRAME, direction="right")
        d.rectangle([int(w * 0.40)*s, 0, int(w * 0.58)*s, 10*s], fill=_c(FRAME_D))
        d.rectangle([int(w * 0.60)*s, 0, (w-1)*s, 10*s], fill=_c(FRAME))
        # Thin accent edge on bottom of top bar
        d.rectangle([0, 8*s, (w-1)*s, 10*s], fill=_c(accent, 70))

        # Bottom bar — thin dark steel blue
        d.rectangle([0, (h-5)*s, int(w*0.3)*s, (h-1)*s], fill=_c(FRAME_D))
        pill(d, (int(w * 0.32), h-5, w-1, h-1), FRAME, direction="left")
        # Thin accent on top edge
        d.rectangle([0, (h-5)*s, (w-1)*s, (h-4)*s], fill=_c(accent, 50))

        # Very subtle scanlines
        scanlines(d, 4, 14, w-8, h-22, CYAN, spacing=5, alpha=2)

        return ss_finish(img, w, h)

    # Option dialogs (463x197)
    for name, color in [
        ("option_dialog_bg_windowed", EDGE),
        ("option_dialog_bg_windowed_green", GREEN),
        ("option_dialog_bg_windowed_purple", PURPLE),
        ("option_dialog_bg_windowed_red", RED),
        ("option_dialog_bg_narrow", EDGE),
    ]:
        save(make_dialog(463, 197, accent=color), f"optiondialog/{name}.png")

    # Option button bg (59x71)
    img, d = ss_start(59, 71)
    rrect(d, (0, 0, 58, 70), fill=PANEL, outline=DARK_GRAY, radius=3)
    d.rectangle([0, 0, 3*SS, 70*SS], fill=_c(FRAME_L))  # Left accent — steel blue
    save(ss_finish(img, 59, 71), "optiondialog/button_bg.png")

    # Button outline (59x71)
    img, d = ss_start(59, 71)
    rrect(d, (0, 0, 58, 70), fill=(SOFT_W[0], SOFT_W[1], SOFT_W[2], 10),
          outline=SOFT_W, radius=3, width=2)
    result = ss_finish(img, 59, 71)
    result = glow(result, radius=2, intensity=0.15)
    save(result, "optiondialog/button_outline.png")

    # Check (24x19)
    img, d = ss_start(24, 19)
    d.line([(2*SS, 10*SS), (8*SS, 16*SS), (22*SS, 2*SS)], fill=_c(WHITE), width=2*SS)
    save(ss_finish(img, 24, 19), "optiondialog/check.png")

    # X (15x15)
    img, d = ss_start(15, 15)
    d.line([(2*SS, 2*SS), (12*SS, 12*SS)], fill=_c(RED), width=2*SS)
    d.line([(12*SS, 2*SS), (2*SS, 12*SS)], fill=_c(RED), width=2*SS)
    save(ss_finish(img, 15, 15), "optiondialog/x.png")

    # Alert dialog backgrounds
    for name, w, h, accent in [
        ("alert_dialog_bg_term", 398, 220, EDGE),
        ("alert_dialog_bg_term_blue", 429, 222, EDGE),
        ("alert_dialog_bg_term_error", 429, 222, RED),
        ("alert_dialog_bg_term_warning", 429, 222, YELLOW),
    ]:
        save(make_dialog(w, h, accent=accent), f"{name}.png")

    # Confirmation dialog bg (429x222)
    save(make_dialog(429, 222, accent=EDGE), "confirmation_dialog_bg_term.png")

    # Confirmation buttons (121x41)
    for name, bg_c, out_c, accent in [
        ("generic_confirmation_button_deselected", PANEL, DARK_GRAY, None),
        ("generic_confirmation_button_selected", (SOFT_W[0], SOFT_W[1], SOFT_W[2], 15), SOFT_W, SOFT_W),
    ]:
        img, d = ss_start(121, 41)
        rrect(d, (0, 0, 120, 40), fill=bg_c, outline=out_c, radius=3,
              width=1 if accent is None else 2)
        if accent:
            d.rectangle([0, 0, 120*SS, 2*SS], fill=_c(accent, 120))
        result = ss_finish(img, 121, 41)
        if accent:
            result = glow(result, radius=2, intensity=0.25)
        save(result, f"confirmation_dialog/{name}.png")

    # Edit string dialog bg (467x186)
    save(make_dialog(467, 186, accent=EDGE), "edit_string_dialog_bg.png")

    # Dialog BG (480x222)
    save(make_dialog(480, 222, accent=EDGE), "dialog_bg.png")

    # Messagebox (459x112)
    img, d = ss_start(459, 112)
    rrect(d, (0, 0, 458, 111), fill=BG, outline=DARK_GRAY, radius=3)
    pill(d, (0, 0, 200, 7), FRAME, direction="right")
    d.rectangle([208*SS, 0, 458*SS, 7*SS], fill=_c(FRAME_D))
    d.rectangle([0, 5*SS, 458*SS, 7*SS], fill=_c(EDGE, 50))
    scanlines(d, 4, 10, 450, 96, EDGE, spacing=5, alpha=2)
    save(ss_finish(img, 459, 112), "messagebox.png")


# ─── Toggles / Radio / Checkbox ─────────────────────────────────────────────

def gen_toggles():
    """Toggle switches, radio buttons, checkbox."""
    s = SS

    # Toggle enabled bg (29x16)
    img, d = ss_start(29, 16)
    d.rounded_rectangle([0, 0, 28*s, 15*s], radius=8*s,
                        fill=_c(WHITE, 35), outline=_c(WHITE), width=s)
    save(ss_finish(img, 29, 16), "toggle/enabled/toggle_bg.png")

    # Toggle circle enabled (12x12)
    img, d = ss_start(12, 12)
    d.ellipse([0, 0, 11*s, 11*s], fill=_c(WHITE))
    save(ss_finish(img, 12, 12), "toggle/enabled/circle.png")

    # Toggle check (10x5)
    img, d = ss_start(10, 5)
    d.line([(1*s, 3*s), (3*s, 4*s), (9*s, 0)], fill=_c(BG), width=s)
    save(ss_finish(img, 10, 5), "toggle/enabled/check.png")

    # Toggle disabled bg (29x16)
    img, d = ss_start(29, 16)
    d.rounded_rectangle([0, 0, 28*s, 15*s], radius=8*s,
                        fill=_c(DARK_GRAY, 50), outline=_c(GRAY), width=s)
    save(ss_finish(img, 29, 16), "toggle/disabled/toggle_disabled_bg.png")

    # Toggle circle disabled (12x12)
    img, d = ss_start(12, 12)
    d.ellipse([0, 0, 11*s, 11*s], fill=_c(GRAY))
    save(ss_finish(img, 12, 12), "toggle/disabled/circle.png")

    # Radio border (19x19)
    img, d = ss_start(19, 19)
    d.ellipse([s, s, 17*s, 17*s], outline=_c(SOFT_W), width=s)
    save(ss_finish(img, 19, 19), "radio/radio_border.png")

    # Radio selected (11x11)
    img, d = ss_start(11, 11)
    d.ellipse([0, 0, 10*s, 10*s], fill=_c(WHITE))
    result = ss_finish(img, 11, 11)
    result = glow(result, radius=1, intensity=0.25)
    save(result, "radio/radio_selected.png")

    # Checkbox (20x20)
    img, d = ss_start(20, 20)
    rrect(d, (1, 1, 18, 18), outline=SOFT_W, radius=2, width=1)
    d.line([(5*s, 10*s), (8*s, 14*s), (15*s, 5*s)], fill=_c(WHITE), width=2*s)
    save(ss_finish(img, 20, 20), "checkbox.png")


# ─── Recon ───────────────────────────────────────────────────────────────────

def gen_recon():
    """Recon screens and icons."""
    ensure_dir("recon")
    import random
    random.seed(55)
    W, H = 480, 222

    # Recon dashboard (480x222) — blue edge glow (consistent with all screens)
    img = pcars_frame_bg(W, H, accent_top=EDGE, accent_bot=EDGE, accent_side=None)
    save(ss_finish(img, W, H), "recon/recon_dashboard.png")

    # Recon list bg (480x222)
    img, d = ss_start(W, H, BG)
    s = SS
    # Thin top bar — dark steel blue with accent
    d.rectangle([0, 0, W*s, 10*s], fill=_c(FRAME))
    d.rectangle([0, 8*s, W*s, 10*s], fill=_c(CYAN, 60))
    # Segmented gaps
    d.rectangle([120*s, 0, 122*s, 10*s], fill=_c(BG))
    d.rectangle([320*s, 0, 322*s, 10*s], fill=_c(BG))
    # Bottom bar
    d.rectangle([0, (H-10)*s, W*s, H*s], fill=_c(FRAME_D))
    d.rectangle([0, (H-10)*s, W*s, (H-8)*s], fill=_c(EDGE, 40))
    # Row separators — very subtle
    for y in range(42, 198, 34):
        d.line([(10*s, y*s), (470*s, y*s)], fill=_c(DARK_GRAY, 40), width=s)
    save(ss_finish(img, W, H), "recon/recon_list_bg.png")

    # Blank recon bg (480x222)
    img, d = ss_start(W, H, BG)
    d.rectangle([0, 0, W*s, 10*s], fill=_c(FRAME))
    d.rectangle([0, 8*s, W*s, 10*s], fill=_c(CYAN, 60))
    d.rectangle([0, (H-10)*s, W*s, H*s], fill=_c(FRAME_D))
    rrect(d, (140, 80, 340, 140), fill=PANEL, outline=DARK_GRAY, radius=4)
    save(ss_finish(img, W, H), "blank_recon_bg.png")

    # RSSI bars (20x20)
    for level in range(4):
        img, d = ss_start(20, 20)
        for b in range(4):
            bh = (4 + b * 4) * s
            bx = b * 5 * s
            by = 19*s - bh
            if b <= level:
                c = [RED, YELLOW, CYAN, GREEN][level]
            else:
                c = (*DARK_GRAY, 40)
            d.rectangle([bx, by, bx + 3*s, 19*s], fill=_c(c))
        save(ss_finish(img, 20, 20), f"recon/rssi_{level}.png")

    # Encryption icons (20x20)
    def lock_icon(d, color, open_lock=False):
        s2 = SS
        if open_lock:
            d.arc([5*s2, 1*s2, 15*s2, 11*s2], 0, 180, fill=_c(color), width=2*s2)
        else:
            d.arc([5*s2, 1*s2, 15*s2, 11*s2], 0, 180, fill=_c(color), width=2*s2)
            d.line([(5*s2, 6*s2), (5*s2, 10*s2)], fill=_c(color), width=2*s2)
            d.line([(15*s2, 6*s2), (15*s2, 10*s2)], fill=_c(color), width=2*s2)
        rrect(d, (3, 9, 17, 19), fill=color, radius=1)

    for name, color, is_open in [
        ("enc_open", GREEN, True), ("enc_wep", RED, False),
        ("enc_wpa2", EDGE, False), ("enc_wpa3", CYAN, False)
    ]:
        img, d = ss_start(20, 20)
        lock_icon(d, color, is_open)
        save(ss_finish(img, 20, 20), f"recon/{name}.png")

    # Clients (20x20)
    img, d = ss_start(20, 20)
    d.ellipse([3*s, 2*s, 9*s, 8*s], fill=_c(SOFT_W))
    d.ellipse([11*s, 2*s, 17*s, 8*s], fill=_c(SOFT_W))
    d.pieslice([1*s, 6*s, 11*s, 18*s], 0, 180, fill=_c(SOFT_W))
    d.pieslice([9*s, 6*s, 19*s, 18*s], 0, 180, fill=_c(SOFT_W))
    save(ss_finish(img, 20, 20), "recon/clients.png")


# ─── Full-Screen Backgrounds ────────────────────────────────────────────────

def gen_backgrounds():
    """Per-section PCARS backgrounds with color identity + remaining screens."""
    import random
    random.seed(99)
    W, H = 480, 222

    def framed():
        """Generic PCARS-framed background (for non-section screens)."""
        img = pcars_frame_bg(W, H)
        return ss_finish(img, W, H)

    def section(color, dark=None):
        """Section-specific PCARS background with colored structural identity."""
        return ss_finish(pcars_section_bg(W, H, color, dark), W, H)

    # ── Watermark helper — composites faint tinted icon onto background ──
    def watermark(bg_img, icon_name, tint_color, alpha=18, overlay=True):
        """Overlay a large faint wash icon + optional smaller full-color icon on top."""
        icon_path = os.path.join(ASSETS_DIR, "dashboard", f"{icon_name}.png")
        if not os.path.exists(icon_path):
            return bg_img
        icon = Image.open(icon_path).convert("RGBA")

        # --- Layer 1: Large faint wash (existing behavior) ---
        wm_size = 160
        wm_icon = icon.resize((wm_size, wm_size), Image.LANCZOS)
        r, g, b, a = wm_icon.split()
        tinted = Image.new("RGBA", wm_icon.size, (0, 0, 0, 0))
        for y in range(wm_icon.size[1]):
            for x in range(wm_icon.size[0]):
                pa = a.getpixel((x, y))
                if pa > 0:
                    ta = int(pa * alpha / 255)
                    tinted.putpixel((x, y), (*tint_color, ta))
        px = 10
        py = (H - wm_size) // 2 + 10
        bg_img.paste(tinted, (px, py), tinted)

        if not overlay:
            return bg_img

        # --- Layer 2: Smaller full-color icon on solid dark pad ---
        sm_size = 80
        pad = 12  # padding around icon
        sm_icon = icon.resize((sm_size, sm_size), Image.LANCZOS)
        # Tint to section color at full opacity
        r2, g2, b2, a2 = sm_icon.split()
        colored = Image.new("RGBA", sm_icon.size, (0, 0, 0, 0))
        for y in range(sm_icon.size[1]):
            for x in range(sm_icon.size[0]):
                pa = a2.getpixel((x, y))
                if pa > 0:
                    colored.putpixel((x, y), (*tint_color, pa))
        # Center over the wash icon
        sx = px + (wm_size - sm_size) // 2
        sy = py + (wm_size - sm_size) // 2
        # Draw solid dark background pad behind icon to block text
        pad_rect = Image.new("RGBA", (sm_size + pad * 2, sm_size + pad * 2), (*BG, 255))
        bg_img.paste(pad_rect, (sx - pad, sy - pad))
        bg_img.paste(colored, (sx, sy), colored)
        return bg_img

    # ── Section backgrounds — each with unique PCARS identity + watermark icon ──
    bg = section(SEC_SETTINGS, SEC_SETTINGS_D)
    save(watermark(bg, "settings", SEC_SETTINGS, alpha=5, overlay=False), "settings_bg.png")

    bg = section(SEC_PINEAP, SEC_PINEAP_D)
    save(watermark(bg, "pineap", SEC_PINEAP, alpha=5, overlay=False), "pineap_bg.png")

    bg = section(SEC_ALERTS, SEC_ALERTS_D)
    save(watermark(bg, "alerts", SEC_ALERTS), "alerts_dashboard/alerts_bg.png")

    bg = section(SEC_PAYLOADS, SEC_PAYLOADS_D)
    save(watermark(bg, "payloads", SEC_PAYLOADS), "payloads_dashboard/payloads_bg.png")

    bg = section(SEC_RECON, SEC_RECON_D)
    save(watermark(bg, "recon", SEC_RECON), "payloads_dashboard/recon_payloads_bg.png")

    save(section(SEC_POWER, SEC_POWER_D), "power_menu_bg.png")

    bg = section(SEC_PAYLOADS, SEC_PAYLOADS_D)
    save(watermark(bg, "payloads", SEC_PAYLOADS), "launch_payload_dialog/launch_payload_bg.png")

    # Payload log backgrounds
    img, d = ss_start(W, H, BG)
    s = SS
    d.rectangle([0, 0, W*s, 10*s], fill=_c(FRAME))
    d.rectangle([0, 8*s, W*s, 10*s], fill=_c(EDGE, 50))
    d.rectangle([200*s, 0, 202*s, 10*s], fill=_c(BG))
    d.rectangle([0, (H-10)*s, W*s, H*s], fill=_c(FRAME_D))
    d.rectangle([0, (H-10)*s, W*s, (H-8)*s], fill=_c(EDGE, 40))
    result = ss_finish(img, W, H)
    save(result, "payloadlog/payload_log_bg.png")
    save(result, "payload_log_bg.png")

    # NOTE: launch_payload and power_menu section backgrounds
    # are already generated above with section-specific colors

    # Lock screen
    img, d = ss_start(W, H, BG)
    s = SS
    d.rectangle([0, 0, W*s, 4*s], fill=_c(FRAME))
    d.rectangle([0, 2*s, W*s, 4*s], fill=_c(EDGE, 50))
    d.rectangle([0, (H-4)*s, W*s, H*s], fill=_c(FRAME_D))
    # Lock icon — blue edge glow outline on black
    d.arc([215*s, 68*s, 265*s, 108*s], 180, 360, fill=_c(EDGE), width=3*s)
    d.line([(215*s, 88*s), (215*s, 106*s)], fill=_c(EDGE), width=3*s)
    d.line([(265*s, 88*s), (265*s, 106*s)], fill=_c(EDGE), width=3*s)
    rrect(d, (205, 105, 275, 155), fill=EDGE, radius=3)
    d.ellipse([234*s, 118*s, 246*s, 130*s], fill=_c(BG))
    d.rectangle([238*s, 128*s, 242*s, 143*s], fill=_c(BG))
    save(ss_finish(img, W, H), "lock_screen.png")

    # Buttons locked
    img, d = ss_start(W, H, BG)
    d.rectangle([0, 0, W*s, 4*s], fill=_c(FRAME))
    d.rectangle([0, 2*s, W*s, 4*s], fill=_c(EDGE, 50))
    d.rectangle([0, (H-4)*s, W*s, H*s], fill=_c(FRAME_D))
    rrect(d, (140, 80, 340, 142), fill=PANEL, outline=DARK_GRAY, radius=3)
    save(ss_finish(img, W, H), "buttons_locked.png")

    # QR screens — real QR codes with PCARS styling
    _qr_screens = [
        ("help_qr", "https://hak5.org/pager-docs",
         ["Scan to open", "documentation"], "hak5.org/pager-docs", None),
        ("license_qr", "https://hak5.org/pager-license",
         ["Scan to view", "full license"], "hak5.org/pager-license",
         ["Access on device at", "/etc/LICENSES"]),
        ("virt_qr", "http://172.16.52.1:1471",
         ["Scan to open", "browser"], "http://172.16.52.1:1471",
         ["Your device must be", "connected via USB-C", "or Management AP"]),
    ]
    try:
        import subprocess, tempfile
        for qr_name, qr_url, title, url_text, extra in _qr_screens:
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                subprocess.run(["qr", qr_url], stdout=tmp, check=True)
                tmp_path = tmp.name
            qr_raw = Image.open(tmp_path).convert("L")
            qr_sz = 160
            qr_raw = qr_raw.resize((qr_sz, qr_sz), Image.NEAREST)

            screen = Image.new("RGB", (W, H), BG)
            sd = ImageDraw.Draw(screen)
            sd.rectangle([0, 0, W, 3], fill=EDGE)
            sd.rectangle([0, H - 3, W, H], fill=FRAME_D)

            # QR code — white modules on dark bg
            qr_rgb = Image.new("RGB", (qr_sz, qr_sz), BG)
            qr_px = qr_raw.load()
            qr_rgb_px = qr_rgb.load()
            for qy in range(qr_sz):
                for qx in range(qr_sz):
                    qr_rgb_px[qx, qy] = WHITE if qr_px[qx, qy] < 128 else BG
            qr_x, qr_y = 20, (H - qr_sz) // 2 + 5
            screen.paste(qr_rgb, (qr_x, qr_y))
            sd.rectangle([qr_x - 2, qr_y - 2, qr_x + qr_sz + 1, qr_y + qr_sz + 1],
                         outline=DARK_GRAY)

            font_lg = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 18)
            font_md = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 13)
            font_sm = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 11)
            tx, ty = 200, 30
            for line in title:
                sd.text((tx, ty), line, fill=WHITE, font=font_lg)
                ty += 26
            ty += 15
            sd.text((tx, ty), url_text, fill=SEC_SETTINGS, font=font_md)
            if extra:
                ty += 25
                for line in extra:
                    sd.text((tx, ty), line, fill=DARK_GRAY, font=font_sm)
                    ty += 16
            screen.save(os.path.join(ASSETS_DIR, f"{qr_name}.png"))
            os.unlink(tmp_path)
    except Exception as e:
        # Fallback if qr CLI not available
        for qr_name, *_ in _qr_screens:
            base = framed()
            base_d = ImageDraw.Draw(base)
            base_d.rounded_rectangle([160, 28, 420, 194], radius=4, fill=_c(WHITE))
            save(base, f"{qr_name}.png")

    # Warning screens
    for name, accent in [("warn_device_too_hot", RED), ("warn_device_dimming_screen", YELLOW)]:
        img, d = ss_start(W, H, BG)
        d.rectangle([0, 0, W*s, 5*s], fill=_c(accent))
        d.rectangle([0, (H-5)*s, W*s, H*s], fill=_c(accent))
        d.polygon([(240*s, 50*s), (310*s, 170*s), (170*s, 170*s)],
                  outline=_c(accent), fill=_c(accent, 20))
        d.line([(240*s, 80*s), (240*s, 135*s)], fill=_c(BG), width=4*s)
        d.ellipse([235*s, 143*s, 245*s, 153*s], fill=_c(BG))
        save(ss_finish(img, W, H), f"{name}.png")

    # Battery alerts
    for name, color in [("low_battery_alert", YELLOW), ("critical_battery_alert", RED)]:
        img, d = ss_start(W, H, BG)
        d.rectangle([0, 0, W*s, 5*s], fill=_c(color))
        d.rectangle([0, (H-5)*s, W*s, H*s], fill=_c(color))
        rrect(d, (195, 55, 265, 160), outline=color, radius=3, width=2)
        d.rectangle([220*s, 48*s, 240*s, 55*s], fill=_c(color))
        fill_h = 35 if "low" in name else 12
        d.rectangle([199*s, (158-fill_h)*s, 261*s, 156*s], fill=_c(color))
        save(ss_finish(img, W, H), f"{name}.png")

    # Upgrade screens — blue frame, functional progress bar color
    for name, color in [
        ("upgrade/checking_for_update-min", CYAN),
        ("upgrade/downloading_upgrade", GREEN),
        ("upgrade/validating_upgrade", EDGE),
    ]:
        base = framed()
        d = ImageDraw.Draw(base)
        d.rounded_rectangle([80, 118, 400, 138], radius=4,
                            fill=_c(PANEL), outline=_c(DARK_GRAY))
        d.rounded_rectangle([82, 120, 250, 136], radius=3, fill=_c(color))
        save(base, f"{name}.png")


# ─── Miscellaneous ───────────────────────────────────────────────────────────

def gen_misc():
    """All remaining small UI assets."""
    s = SS

    # Arrows (19x38) — subtle blue accent
    for name, flip in [("arrow_up", False), ("arrow_down", True)]:
        img, d = ss_start(19, 38)
        if not flip:
            d.polygon([(9*s, 2*s), (17*s, 18*s), (12*s, 18*s),
                       (12*s, 36*s), (6*s, 36*s), (6*s, 18*s), (1*s, 18*s)],
                      fill=_c(EDGE))
        else:
            d.polygon([(9*s, 36*s), (17*s, 20*s), (12*s, 20*s),
                       (12*s, 2*s), (6*s, 2*s), (6*s, 20*s), (1*s, 20*s)],
                      fill=_c(EDGE))
        save(ss_finish(img, 19, 38), f"{name}.png")

    # Small up/down (16x16)
    for name, pts in [("up", [(8, 2), (14, 13), (2, 13)]),
                      ("down", [(8, 13), (14, 2), (2, 2)])]:
        img, d = ss_start(16, 16)
        d.polygon([(p[0]*s, p[1]*s) for p in pts], fill=_c(SOFT_W))
        save(ss_finish(img, 16, 16), f"{name}.png")

    # Dividers (13x160) — generic dark steel blue
    for name, color in [("divider", FRAME_L), ("divleft", FRAME), ("divright", FRAME_D)]:
        img, d = ss_start(13, 160)
        d.rounded_rectangle([4*s, 0, 8*s, 159*s], radius=2*s, fill=_c(color))
        save(ss_finish(img, 13, 160), f"{name}.png")

    # Section-colored dividers (13x160) — PCARS identity for two-column menus
    section_divs = {
        'settings': (SEC_SETTINGS_D, tuple(min(c + 20, 255) for c in SEC_SETTINGS_D)),
        'pineap':   (SEC_PINEAP_D,  tuple(min(c + 20, 255) for c in SEC_PINEAP_D)),
    }
    for sec, (dark_c, light_c) in section_divs.items():
        img, d = ss_start(13, 160)
        d.rounded_rectangle([4*s, 0, 8*s, 159*s], radius=2*s, fill=_c(light_c))
        save(ss_finish(img, 13, 160), f"divleft_{sec}.png")
        img, d = ss_start(13, 160)
        d.rounded_rectangle([4*s, 0, 8*s, 159*s], radius=2*s, fill=_c(dark_c))
        save(ss_finish(img, 13, 160), f"divright_{sec}.png")

    # Menu icon (29x20) — three bars in dark steel blue
    img, d = ss_start(29, 20)
    for i, (y, c) in enumerate([(2, FRAME_L), (8, FRAME), (14, FRAME_D)]):
        pill(d, (2, y, 26, y + 4), c, direction="right")
    save(ss_finish(img, 29, 20), "menu.png")

    # Menu disabled (29x20)
    img, d = ss_start(29, 20)
    for y in [2, 8, 14]:
        pill(d, (2, y, 26, y + 4), GRAY, direction="right")
    save(ss_finish(img, 29, 20), "menu_disabled.png")

    # Info (29x20)
    img, d = ss_start(29, 20)
    rrect(d, (4, 0, 24, 19), outline=CYAN, radius=3, width=1)
    d.ellipse([12*s, 3*s, 16*s, 7*s], fill=_c(CYAN))
    d.rectangle([13*s, 9*s, 15*s, 16*s], fill=_c(CYAN))
    save(ss_finish(img, 29, 20), "info.png")

    # Warning (29x20)
    img, d = ss_start(29, 20)
    d.polygon([(14*s, 1*s), (27*s, 18*s), (1*s, 18*s)],
              outline=_c(YELLOW), fill=_c(YELLOW, 20))
    d.line([(14*s, 6*s), (14*s, 13*s)], fill=_c(YELLOW), width=s)
    d.ellipse([13*s, 14*s, 15*s, 16*s], fill=_c(YELLOW))
    save(ss_finish(img, 29, 20), "warning.png")

    # Keyboard icon (29x20)
    img, d = ss_start(29, 20)
    rrect(d, (1, 3, 27, 17), outline=SOFT_W, radius=2, width=1)
    for x in [6, 11, 16, 21]:
        d.rectangle([x*s, 6*s, (x+2)*s, 8*s], fill=_c(SOFT_W))
    for x in [8, 13, 18]:
        d.rectangle([x*s, 11*s, (x+2)*s, 13*s], fill=_c(SOFT_W))
    save(ss_finish(img, 29, 20), "keyboard.png")

    # Wizard (29x20)
    img, d = ss_start(29, 20)
    d.polygon([(14*s, 1*s), (16*s, 7*s), (24*s, 7*s), (18*s, 11*s),
               (20*s, 18*s), (14*s, 14*s), (8*s, 18*s), (10*s, 11*s),
               (4*s, 7*s), (12*s, 7*s)], fill=_c(EDGE), outline=_c(FRAME_L))
    save(ss_finish(img, 29, 20), "wizard.png")

    # Disabled variants — desaturated copies
    for name in ["info", "warning", "keyboard", "wizard"]:
        orig = Image.open(os.path.join(ASSETS_DIR, f"{name}.png")).convert("RGBA")
        px = orig.load()
        for y in range(orig.height):
            for x in range(orig.width):
                r, g, b, a = px[x, y]
                if a > 0:
                    gray = min(int(0.3 * r + 0.59 * g + 0.11 * b), 60)
                    px[x, y] = (gray, gray, gray, a)
        save(orig, f"disabled_{name}.png")

    # Client (23x14)
    img, d = ss_start(23, 14)
    rrect(d, (0, 0, 22, 13), outline=SOFT_W, radius=2, width=1)
    d.ellipse([9*s, 4*s, 13*s, 8*s], fill=_c(CYAN))
    save(ss_finish(img, 23, 14), "client.png")

    # Disabled client (23x14)
    img, d = ss_start(23, 14)
    rrect(d, (0, 0, 22, 13), outline=GRAY, radius=2, width=1)
    d.ellipse([9*s, 4*s, 13*s, 8*s], fill=_c(GRAY))
    save(ss_finish(img, 23, 14), "disabled_client.png")

    # X (15x15)
    img, d = ss_start(15, 15)
    d.line([(2*s, 2*s), (12*s, 12*s)], fill=_c(RED), width=2*s)
    d.line([(12*s, 2*s), (2*s, 12*s)], fill=_c(RED), width=2*s)
    save(ss_finish(img, 15, 15), "x.png")

    # Triangle (13x15)
    img, d = ss_start(13, 15)
    d.polygon([(1*s, 14*s), (6*s, 1*s), (11*s, 14*s)], fill=_c(EDGE))
    save(ss_finish(img, 13, 15), "triangle.png")

    # Start (20x20) — play triangle
    img, d = ss_start(20, 20)
    d.polygon([(4*s, 2*s), (18*s, 10*s), (4*s, 18*s)], fill=_c(GREEN))
    save(ss_finish(img, 20, 20), "start.png")

    # Swap (20x20)
    img, d = ss_start(20, 20)
    d.polygon([(2*s, 5*s), (10*s, 1*s), (10*s, 9*s)], fill=_c(EDGE))
    d.polygon([(18*s, 15*s), (10*s, 11*s), (10*s, 19*s)], fill=_c(FRAME_L))
    save(ss_finish(img, 20, 20), "swap.png")

    # Autoplay (24x24)
    img, d = ss_start(24, 24)
    d.ellipse([2*s, 2*s, 21*s, 21*s], outline=_c(GREEN), width=s)
    d.polygon([(9*s, 6*s), (18*s, 12*s), (9*s, 18*s)], fill=_c(GREEN))
    save(ss_finish(img, 24, 24), "autoplay.png")

    # Autoplay stopped (24x24)
    img, d = ss_start(24, 24)
    d.ellipse([2*s, 2*s, 21*s, 21*s], outline=_c(RED), width=s)
    d.rectangle([8*s, 7*s, 16*s, 17*s], fill=_c(RED))
    save(ss_finish(img, 24, 24), "autoplay_stopped.png")

    # Flame (11x17)
    img, d = ss_start(11, 17)
    d.polygon([(5*s, 0), (10*s, 10*s), (8*s, 16*s),
               (5*s, 12*s), (2*s, 16*s), (0, 10*s)],
              fill=_c(ORANGE), outline=_c(RED))
    save(ss_finish(img, 11, 17), "flame.png")

    # Folder (24x24)
    img, d = ss_start(24, 24)
    d.polygon([(1*s, 5*s), (10*s, 5*s), (12*s, 2*s), (22*s, 2*s), (22*s, 5*s)],
              fill=_c(SOFT_W))
    rrect(d, (1, 5, 22, 21), fill=SOFT_W, radius=2)
    save(ss_finish(img, 24, 24), "folder.png")

    # WiFi icon (25x25)
    img, d = ss_start(25, 25)
    d.arc([1*s, 1*s, 24*s, 24*s], 210, 330, fill=_c(CYAN), width=2*s)
    d.arc([5*s, 5*s, 20*s, 20*s], 215, 325, fill=_c(CYAN), width=2*s)
    d.arc([9*s, 9*s, 16*s, 16*s], 220, 320, fill=_c(CYAN), width=s)
    d.ellipse([11*s, 18*s, 14*s, 21*s], fill=_c(CYAN))
    save(ss_finish(img, 25, 25), "wifi_icon.png")

    # Alerts sub (26x9) — coral-red pill to match alerts section
    img, d = ss_start(26, 9)
    pill(d, (0, 0, 25, 8), SEC_ALERTS, direction="right")
    save(ss_finish(img, 26, 9), "alerts_dashboard/sub.png")

    # Payload dialog bg (135x70)
    img, d = ss_start(135, 70)
    rrect(d, (0, 0, 134, 69), fill=PANEL, outline=DARK_GRAY, radius=3)
    d.rectangle([0, 0, 3*s, 69*s], fill=_c(FRAME_L))
    save(ss_finish(img, 135, 70), "payload_dialog_option_bg.png")

    # Payload dialog selected (136x71)
    img, d = ss_start(136, 71)
    rrect(d, (0, 0, 135, 70), fill=(SOFT_W[0], SOFT_W[1], SOFT_W[2], 10),
          outline=SOFT_W, radius=3, width=2)
    result = ss_finish(img, 136, 71)
    result = glow(result, radius=2, intensity=0.15)
    save(result, "payload_dialog_selected_box.png")

    # Pager device (88x62)
    img, d = ss_start(88, 62)
    rrect(d, (2, 2, 85, 59), fill=PANEL, outline=FRAME_L, radius=3, width=1)
    rrect(d, (8, 8, 55, 38), fill=(CYAN[0], CYAN[1], CYAN[2], 15),
          outline=TEAL, radius=2, width=1)
    d.ellipse([65*s, 15*s, 78*s, 28*s], outline=_c(SOFT_W), width=s)
    d.ellipse([65*s, 35*s, 78*s, 48*s], outline=_c(SOFT_W), width=s)
    save(ss_finish(img, 88, 62), "pager-16bit.png")

    # Payload log indicators
    for name, w, h, color in [
        ("payloadlog/payload_complete_indicator", 480, 43, GREEN),
        ("payloadlog/payload_error_indicator", 480, 44, RED),
        ("payloadlog/payload_running_indicator", 480, 43, CYAN),
        ("payloadlog/payload_stopped_indicator", 480, 44, EDGE),
    ]:
        img, d = ss_start(w, h)
        rrect(d, (0, 0, w-1, h-1), fill=(color[0], color[1], color[2], 8),
              outline=(color[0], color[1], color[2], 35), radius=2, width=1)
        d.rectangle([0, 0, 3*s, (h-1)*s], fill=_c(color))
        save(ss_finish(img, w, h), f"{name}.png")

    # Scroll indicators (12x15)
    for name, flip in [("payloadlog/scroll_up_indicator", False),
                       ("payloadlog/scroll_down_indicator", True)]:
        img, d = ss_start(12, 15)
        if not flip:
            d.polygon([(6*s, 1*s), (11*s, 14*s), (1*s, 14*s)], fill=_c(CYAN))
        else:
            d.polygon([(6*s, 14*s), (11*s, 1*s), (1*s, 1*s)], fill=_c(CYAN))
        save(ss_finish(img, 12, 15), f"{name}.png")

    # Scroll pause (16x16)
    img, d = ss_start(16, 16)
    d.rectangle([3*s, 2*s, 6*s, 13*s], fill=_c(EDGE))
    d.rectangle([9*s, 2*s, 12*s, 13*s], fill=_c(EDGE))
    save(ss_finish(img, 16, 16), "payloadlog/scroll_pause_indicator.png")

    # Payloads dashboard arrow (20x18)
    img, d = ss_start(20, 18)
    d.polygon([(2*s, 9*s), (16*s, 2*s), (16*s, 16*s)], fill=_c(SOFT_W))
    save(ss_finish(img, 20, 18), "payloads_dashboard/arrow.png")

    # Launch animation frames — organic plasma ball, 4 frames cycling
    PLASMA_GREEN = (0, 220, 80)
    anim_seeds = [42, 77, 123, 256]
    for fi, seed in enumerate(anim_seeds):
        name = f"animation/anim_frame_{fi + 1}"
        result = _draw_organic_plasma(113, 106, seed=seed, color=PLASMA_GREEN)
        save(result, f"launch_payload_dialog/{name}.png")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print(f"Generating PCARS assets → {ASSETS_DIR}")
    print(f"Supersample factor: {SS}x")
    os.makedirs(ASSETS_DIR, exist_ok=True)

    steps = [
        ("Status bar icons", gen_statusbar),
        ("Dashboard", gen_dashboard),
        ("Spinner", gen_spinner),
        ("Boot animation", gen_boot),
        ("Keyboards", gen_keyboard),
        ("Dialogs", gen_dialogs),
        ("Toggles/Radio/Checkbox", gen_toggles),
        ("Recon", gen_recon),
        ("Full-screen backgrounds", gen_backgrounds),
        ("Misc UI elements", gen_misc),
    ]

    for i, (label, fn) in enumerate(steps, 1):
        print(f"  [{i}/{len(steps)}] {label}...")
        fn()

    count = sum(1 for r, _, fs in os.walk(ASSETS_DIR) for f in fs if f.endswith(".png"))
    print(f"\nGenerated {count} PNG assets.")


if __name__ == "__main__":
    main()
