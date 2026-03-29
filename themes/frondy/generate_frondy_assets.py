#!/usr/bin/env python3
"""
Frondy Theme — Asset Generator
WiFi Pineapple Pager (480x222 display)

High-contrast black and yellow theme. Clean, flat, candy-polished UI.
No glow, no scanlines, no animations beyond boot. Sharp edges, bold contrast.
Supersampled rendering at 3x with LANCZOS downscale for anti-aliased edges.

Usage: python3 generate_frondy_assets.py
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

# ─── Configuration ───────────────────────────────────────────────────────────

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
SS = 3  # Supersample factor

# ─── Frondy Palette ────────────────────────────────────────────────────
# Pure black and yellow. High contrast. Clean.

# Backgrounds — true black
BG        = (0, 0, 0)              # Pure black background
PANEL     = (0, 0, 0)              # Pure black panel
PANEL_L   = (24, 22, 14)           # Lighter panel — hover/active areas

# Yellow — the accent (warm gold-yellow, not lemon)
YELLOW    = (255, 200, 0)          # Primary accent — bold yellow
YELLOW_L  = (255, 220, 60)         # Light yellow — highlights
YELLOW_D  = (140, 110, 0)          # Dark yellow — dimmed/inactive
YELLOW_DD = (70, 55, 0)            # Very dark yellow — subtle structural

# Neutrals
WHITE     = (245, 240, 230)        # Warm white — text
SOFT_W    = (200, 195, 185)        # Soft white — secondary text
GRAY      = (100, 95, 85)          # Disabled text
DARK_GRAY = (35, 33, 28)           # Borders / separators
DIM       = (45, 42, 32)           # Dimmed elements

# Functional colors (kept distinct for clarity — yellow theme doesn't mask errors)
RED       = (220, 55, 40)          # Alert / error
GREEN     = (75, 195, 75)          # Success / enabled
CYAN      = (0, 195, 215)          # Info readout

T = (0, 0, 0, 0)  # Transparent

# Section colors — all yellow (unified, theme.json maps everything to yellow)
SEC_ACCENT   = YELLOW
SEC_DIM      = YELLOW_D
SEC_DARK     = YELLOW_DD


# ─── Core Drawing Utilities ──────────────────────────────────────────────────

def _c(color, alpha=255):
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
    if bg is None:
        return Image.new("RGBA", (w, h), T)
    return Image.new("RGBA", (w, h), _c(bg))


def ss_start(w, h, bg=None):
    img = new(w * SS, h * SS, bg)
    return img, ImageDraw.Draw(img)


def ss_finish(img, w, h):
    return img.resize((w, h), Image.LANCZOS)


def rrect(d, xy, fill=None, outline=None, radius=4, width=1, s=SS):
    x0, y0, x1, y1 = [v * s for v in xy] if s > 1 else xy
    r = radius * s if s > 1 else radius
    w = width * s if s > 1 else width
    d.rounded_rectangle([x0, y0, x1, y1], radius=r,
                        fill=_c(fill) if fill else None,
                        outline=_c(outline) if outline else None,
                        width=w)


# ─── Frondy Background Templates ──────────────────────────────────────

def yj_frame_bg(w, h, top_h=26):
    """Clean black background with yellow-accented status bar."""
    img, d = ss_start(w, h, BG)
    s = SS

    # Status bar — dark panel
    d.rectangle([0, 0, w * s, top_h * s], fill=_c(PANEL))

    # 1px yellow separator below status bar
    d.rectangle([0, (top_h - 1) * s, w * s, top_h * s], fill=_c(YELLOW, 40))

    return img


def yj_section_bg(w, h, top_h=26, sidebar_w=4, bottom_h=3):
    """Section background — yellow left bar, yellow bottom strip."""
    img, d = ss_start(w, h, BG)
    s = SS

    # Status bar
    d.rectangle([0, 0, w * s, top_h * s], fill=_c(PANEL))
    d.rectangle([0, (top_h - 1) * s, w * s, top_h * s], fill=_c(YELLOW, 40))

    # Left sidebar bar — yellow structural accent
    bar_top = top_h * s
    bar_bot = (h - bottom_h) * s
    d.rectangle([0, bar_top, sidebar_w * s, bar_bot], fill=_c(YELLOW))

    # Bottom accent strip
    d.rectangle([0, (h - bottom_h) * s, w * s, h * s], fill=_c(YELLOW_DD, 50))
    d.rectangle([0, (h - bottom_h) * s, w * s, (h - bottom_h + 1) * s],
                fill=_c(YELLOW, 30))

    return img


# ─── Dashboard ───────────────────────────────────────────────────────────────

def gen_dashboard():
    """Main dashboard — 5 full-width horizontal bands.
    Unselected: black band with dim yellow icon/label.
    Selected: solid yellow band with black icon/label.
    """
    ensure_dir("dashboard")

    W, H = 480, 222
    TOP_BAR = 26
    BAND_H = 39       # (222 - 26) / 5 ≈ 39.2, use 39 with 1px gaps
    BAND_W = 480
    s = SS

    # ── Background: black base + status bar + faint band separators ──
    img, d = ss_start(W, H, BG)

    # Status bar
    d.rectangle([0, 0, W * s, TOP_BAR * s], fill=_c(PANEL))
    d.rectangle([0, (TOP_BAR - 1) * s, W * s, TOP_BAR * s], fill=_c(YELLOW, 35))

    # 5 bands with 1px yellow separator lines between them
    for i in range(1, 5):
        y = TOP_BAR + i * BAND_H
        d.rectangle([0, y * s, W * s, (y + 1) * s], fill=_c(YELLOW_DD, 40))

    result = ss_finish(img, W, H)
    save(result, "dashboard/yj_bg.png")

    # ── Band background (480x39) — transparent (bg shows through) ──
    img = new(BAND_W, BAND_H)
    save(img, "dashboard/band_bg.png")

    # ── Band highlight (480x39) — same height as band, solid yellow ──
    img, d = ss_start(BAND_W, BAND_H)
    d.rectangle([0, 0, BAND_W * s, BAND_H * s], fill=_c(YELLOW))
    result = ss_finish(img, BAND_W, BAND_H)
    save(result, "dashboard/band_highlight.png")

    # ── Breadcrumb dots (8x8) ──
    dot_size = 8
    img, d = ss_start(dot_size, dot_size)
    d.ellipse([1 * s, 1 * s, (dot_size - 1) * s, (dot_size - 1) * s],
              outline=_c((255, 255, 255), 255), width=2 * s)
    save(ss_finish(img, dot_size, dot_size), "dashboard/dot_hollow.png")

    img, d = ss_start(dot_size, dot_size)
    d.ellipse([1 * s, 1 * s, (dot_size - 1) * s, (dot_size - 1) * s],
              fill=_c((255, 255, 255), 255))
    save(ss_finish(img, dot_size, dot_size), "dashboard/dot_filled.png")

    # ── Nav Icons — 24x24 — 8-BIT PIXEL ART style ──
    ICON_SIZE = 24

    # Pixel art bitmaps — each 1 = filled pixel on a 9x9 grid
    ICON_BITMAPS = {
        "alerts": [  # Frondy brand icon — skull with frond pokies + X eye patch
            [0,0,0,1,0,0,0,0,0],
            [0,0,0,1,0,1,0,0,0],
            [0,1,0,1,0,1,0,0,0],
            [0,0,1,1,0,1,1,0,0],
            [0,1,1,1,1,1,1,1,0],
            [0,1,0,1,0,0,1,1,0],
            [0,1,1,0,0,0,1,1,0],
            [0,0,1,1,1,1,1,0,0],
            [0,0,1,0,1,0,1,0,0],
        ],
        "payloads": [  # Terminal prompt >_
            [0,0,0,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,1,1,1,1],
        ],
        "recon": [  # Crosshair — targeting/scan
            [0,0,0,0,1,0,0,0,0],
            [0,0,0,0,1,0,0,0,0],
            [0,0,1,1,1,1,1,0,0],
            [0,0,1,0,0,0,1,0,0],
            [1,1,1,0,1,0,1,1,1],
            [0,0,1,0,0,0,1,0,0],
            [0,0,1,1,1,1,1,0,0],
            [0,0,0,0,1,0,0,0,0],
            [0,0,0,0,1,0,0,0,0],
        ],
        "pineap": [  # Antenna tower — broadcast
            [1,0,0,0,1,0,0,0,1],
            [0,1,0,0,1,0,0,1,0],
            [0,0,1,0,1,0,1,0,0],
            [0,0,0,1,1,1,0,0,0],
            [0,0,0,0,1,0,0,0,0],
            [0,0,0,0,1,0,0,0,0],
            [0,0,0,1,1,1,0,0,0],
            [0,0,1,0,1,0,1,0,0],
            [0,1,1,1,1,1,1,1,0],
        ],
        "settings": [  # 3 horizontal sliders
            [0,0,0,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,0,0],
            [1,1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,0,0,0,0],
            [1,1,1,1,1,1,1,1,1],
        ],
    }

    def _draw_pixel_icon(target_size, bitmap, name):
        """Render a pixel art icon from a 9x9 bitmap to target_size PNG.
        No anti-aliasing — crisp nearest-neighbor scaling for true 8-bit look."""
        rows = len(bitmap)
        cols = max(len(r) for r in bitmap)
        # Draw at native grid size first
        grid_sz = max(rows, cols)
        img = Image.new("RGBA", (grid_sz, grid_sz), (0, 0, 0, 0))
        for r, row in enumerate(bitmap):
            for c, val in enumerate(row):
                if val:
                    img.putpixel((c, r), (255, 255, 255, 255))
        # Scale up with NEAREST — preserves crisp pixel edges
        img = img.resize((target_size, target_size), Image.NEAREST)
        save(img, name)

    for icon_name in ["alerts", "payloads", "recon", "pineap", "settings"]:
        _draw_pixel_icon(ICON_SIZE, ICON_BITMAPS[icon_name], f"dashboard/{icon_name}.png")

    _draw_icon_old = None  # old function removed

    # ── Labels — crisp text for band layout ──
    salter_path = os.path.join(ASSETS_DIR, "fonts", "uni0563.ttf")
    font = ImageFont.truetype(salter_path, 14)      # Unselected — slightly smaller for chunky font
    font_sel = ImageFont.truetype(salter_path, 28)  # Selected — sized down slightly for chunky font

    label_names = ["ALERTS", "PAYLOADS", "RECON", "PINEAP", "SETTINGS"]
    for label in label_names:
        # Normal size (28pt)
        bbox = font.getbbox(label)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        img = Image.new("RGBA", (tw + 4, th + 4), T)
        d = ImageDraw.Draw(img)
        d.text((2 - bbox[0], 2 - bbox[1]), label, fill=(255, 255, 255, 255), font=font)
        r, g, b, a = img.split()
        a = a.point(lambda p: 255 if p > 96 else 0)
        img = Image.merge("RGBA", (r, g, b, a))
        save(img, f"dashboard/label_{label.lower()}.png")

        # Selected size (34pt) — larger for active state
        bbox_s = font_sel.getbbox(label)
        tw_s = bbox_s[2] - bbox_s[0]
        th_s = bbox_s[3] - bbox_s[1]
        img_s = Image.new("RGBA", (tw_s + 4, th_s + 4), T)
        d_s = ImageDraw.Draw(img_s)
        d_s.text((2 - bbox_s[0], 2 - bbox_s[1]), label, fill=(255, 255, 255, 255), font=font_sel)
        r, g, b, a = img_s.split()
        a = a.point(lambda p: 255 if p > 96 else 0)
        img_s = Image.merge("RGBA", (r, g, b, a))
        save(img_s, f"dashboard/label_{label.lower()}_selected.png")

    # ── Selected Icons — 30x30 — same pixel art, scaled up ──
    SEL_ICON = 30
    for icon_name in ["alerts", "payloads", "recon", "pineap", "settings"]:
        _draw_pixel_icon(SEL_ICON, ICON_BITMAPS[icon_name], f"dashboard/{icon_name}_selected.png")


# ─── Status Bar ──────────────────────────────────────────────────────────────

def gen_statusbar():
    """Status bar icons — yellow accent system."""
    ensure_dir("statusbar")
    s = SS

    # ── Battery (38x20) ──
    bat_specs = [
        ("dashboard_battery_charge_25", 1, YELLOW),
        ("dashboard_battery_charge_50", 2, YELLOW),
        ("dashboard_battery_charge_75", 3, YELLOW_L),
        ("dashboard_battery_charge_100", 4, YELLOW_L),
        ("dashboard_battery_full", 4, YELLOW_L),
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
        col = _c((int(70 + frac * 185), int(55 + frac * 145), 0))
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
               fill=_c(YELLOW), width=s)
    d.line([(10*s, 2*s), (10*s, 18*s)], fill=_c(YELLOW), width=s)
    save(ss_finish(img, 20, 20), "statusbar/bluetooth.png")

    # ── Volume ──
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
    d.line([(2*s, 3*s), (17*s, 17*s)], fill=_c(YELLOW_D), width=2*s)
    save(ss_finish(img, 20, 20), "statusbar/mute.png")

    # ── Vibrate (24x17) ──
    img, d = ss_start(24, 17)
    rrect(d, (7, 1, 17, 16), outline=SOFT_W, radius=2, width=1)
    d.arc([1*s, 4*s, 7*s, 13*s], 100, 260, fill=_c(SOFT_W), width=s)
    d.arc([17*s, 4*s, 23*s, 13*s], 280, 80, fill=_c(SOFT_W), width=s)
    save(ss_finish(img, 24, 17), "statusbar/vibrate.png")

    # ── GHz indicators (20x20 or 20x22) ──
    ghz = [("ghz_2", "2", YELLOW, 20), ("ghz_5", "5", YELLOW, 20),
           ("ghz_6", "6", YELLOW_D, 20), ("ghz_25", "25", YELLOW, 20),
           ("ghz_26", "26", YELLOW, 22), ("ghz_56", "56", YELLOW, 20),
           ("ghz_256", "A", YELLOW_L, 20), ("ghz_off", "-", GRAY, 20)]
    for name, _label, color, hh in ghz:
        img, d = ss_start(20, hh)
        rrect(d, (0, 0, 19, hh - 1), fill=(color[0], color[1], color[2], 30),
              outline=color, radius=3, width=1)
        save(ss_finish(img, 20, hh), f"statusbar/{name}.png")

    # ── GPS (21x21) ──
    img, d = ss_start(21, 21)
    cx, cy = 10*s, 10*s
    d.ellipse([cx-7*s, cy-7*s, cx+7*s, cy+7*s], outline=_c(YELLOW), width=s)
    d.ellipse([cx-3*s, cy-3*s, cx+3*s, cy+3*s], fill=_c(YELLOW))
    for dx, dy, dx2, dy2 in [(0, -9, 0, -4), (0, 4, 0, 9), (-9, 0, -4, 0), (4, 0, 9, 0)]:
        d.line([(cx+dx*s, cy+dy*s), (cx+dx2*s, cy+dy2*s)], fill=_c(YELLOW), width=s)
    save(ss_finish(img, 21, 21), "statusbar/gps.png")

    # ── Database (21x19) ──
    img, d = ss_start(21, 19)
    for cy in [3, 8, 13]:
        d.ellipse([3*s, cy*s, 18*s, (cy+5)*s], outline=_c(YELLOW_D), width=s)
    d.line([(3*s, 5*s), (3*s, 15*s)], fill=_c(YELLOW_D), width=s)
    d.line([(18*s, 5*s), (18*s, 15*s)], fill=_c(YELLOW_D), width=s)
    save(ss_finish(img, 21, 19), "statusbar/database.png")

    # ── PCAP (20x21) ──
    img, d = ss_start(20, 21)
    rrect(d, (2, 0, 17, 20), outline=YELLOW_D, radius=2, width=1)
    for ly in [5, 9, 13]:
        d.line([(5*s, ly*s), (14*s, ly*s)], fill=_c(YELLOW_D), width=s)
    save(ss_finish(img, 20, 21), "statusbar/pcap.png")

    # ── Wigle (28x21) ──
    img, d = ss_start(28, 21)
    d.ellipse([4*s, 1*s, 24*s, 20*s], outline=_c(YELLOW_D), width=s)
    d.ellipse([10*s, 1*s, 18*s, 20*s], outline=_c(YELLOW_D), width=s)
    d.line([(4*s, 10*s), (24*s, 10*s)], fill=_c(YELLOW_D), width=s)
    save(ss_finish(img, 28, 21), "statusbar/wigle.png")


# ─── Spinner ─────────────────────────────────────────────────────────────────

def gen_spinner():
    """Loading spinner — clean rotating yellow arc on black."""
    ensure_dir("spinner")
    s = SS
    W, H = 220, 156

    for frame in range(1, 5):
        img, d = ss_start(W, H)
        cx, cy = W * s // 2, H * s // 2
        ba = (frame - 1) * 90

        # Outer ring — dim
        r1 = min(cx, cy) - 6 * s
        d.arc([cx - r1, cy - r1, cx + r1, cy + r1],
              0, 360, fill=_c(DARK_GRAY, 60), width=2 * s)

        # Sweeping arc — yellow
        d.arc([cx - r1, cy - r1, cx + r1, cy + r1],
              ba, ba + 90, fill=_c(YELLOW, 220), width=3 * s)
        # Trail
        d.arc([cx - r1, cy - r1, cx + r1, cy + r1],
              ba - 30, ba, fill=_c(YELLOW, 80), width=2 * s)

        # Middle ring — subtle pulse
        r2 = r1 - 16 * s
        pulse_alpha = [100, 160, 200, 140][frame - 1]
        d.arc([cx - r2, cy - r2, cx + r2, cy + r2],
              0, 360, fill=_c(YELLOW_D, pulse_alpha), width=2 * s)

        # Inner arc — counter-rotating
        r3 = r2 - 14 * s
        ba2 = 360 - ba
        d.arc([cx - r3, cy - r3, cx + r3, cy + r3],
              ba2, ba2 + 60, fill=_c(YELLOW_L, 160), width=2 * s)

        # Center dot
        pr = (4 + frame) * s
        d.ellipse([cx - pr, cy - pr, cx + pr, cy + pr],
                  fill=_c(YELLOW, 60 + frame * 25))
        d.ellipse([cx - 3 * s, cy - 3 * s, cx + 3 * s, cy + 3 * s],
                  fill=_c(YELLOW, 200))

        save(ss_finish(img, W, H), f"spinner/spinner{frame}.png")


# ─── Boot Animation ──────────────────────────────────────────────────────────

def gen_boot():
    """Boot animation — pixel grid tile-in.
    Black screen. Square pixels fill in from edges/corners toward center,
    revealing Frondy text. 16 frames.
    """
    ensure_dir("boot_animation")
    import random

    title_path = os.path.join(ASSETS_DIR, "fonts", "uni0563.ttf")
    mono_path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    try:
        font_title = ImageFont.truetype(title_path, 44)
        font_sub = ImageFont.truetype(mono_path, 10)
        font_ver = ImageFont.truetype(mono_path, 14)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = font_title
        font_ver = font_title

    W, H = 480, 222
    TOTAL_FRAMES = 16
    y = YELLOW
    b = BG

    # Square pixel grid — tight tiling, no gaps
    px_size = 20  # each pixel block is 20x20
    cols = (W + px_size - 1) // px_size
    rows = (H + px_size - 1) // px_size

    grid = []  # (x, y)
    for row in range(rows):
        for col in range(cols):
            grid.append((col * px_size, row * px_size))

    total_tiles = len(grid)

    # Shuffle appearance order — edges/corners FIRST, center LAST
    random.seed(42)
    indexed = list(range(total_tiles))
    cx_mid, cy_mid = W / 2, H / 2
    # Sort by REVERSE distance from center (farthest first) with jitter
    indexed.sort(key=lambda i: (
        -math.sqrt((grid[i][0] + px_size / 2 - cx_mid) ** 2 +
                   (grid[i][1] + px_size / 2 - cy_mid) ** 2)
        + random.uniform(-40, 40)  # noqa: jitter for organic feel
    ))

    # Frame 1 = fully black, frames 2-13 = pixel fill, 14-16 = hold
    FILL_FRAMES = 13

    # Pre-calculate text position (centered, slightly above middle)
    txt = "Frondy"
    _bbox = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), txt, font=font_title)
    tw = _bbox[2] - _bbox[0]
    th = _bbox[3] - _bbox[1]
    tx = (W - tw) // 2 - _bbox[0]
    ty = (H - th) // 2 - _bbox[1] - 10

    # Version label centered under title
    ver = "v1.0.0"
    _bbox_v = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), ver, font=font_ver)
    vw = _bbox_v[2] - _bbox_v[0]
    vx = (W - vw) // 2
    vy = ty + th + 14

    sub = "WIFI PINEAPPLE PAGER"
    _bbox2 = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), sub, font=font_sub)
    stw = _bbox2[2] - _bbox2[0]
    sx = (W - stw) // 2
    sy = H - 26

    for frame_num in range(1, TOTAL_FRAMES + 1):
        img = Image.new("RGBA", (W, H), (*b, 255))
        d = ImageDraw.Draw(img)

        # Frame 1 = fully black, frames 2-FILL_FRAMES = progressive fill
        if frame_num == 1:
            count = 0
        elif frame_num <= FILL_FRAMES:
            count = int(total_tiles * (frame_num - 1) / (FILL_FRAMES - 1))
            count = min(count, total_tiles)
        else:
            count = total_tiles

        for j in range(count):
            i = indexed[j]
            px, py = grid[i]
            d.rectangle([px, py, px + px_size - 1, py + px_size - 1],
                        fill=(*y, 255))

        # Text — black on yellow (hidden until tiles reveal behind it)
        d.text((tx, ty), txt, fill=(*b, 255), font=font_title)
        d.text((vx, vy), ver, fill=(*b, 255), font=font_ver)
        d.text((sx, sy), sub, fill=(*b, 255), font=font_sub)

        # Boot LED indicator — black pill with 3 colored blinking dots
        # Mimics the physical device button LEDs (red A, green B, white d-pad)
        # As boot progresses, dots transition from hardware colors to yellow
        dot_r = 4
        dot_spacing = 14
        pill_w = dot_spacing * 2 + dot_r * 2 + 16  # width for 3 dots + padding
        pill_h = dot_r * 2 + 16  # extra top/bottom padding
        pill_x = W - pill_w - 10  # lower right
        pill_y = H - pill_h - 8
        pill_cx = pill_x + pill_w // 2
        pill_cy = pill_y + pill_h // 2

        # Check if tiles have reached the pill area
        check_x = min(pill_cx, W - 1)
        check_y = min(pill_cy, H - 1)
        dot_pixel = img.getpixel((check_x, check_y))
        pill_area_filled = dot_pixel[:3] == y

        if pill_area_filled and frame_num > 1:
            # Render pill + dots at 3x for anti-aliasing
            aa = 3
            pw, ph = pill_w * aa, pill_h * aa
            pill_img = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
            pd = ImageDraw.Draw(pill_img)
            # Black pill background with rounded ends
            pr = ph // 2
            pd.rounded_rectangle([0, 0, pw - 1, ph - 1], radius=pr,
                                  fill=(*b, 255))

            # Hardware colors → yellow transition
            # Progress: 0.0 at first pill frame, 1.0 at frame 16
            progress = (frame_num - 1) / (TOTAL_FRAMES - 1)

            hw_colors = [
                (220, 40, 40),    # red (A button)
                (40, 200, 40),    # green (B button)
                (220, 215, 200),  # white (d-pad)
            ]
            yel = (255, 200, 0)

            # Blend hardware color toward yellow based on progress
            def lerp_color(c1, c2, t):
                return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

            # Blink patterns — slower (~20% less frequent)
            # Each dot: 3 on, 3 off with different phase offsets
            blink_patterns = [
                (frame_num // 3) % 2 == 0,           # red: 3 on / 3 off
                ((frame_num + 2) // 3) % 2 == 0,     # green: offset by 2
                ((frame_num + 1) // 3) % 2 == 0,     # white: offset by 1
            ]

            cr = dot_r * aa
            cy_dot = ph // 2
            for i, (hw_col, is_on) in enumerate(zip(hw_colors, blink_patterns)):
                cx = pw // 2 + (i - 1) * dot_spacing * aa
                # Transition: early = hardware color, late = yellow
                color = lerp_color(hw_col, yel, progress ** 1.5)
                if is_on:
                    pd.ellipse([cx - cr, cy_dot - cr, cx + cr, cy_dot + cr],
                               fill=(*color, 255))
                else:
                    dim = tuple(c // 5 for c in color)
                    pd.ellipse([cx - cr, cy_dot - cr, cx + cr, cy_dot + cr],
                               fill=(*dim, 255))

            # Downscale and composite
            pill_sm = pill_img.resize((pill_w, pill_h), Image.LANCZOS)
            img.paste(pill_sm, (pill_x, pill_y), pill_sm)

        save(img, f"boot_animation/init-{frame_num}.png")


# ─── Keyboard ────────────────────────────────────────────────────────────────

def gen_keyboard():
    """Keyboard layouts — dark keys on black with yellow labels."""
    ensure_dir("keyboard")
    s = SS
    W, H = 480, 222

    try:
        kb_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 14 * s)
        kb_font_sm = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 10 * s)
    except Exception:
        kb_font = ImageFont.load_default()
        kb_font_sm = kb_font

    KEY_LABEL_COLOR = _c(YELLOW)

    SPECIAL = {
        "backspace": "\u2190", "capslock": "\u21e7", "done": "\u2713",
        "symbols_toggle": "#$", "space": "\u2423",
    }

    def draw_key_label(d, x, y, kw, kh, label):
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
        d.rectangle([8*s, 6*s, 472*s, 8*s], fill=_c(YELLOW_D))

    def draw_fn_row(d):
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

    # QWERTY lowercase
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

    # Symbols
    img, d = ss_start(W, H, BG)
    draw_input_area(d)
    draw_kb(d, [list("1234567890"), list("!@#$%^&*()"),
                list("~<>+=:;[]") + ["backspace"],
                ["capslock"] + list("_\"`{}|\\,.")])
    draw_fn_row(d)
    save(ss_finish(img, W, H), "keyboard/keyboard_layout_symbols.png")

    # Numeric
    img, d = ss_start(W, H, BG)
    draw_input_area(d)
    draw_kb(d, [list("789"), list("456"), list("123"),
                ["done", "0", "backspace"]],
            start_y=59, key_w=47, key_h=31)
    save(ss_finish(img, W, H), "keyboard/keyboard_layout_numeric.png")

    # IP
    img, d = ss_start(W, H, BG)
    draw_input_area(d)
    draw_kb(d, [["0", "1", "2", "3", "done"],
                ["/", "4", "5", "6", "backspace"],
                [".", "7", "8", "9"]],
            start_y=57, key_w=77, key_h=56, cols=5)
    save(ss_finish(img, W, H), "keyboard/keyboard_layout_ip.png")

    # Hex
    img, d = ss_start(W, H, BG)
    draw_input_area(d)
    draw_kb(d, [["0", "1", "2", "3", "4", "done"],
                ["5", "6", "7", "8", "9", "backspace"],
                list("ABCDEF")],
            start_y=57, key_w=77, key_h=56)
    save(ss_finish(img, W, H), "keyboard/keyboard_layout_hex.png")

    # Key highlight (47x31) — solid yellow fill, black text on top
    img, d = ss_start(47, 31)
    rrect(d, (0, 0, 46, 30), fill=YELLOW, radius=3)
    save(ss_finish(img, 47, 31), "keyboard/_key-bg.png")

    # Spacebar (188x31)
    img, d = ss_start(188, 31)
    rrect(d, (0, 0, 187, 30), fill=YELLOW, radius=3)
    save(ss_finish(img, 188, 31), "keyboard/_spacebar-4x.png")

    # Hex key (75x54)
    img, d = ss_start(75, 54)
    rrect(d, (0, 0, 74, 53), fill=YELLOW, radius=3)
    save(ss_finish(img, 75, 54), "keyboard/_hex-bg.png")


# ─── Dialogs ────────────────────────────────────────────────────────────────

def gen_dialogs():
    """Dialog backgrounds — clean black panels with yellow accent bars."""

    def make_dialog(w, h, accent=YELLOW):
        img, d = ss_start(w, h)
        s = SS
        # Main panel
        rrect(d, (0, 0, w-1, h-1), fill=BG, outline=DARK_GRAY, radius=5, width=1)

        # Top bar — yellow accent
        d.rectangle([0, 0, (w-1)*s, 3*s], fill=_c(accent, 180))

        # Bottom bar
        d.rectangle([0, (h-3)*s, (w-1)*s, (h-1)*s], fill=_c(accent, 80))

        return ss_finish(img, w, h)

    # Option dialogs (463x197)
    for name, color in [
        ("option_dialog_bg_windowed", YELLOW),
        ("option_dialog_bg_windowed_green", YELLOW),
        ("option_dialog_bg_windowed_purple", YELLOW),
        ("option_dialog_bg_windowed_red", RED),
        ("option_dialog_bg_narrow", YELLOW),
    ]:
        save(make_dialog(463, 197, accent=color), f"optiondialog/{name}.png")

    # Option button bg (59x71) — uniform thin outline, no thick left bar
    img, d = ss_start(59, 71)
    rrect(d, (0, 0, 58, 70), fill=PANEL, outline=YELLOW_D, radius=3, width=1)
    save(ss_finish(img, 59, 71), "optiondialog/button_bg.png")

    # Button outline (59x71) — yellow outline, no glow
    img, d = ss_start(59, 71)
    rrect(d, (0, 0, 58, 70), fill=(YELLOW[0], YELLOW[1], YELLOW[2], 10),
          outline=YELLOW, radius=3, width=2)
    save(ss_finish(img, 59, 71), "optiondialog/button_outline.png")

    # Check (24x19) — white, bolder
    img, d = ss_start(24, 19)
    d.line([(2*SS, 10*SS), (8*SS, 16*SS), (22*SS, 2*SS)], fill=_c(WHITE), width=3*SS)
    save(ss_finish(img, 24, 19), "optiondialog/check.png")

    # X (15x15) — white, bolder
    img, d = ss_start(15, 15)
    d.line([(2*SS, 2*SS), (12*SS, 12*SS)], fill=_c(WHITE), width=3*SS)
    d.line([(12*SS, 2*SS), (2*SS, 12*SS)], fill=_c(WHITE), width=3*SS)
    save(ss_finish(img, 15, 15), "optiondialog/x.png")

    # Alert dialog backgrounds
    for name, w, h, accent in [
        ("alert_dialog_bg_term", 398, 220, YELLOW),
        ("alert_dialog_bg_term_blue", 429, 222, YELLOW),
        ("alert_dialog_bg_term_error", 429, 222, RED),
        ("alert_dialog_bg_term_warning", 429, 222, YELLOW),
    ]:
        save(make_dialog(w, h, accent=accent), f"{name}.png")

    # Confirmation dialog bg (429x222)
    save(make_dialog(429, 222, accent=YELLOW), "confirmation_dialog_bg_term.png")

    # Confirmation buttons (121x41)
    # Selected = solid yellow fill (confirm/OK), deselected = outline ghost (cancel)
    # Deselected: outline-only ghost button
    img, d = ss_start(121, 41)
    rrect(d, (0, 0, 120, 40), fill=BG, outline=YELLOW_D, radius=3, width=1)
    save(ss_finish(img, 121, 41), "confirmation_dialog/generic_confirmation_button_deselected.png")
    # Selected: solid yellow fill
    img, d = ss_start(121, 41)
    rrect(d, (0, 0, 120, 40), fill=YELLOW, outline=YELLOW, radius=3, width=2)
    save(ss_finish(img, 121, 41), "confirmation_dialog/generic_confirmation_button_selected.png")

    # Edit string dialog bg (467x186)
    save(make_dialog(467, 186, accent=YELLOW), "edit_string_dialog_bg.png")

    # Dialog BG (480x222)
    save(make_dialog(480, 222, accent=YELLOW), "dialog_bg.png")

    # Messagebox (459x112)
    img, d = ss_start(459, 112)
    rrect(d, (0, 0, 458, 111), fill=BG, outline=DARK_GRAY, radius=3)
    d.rectangle([0, 0, 458*SS, 3*SS], fill=_c(YELLOW, 140))
    save(ss_finish(img, 459, 112), "messagebox.png")


# ─── Toggles / Radio / Checkbox ─────────────────────────────────────────────

def gen_toggles():
    """Toggle switches, radio buttons, checkbox — yellow accents."""
    s = SS

    # Toggle enabled bg (29x16)
    img, d = ss_start(29, 16)
    d.rounded_rectangle([0, 0, 28*s, 15*s], radius=8*s,
                        fill=_c(YELLOW, 35), outline=_c(YELLOW), width=s)
    save(ss_finish(img, 29, 16), "toggle/enabled/toggle_bg.png")

    # Toggle circle enabled (12x12)
    img, d = ss_start(12, 12)
    d.ellipse([0, 0, 11*s, 11*s], fill=_c(YELLOW))
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
    d.ellipse([0, 0, 10*s, 10*s], fill=_c(YELLOW))
    save(ss_finish(img, 11, 11), "radio/radio_selected.png")

    # Checkbox (20x20)
    img, d = ss_start(20, 20)
    rrect(d, (1, 1, 18, 18), outline=SOFT_W, radius=2, width=1)
    d.line([(5*s, 10*s), (8*s, 14*s), (15*s, 5*s)], fill=_c(YELLOW), width=2*s)
    save(ss_finish(img, 20, 20), "checkbox.png")


# ─── Recon ───────────────────────────────────────────────────────────────────

def gen_recon():
    """Recon screens and icons."""
    ensure_dir("recon")
    W, H = 480, 222

    # Recon dashboard (480x222)
    img = yj_frame_bg(W, H)
    save(ss_finish(img, W, H), "recon/recon_dashboard.png")

    # Recon list bg (480x222)
    img, d = ss_start(W, H, BG)
    s = SS
    # Top bar with yellow accent
    d.rectangle([0, 0, W*s, 10*s], fill=_c(PANEL))
    d.rectangle([0, 8*s, W*s, 10*s], fill=_c(YELLOW, 50))
    d.rectangle([120*s, 0, 122*s, 10*s], fill=_c(BG))
    d.rectangle([320*s, 0, 322*s, 10*s], fill=_c(BG))
    # Bottom bar
    d.rectangle([0, (H-10)*s, W*s, H*s], fill=_c(PANEL))
    d.rectangle([0, (H-10)*s, W*s, (H-8)*s], fill=_c(YELLOW, 35))
    # Row separators
    for y in range(42, 198, 34):
        d.line([(10*s, y*s), (470*s, y*s)], fill=_c(DARK_GRAY, 40), width=s)
    save(ss_finish(img, W, H), "recon/recon_list_bg.png")

    # Blank recon bg (480x222)
    img, d = ss_start(W, H, BG)
    d.rectangle([0, 0, W*s, 10*s], fill=_c(PANEL))
    d.rectangle([0, 8*s, W*s, 10*s], fill=_c(YELLOW, 50))
    d.rectangle([0, (H-10)*s, W*s, H*s], fill=_c(PANEL))
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
                c = [RED, YELLOW_D, YELLOW, YELLOW_L][level]
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
        ("enc_wpa2", YELLOW, False), ("enc_wpa3", YELLOW_L, False)
    ]:
        img, d = ss_start(20, 20)
        lock_icon(d, color, is_open)
        save(ss_finish(img, 20, 20), f"recon/{name}.png")

    # Clients (20x20)
    img, d = ss_start(20, 20)
    s = SS
    d.ellipse([3*s, 2*s, 9*s, 8*s], fill=_c(SOFT_W))
    d.ellipse([11*s, 2*s, 17*s, 8*s], fill=_c(SOFT_W))
    d.pieslice([1*s, 6*s, 11*s, 18*s], 0, 180, fill=_c(SOFT_W))
    d.pieslice([9*s, 6*s, 19*s, 18*s], 0, 180, fill=_c(SOFT_W))
    save(ss_finish(img, 20, 20), "recon/clients.png")


# ─── Full-Screen Backgrounds ────────────────────────────────────────────────

def gen_backgrounds():
    """Section backgrounds + all full-screen assets."""
    W, H = 480, 222

    def framed():
        img = yj_frame_bg(W, H)
        return ss_finish(img, W, H)

    def section():
        return ss_finish(yj_section_bg(W, H), W, H)

    # All section backgrounds — unified yellow, no per-section variation
    save(section(), "settings_bg.png")
    save(section(), "pineap_bg.png")
    save(section(), "alerts_dashboard/alerts_bg.png")
    save(section(), "payloads_dashboard/payloads_bg.png")
    save(section(), "payloads_dashboard/recon_payloads_bg.png")
    save(section(), "power_menu_bg.png")
    save(section(), "launch_payload_dialog/launch_payload_bg.png")

    # Payload log backgrounds
    img, d = ss_start(W, H, BG)
    s = SS
    d.rectangle([0, 0, W*s, 10*s], fill=_c(PANEL))
    d.rectangle([0, 8*s, W*s, 10*s], fill=_c(YELLOW, 45))
    d.rectangle([200*s, 0, 202*s, 10*s], fill=_c(BG))
    d.rectangle([0, (H-10)*s, W*s, H*s], fill=_c(PANEL))
    d.rectangle([0, (H-10)*s, W*s, (H-8)*s], fill=_c(YELLOW, 30))
    result = ss_finish(img, W, H)
    save(result, "payloadlog/payload_log_bg.png")
    save(result, "payload_log_bg.png")

    # Lock screen — pixel art padlock
    img, d = ss_start(W, H, BG)
    s = SS
    d.rectangle([0, 0, W*s, 3*s], fill=_c(YELLOW))
    d.rectangle([0, (H-3)*s, W*s, H*s], fill=_c(YELLOW_DD))
    # Pixel art lock — 8px grid blocks
    px = 8
    ox, oy = 200, 52  # origin
    lock_shackle = [  # top arc of shackle
        (4,0),(5,0),(6,0),
        (3,1),(7,1),
        (2,2),(8,2),
        (2,3),(8,3),
        (2,4),(8,4),
    ]
    lock_body = [  # rectangular body
        (1,5),(2,5),(3,5),(4,5),(5,5),(6,5),(7,5),(8,5),(9,5),
        (1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6),(8,6),(9,6),
        (1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),(9,7),
        (1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(7,8),(8,8),(9,8),
        (1,9),(2,9),(3,9),(4,9),(5,9),(6,9),(7,9),(8,9),(9,9),
        (1,10),(2,10),(3,10),(4,10),(5,10),(6,10),(7,10),(8,10),(9,10),
        (1,11),(2,11),(3,11),(4,11),(5,11),(6,11),(7,11),(8,11),(9,11),
    ]
    lock_keyhole = [(5,7),(5,8),(5,9)]  # keyhole cutout
    for bx, by in lock_shackle + lock_body:
        x1, y1 = (ox + bx * px) * s, (oy + by * px) * s
        d.rectangle([x1, y1, x1 + px*s - s, y1 + px*s - s], fill=_c(YELLOW))
    for bx, by in lock_keyhole:
        x1, y1 = (ox + bx * px) * s, (oy + by * px) * s
        d.rectangle([x1, y1, x1 + px*s - s, y1 + px*s - s], fill=_c(BG))
    save(ss_finish(img, W, H), "lock_screen.png")

    # Buttons locked
    img, d = ss_start(W, H, BG)
    d.rectangle([0, 0, W*s, 3*s], fill=_c(YELLOW))
    d.rectangle([0, (H-3)*s, W*s, H*s], fill=_c(YELLOW_DD))
    rrect(d, (140, 80, 340, 142), fill=PANEL, outline=DARK_GRAY, radius=3)
    save(ss_finish(img, W, H), "buttons_locked.png")

    # QR screens
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
            sd.rectangle([0, 0, W, 2], fill=YELLOW)
            sd.rectangle([0, H - 2, W, H], fill=YELLOW_DD)

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
            sd.text((tx, ty), url_text, fill=YELLOW, font=font_md)
            if extra:
                ty += 25
                for line in extra:
                    sd.text((tx, ty), line, fill=DARK_GRAY, font=font_sm)
                    ty += 16
            screen.save(os.path.join(ASSETS_DIR, f"{qr_name}.png"))
            os.unlink(tmp_path)
    except Exception:
        for qr_name, *_ in _qr_screens:
            base = framed()
            base_d = ImageDraw.Draw(base)
            base_d.rounded_rectangle([160, 28, 420, 194], radius=4, fill=_c(WHITE))
            save(base, f"{qr_name}.png")

    # Warning screens — pixel art triangle with exclamation + text labels
    # Text matches default themes: too_hot="TOO HOT / TURNING OFF",
    # dimming="TOO HOT / DIMMING SCREEN"
    warn_text = {
        "warn_device_too_hot": ("TOO HOT", "TURNING OFF"),
        "warn_device_dimming_screen": ("TOO HOT", "DIMMING SCREEN"),
    }
    try:
        warn_font_lg = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 18 * SS)
        warn_font_sm = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 14 * SS)
    except (IOError, OSError):
        warn_font_lg = ImageFont.load_default()
        warn_font_sm = ImageFont.load_default()
    for name, accent in [("warn_device_too_hot", RED), ("warn_device_dimming_screen", YELLOW)]:
        img, d = ss_start(W, H, BG)
        s = SS
        d.rectangle([0, 0, W*s, 4*s], fill=_c(accent))
        d.rectangle([0, (H-4)*s, W*s, H*s], fill=_c(accent))
        px = 8
        # Triangle: 10 rows * 8px = 80px, text ~45px, gap 8px = ~133px total
        # Usable area: 222 - 4 - 4 = 214px, center at 4 + 214/2 = 111
        # Group top = 111 - 133/2 ≈ 44
        ox, oy = 192, 36
        # Pixel art triangle (11 wide at base, 10 tall)
        tri_rows = [
            [5],
            [4,5,6],
            [3,4,5,6,7],
            [3,4,5,6,7],
            [2,3,4,5,6,7,8],
            [2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8,9],
            [1,2,3,4,5,6,7,8,9],
            [0,1,2,3,4,5,6,7,8,9,10],
            [0,1,2,3,4,5,6,7,8,9,10],
        ]
        for ry, cols in enumerate(tri_rows):
            for cx in cols:
                x1, y1 = (ox + cx * px) * s, (oy + ry * px) * s
                d.rectangle([x1, y1, x1 + px*s - s, y1 + px*s - s], fill=_c(accent))
        # Exclamation mark cutout
        for ry in range(3, 7):
            x1, y1 = (ox + 5 * px) * s, (oy + ry * px) * s
            d.rectangle([x1, y1, x1 + px*s - s, y1 + px*s - s], fill=_c(BG))
        # Dot
        x1, y1 = (ox + 5 * px) * s, (oy + 8 * px) * s
        d.rectangle([x1, y1, x1 + px*s - s, y1 + px*s - s], fill=_c(BG))
        # Text labels — centered below icon (8px gap after icon bottom)
        # Icon bottom = oy + 10*px = 28 + 80 = 108, then 8px gap
        line1, line2 = warn_text[name]
        text_top = (oy + 10 * px + 8) * s
        bbox1 = warn_font_lg.getbbox(line1)
        tw1 = bbox1[2] - bbox1[0]
        d.text(((W * s - tw1) // 2, text_top), line1, fill=_c(WHITE), font=warn_font_lg)
        bbox2 = warn_font_sm.getbbox(line2)
        tw2 = bbox2[2] - bbox2[0]
        d.text(((W * s - tw2) // 2, text_top + 25 * s), line2, fill=_c(accent), font=warn_font_sm)
        save(ss_finish(img, W, H), f"{name}.png")

    # Battery alerts — pixel art battery + text labels
    # Text matches default themes: low="LOW BATTERY", critical="CONNECT POWER"
    batt_text = {
        "low_battery_alert": "LOW BATTERY",
        "critical_battery_alert": "CONNECT POWER",
    }
    try:
        batt_font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 20 * SS)
    except (IOError, OSError):
        batt_font = ImageFont.load_default()
    for name, color in [("low_battery_alert", YELLOW), ("critical_battery_alert", RED)]:
        img, d = ss_start(W, H, BG)
        s = SS
        d.rectangle([0, 0, W*s, 4*s], fill=_c(color))
        d.rectangle([0, (H-4)*s, W*s, H*s], fill=_c(color))
        px = 8
        # Battery icon: 15 rows * 8px = 120px, text ~20px, gap 8px = ~148px total
        # Usable area: 222 - 4 (top bar) - 4 (bottom bar) = 214px, center at 4 + 214/2 = 111
        # Group top = 111 - 148/2 = 37
        ox, oy = 200, 37
        # Battery terminal (top nub)
        for bx in [3, 4, 5]:
            x1, y1 = (ox + bx * px) * s, (oy + 0 * px) * s
            d.rectangle([x1, y1, x1 + px*s - s, y1 + px*s - s], fill=_c(color))
        # Battery body outline (9 wide, 14 tall)
        body_outline = []
        for ry in range(1, 15):
            body_outline.append((0, ry))
            body_outline.append((8, ry))
        for bx in range(0, 9):
            body_outline.append((bx, 1))
            body_outline.append((bx, 14))
        for bx, by in body_outline:
            x1, y1 = (ox + bx * px) * s, (oy + by * px) * s
            d.rectangle([x1, y1, x1 + px*s - s, y1 + px*s - s], fill=_c(color))
        # Fill level
        fill_rows = 4 if "low" in name else 2
        for ry in range(14 - fill_rows, 14):
            for bx in range(1, 8):
                x1, y1 = (ox + bx * px) * s, (oy + ry * px) * s
                d.rectangle([x1, y1, x1 + px*s - s, y1 + px*s - s], fill=_c(color))
        # Text label — centered below battery icon (8px gap after icon bottom)
        # Icon bottom = oy + 15*px = 37 + 120 = 157, then 8px gap
        label = batt_text[name]
        bbox = batt_font.getbbox(label)
        tw = bbox[2] - bbox[0]
        text_x = (W * s - tw) // 2
        text_y = (oy + 15 * px + 8) * s
        d.text((text_x, text_y), label, fill=_c(color), font=batt_font)
        save(ss_finish(img, W, H), f"{name}.png")

    # Upgrade screens
    for name, color in [
        ("upgrade/checking_for_update-min", YELLOW),
        ("upgrade/downloading_upgrade", GREEN),
        ("upgrade/validating_upgrade", YELLOW_L),
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

    # Arrows (19x38)
    for name, flip in [("arrow_up", False), ("arrow_down", True)]:
        img, d = ss_start(19, 38)
        if not flip:
            d.polygon([(9*s, 2*s), (17*s, 18*s), (12*s, 18*s),
                       (12*s, 36*s), (6*s, 36*s), (6*s, 18*s), (1*s, 18*s)],
                      fill=_c(YELLOW))
        else:
            d.polygon([(9*s, 36*s), (17*s, 20*s), (12*s, 20*s),
                       (12*s, 2*s), (6*s, 2*s), (6*s, 20*s), (1*s, 20*s)],
                      fill=_c(YELLOW))
        save(ss_finish(img, 19, 38), f"{name}.png")

    # Small up/down (16x16)
    for name, pts in [("up", [(8, 2), (14, 13), (2, 13)]),
                      ("down", [(8, 13), (14, 2), (2, 2)])]:
        img, d = ss_start(16, 16)
        d.polygon([(p[0]*s, p[1]*s) for p in pts], fill=_c(SOFT_W))
        save(ss_finish(img, 16, 16), f"{name}.png")

    # Dividers (13x160) — yellow-tinted
    for name, color in [("divider", YELLOW_D), ("divleft", YELLOW_DD), ("divright", YELLOW_DD)]:
        img, d = ss_start(13, 160)
        d.rounded_rectangle([4*s, 0, 8*s, 159*s], radius=2*s, fill=_c(color))
        save(ss_finish(img, 13, 160), f"{name}.png")

    # Section-colored dividers — same yellow for all sections
    for sec in ['settings', 'pineap']:
        img, d = ss_start(13, 160)
        d.rounded_rectangle([4*s, 0, 8*s, 159*s], radius=2*s, fill=_c(YELLOW_DD))
        save(ss_finish(img, 13, 160), f"divleft_{sec}.png")
        img, d = ss_start(13, 160)
        d.rounded_rectangle([4*s, 0, 8*s, 159*s], radius=2*s, fill=_c(YELLOW_DD))
        save(ss_finish(img, 13, 160), f"divright_{sec}.png")

    # Menu icon (29x20) — three bars, yellow
    img, d = ss_start(29, 20)
    for y in [2, 8, 14]:
        d.rounded_rectangle([2*s, y*s, 26*s, (y + 4)*s], radius=2*s, fill=_c(YELLOW))
    save(ss_finish(img, 29, 20), "menu.png")

    # Menu disabled (29x20)
    img, d = ss_start(29, 20)
    for y in [2, 8, 14]:
        d.rounded_rectangle([2*s, y*s, 26*s, (y + 4)*s], radius=2*s, fill=_c(GRAY))
    save(ss_finish(img, 29, 20), "menu_disabled.png")

    # Info (29x20)
    img, d = ss_start(29, 20)
    rrect(d, (4, 0, 24, 19), outline=YELLOW, radius=3, width=1)
    d.ellipse([12*s, 3*s, 16*s, 7*s], fill=_c(YELLOW))
    d.rectangle([13*s, 9*s, 15*s, 16*s], fill=_c(YELLOW))
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
               (4*s, 7*s), (12*s, 7*s)], fill=_c(YELLOW), outline=_c(YELLOW_D))
    save(ss_finish(img, 29, 20), "wizard.png")

    # Disabled variants
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
    d.ellipse([9*s, 4*s, 13*s, 8*s], fill=_c(YELLOW))
    save(ss_finish(img, 23, 14), "client.png")

    # Disabled client (23x14)
    img, d = ss_start(23, 14)
    rrect(d, (0, 0, 22, 13), outline=GRAY, radius=2, width=1)
    d.ellipse([9*s, 4*s, 13*s, 8*s], fill=_c(GRAY))
    save(ss_finish(img, 23, 14), "disabled_client.png")

    # X (15x15) — white, bolder
    img, d = ss_start(15, 15)
    d.line([(2*s, 2*s), (12*s, 12*s)], fill=_c(WHITE), width=3*s)
    d.line([(12*s, 2*s), (2*s, 12*s)], fill=_c(WHITE), width=3*s)
    save(ss_finish(img, 15, 15), "x.png")

    # Triangle (13x15)
    img, d = ss_start(13, 15)
    d.polygon([(1*s, 14*s), (6*s, 1*s), (11*s, 14*s)], fill=_c(YELLOW))
    save(ss_finish(img, 13, 15), "triangle.png")

    # Start (20x20)
    img, d = ss_start(20, 20)
    d.polygon([(4*s, 2*s), (18*s, 10*s), (4*s, 18*s)], fill=_c(GREEN))
    save(ss_finish(img, 20, 20), "start.png")

    # Swap (20x20)
    img, d = ss_start(20, 20)
    d.polygon([(2*s, 5*s), (10*s, 1*s), (10*s, 9*s)], fill=_c(YELLOW))
    d.polygon([(18*s, 15*s), (10*s, 11*s), (10*s, 19*s)], fill=_c(YELLOW_D))
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
              fill=_c(YELLOW), outline=_c(YELLOW_D))
    save(ss_finish(img, 11, 17), "flame.png")

    # Folder (24x24)
    img, d = ss_start(24, 24)
    d.polygon([(1*s, 5*s), (10*s, 5*s), (12*s, 2*s), (22*s, 2*s), (22*s, 5*s)],
              fill=_c(YELLOW))
    rrect(d, (1, 5, 22, 21), fill=YELLOW, radius=2)
    save(ss_finish(img, 24, 24), "folder.png")

    # WiFi icon (25x25)
    img, d = ss_start(25, 25)
    d.arc([1*s, 1*s, 24*s, 24*s], 210, 330, fill=_c(YELLOW), width=2*s)
    d.arc([5*s, 5*s, 20*s, 20*s], 215, 325, fill=_c(YELLOW), width=2*s)
    d.arc([9*s, 9*s, 16*s, 16*s], 220, 320, fill=_c(YELLOW), width=s)
    d.ellipse([11*s, 18*s, 14*s, 21*s], fill=_c(YELLOW))
    save(ss_finish(img, 25, 25), "wifi_icon.png")

    # Alerts sub (26x9) — yellow pill
    img, d = ss_start(26, 9)
    d.rounded_rectangle([0, 0, 25*s, 8*s], radius=4*s, fill=_c(YELLOW))
    save(ss_finish(img, 26, 9), "alerts_dashboard/sub.png")

    # Payload dialog bg (135x70) — uniform thin outline, no thick left bar
    img, d = ss_start(135, 70)
    rrect(d, (0, 0, 134, 69), fill=PANEL, outline=YELLOW_D, radius=3, width=1)
    save(ss_finish(img, 135, 70), "payload_dialog_option_bg.png")

    # Payload dialog selected (136x71) — solid yellow fill
    img, d = ss_start(136, 71)
    rrect(d, (0, 0, 135, 70), fill=YELLOW,
          outline=YELLOW, radius=3, width=2)
    save(ss_finish(img, 136, 71), "payload_dialog_selected_box.png")

    # Pager device (88x62)
    img, d = ss_start(88, 62)
    rrect(d, (2, 2, 85, 59), fill=PANEL, outline=YELLOW_D, radius=3, width=1)
    rrect(d, (8, 8, 55, 38), fill=(YELLOW[0], YELLOW[1], YELLOW[2], 12),
          outline=YELLOW_DD, radius=2, width=1)
    d.ellipse([65*s, 15*s, 78*s, 28*s], outline=_c(SOFT_W), width=s)
    d.ellipse([65*s, 35*s, 78*s, 48*s], outline=_c(SOFT_W), width=s)
    save(ss_finish(img, 88, 62), "pager-16bit.png")

    # Payload log indicators
    for name, w, h, color in [
        ("payloadlog/payload_complete_indicator", 480, 43, GREEN),
        ("payloadlog/payload_error_indicator", 480, 44, RED),
        ("payloadlog/payload_running_indicator", 480, 43, YELLOW),
        ("payloadlog/payload_stopped_indicator", 480, 44, YELLOW_D),
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
            d.polygon([(6*s, 1*s), (11*s, 14*s), (1*s, 14*s)], fill=_c(YELLOW))
        else:
            d.polygon([(6*s, 14*s), (11*s, 1*s), (1*s, 1*s)], fill=_c(YELLOW))
        save(ss_finish(img, 12, 15), f"{name}.png")

    # Scroll pause (16x16)
    img, d = ss_start(16, 16)
    d.rectangle([3*s, 2*s, 6*s, 13*s], fill=_c(YELLOW))
    d.rectangle([9*s, 2*s, 12*s, 13*s], fill=_c(YELLOW))
    save(ss_finish(img, 16, 16), "payloadlog/scroll_pause_indicator.png")

    # Payloads dashboard arrow (20x18)
    img, d = ss_start(20, 18)
    d.polygon([(2*s, 9*s), (16*s, 2*s), (16*s, 16*s)], fill=_c(SOFT_W))
    save(ss_finish(img, 20, 18), "payloads_dashboard/arrow.png")

    # Launch animation frames — outline Frondy brand icon with pulse, 4 frames
    # V2 brand bitmap (11x13) — skull with frond pokies + X eye patch
    BRAND_BITMAP = [
        [0,0,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,1,0,1,0,0,0,0],
        [0,1,0,0,1,0,1,0,0,0,0],
        [0,1,0,1,1,0,1,0,1,0,0],
        [0,0,1,1,1,1,0,1,1,0,0],
        [0,0,1,1,1,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,1,1,1,0],  # forehead
        [0,1,0,1,0,1,0,0,1,1,0],  # X top
        [0,1,1,0,1,1,0,0,1,1,0],  # X center
        [0,1,0,1,0,1,0,0,1,1,0],  # X bottom
        [0,1,1,1,1,1,1,1,1,1,0],  # chin
        [0,0,1,1,1,1,1,1,1,0,0],
        [0,0,0,1,0,1,0,1,0,0,0],  # teeth
    ]
    bm_rows = len(BRAND_BITMAP)
    bm_cols = len(BRAND_BITMAP[0])

    for fi in range(4):
        w, h = 113, 106
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))

        # Scale: fit brand bitmap into ~70% of frame height
        target_h = int(h * 0.70)
        px_size = target_h // bm_rows
        icon_w = bm_cols * px_size
        icon_h = bm_rows * px_size
        ox = (w - icon_w) // 2
        oy = (h - icon_h) // 2

        # Pulse alpha: breathe in/out across 4 frames
        outline_alpha = [140, 200, 255, 200][fi]
        outline_width = [1, 1, 2, 1][fi]
        glow_alpha = [0, 20, 40, 20][fi]

        # Build filled region mask for outline extraction
        filled = Image.new("L", (w, h), 0)
        fd = ImageDraw.Draw(filled)
        for r, row in enumerate(BRAND_BITMAP):
            for c, val in enumerate(row):
                if val:
                    px = ox + c * px_size
                    py = oy + r * px_size
                    fd.rectangle([px, py, px + px_size - 1, py + px_size - 1], fill=255)

        # Extract outline by finding edge pixels
        filled_px = filled.load()
        d = ImageDraw.Draw(img)
        yc = (255, 200, 0)

        for y in range(h):
            for x in range(w):
                if filled_px[x, y] > 0:
                    # Check if this pixel is on the edge (has a transparent neighbor)
                    is_edge = False
                    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                        nx, ny = x + dx, y + dy
                        if nx < 0 or ny < 0 or nx >= w or ny >= h:
                            is_edge = True
                            break
                        if filled_px[nx, ny] == 0:
                            is_edge = True
                            break
                    if is_edge:
                        # Outline pixel
                        img.putpixel((x, y), (*yc, outline_alpha))
                        # Thicker outline on frame 3
                        if outline_width > 1:
                            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                                nx, ny = x + dx, y + dy
                                if 0 <= nx < w and 0 <= ny < h:
                                    existing = img.getpixel((nx, ny))
                                    if existing[3] < outline_alpha:
                                        img.putpixel((nx, ny), (*yc, outline_alpha // 2))
                    elif glow_alpha > 0:
                        # Inner glow fill on brighter frames
                        img.putpixel((x, y), (*yc, glow_alpha))

        save(img, f"launch_payload_dialog/animation/anim_frame_{fi + 1}.png")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print(f"Generating Frondy assets → {ASSETS_DIR}")
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
