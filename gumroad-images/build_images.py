from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

FONT_DIR = "C:/Users/Logik/AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin/cdd47fdc-94d4-447a-9151-b9bc37b9dbfd/0619674c-e402-45d3-a3a5-7b1a06542619/skills/canvas-design/canvas-fonts"
OUT_DIR = "C:/Users/Logik/OneDrive/Desktop/LogicalCoders/gumroad-images"

NAVY_DARK = (15, 37, 87)      # #0f2557
NAVY_MID  = (30, 58, 138)     # #1e3a8a
BLUE      = (37, 99, 235)     # #2563eb
LIGHT_BLUE= (147, 197, 253)   # #93c5fd
AMBER     = (245, 158, 11)    # #f59e0b
WHITE     = (255, 255, 255)
INK       = (30, 41, 59)      # #1e293b

def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)

def vertical_gradient(size, top, bottom):
    w, h = size
    base = Image.new("RGB", (1, h), color=0)
    for y in range(h):
        t = y / max(h - 1, 1)
        r = int(top[0] + (bottom[0]-top[0]) * t)
        g = int(top[1] + (bottom[1]-top[1]) * t)
        b = int(top[2] + (bottom[2]-top[2]) * t)
        base.putpixel((0, y), (r, g, b))
    return base.resize((w, h))

def diagonal_gradient(size, c1, c2, c3):
    w, h = size
    img = Image.new("RGB", (w, h))
    px = img.load()
    maxsum = w + h
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            t = (x + y) / maxsum
            if t < 0.5:
                tt = t / 0.5
                r = int(c1[0] + (c2[0]-c1[0]) * tt)
                g = int(c1[1] + (c2[1]-c1[1]) * tt)
                b = int(c1[2] + (c2[2]-c1[2]) * tt)
            else:
                tt = (t - 0.5) / 0.5
                r = int(c2[0] + (c3[0]-c2[0]) * tt)
                g = int(c2[1] + (c3[1]-c2[1]) * tt)
                b = int(c2[2] + (c3[2]-c2[2]) * tt)
            for yy in range(y, min(y+2, h)):
                for xx in range(x, min(x+2, w)):
                    px[xx, yy] = (r, g, b)
    return img

def rounded_rect(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def draw_shield_check(draw, cx, cy, s, fill, check_color):
    # shield outline
    pts = [
        (cx, cy - s),
        (cx + s*0.85, cy - s*0.62),
        (cx + s*0.85, cy + s*0.15),
        (cx, cy + s*1.15),
        (cx - s*0.85, cy + s*0.15),
        (cx - s*0.85, cy - s*0.62),
    ]
    draw.polygon(pts, fill=fill)
    # checkmark
    lw = max(int(s*0.14), 4)
    draw.line([(cx - s*0.38, cy + s*0.02), (cx - s*0.08, cy + s*0.32)], fill=check_color, width=lw, joint="curve")
    draw.line([(cx - s*0.08, cy + s*0.32), (cx + s*0.45, cy - s*0.35)], fill=check_color, width=lw, joint="curve")

def draw_doc_icon(draw, box, fill, line_color):
    x0, y0, x1, y1 = box
    rounded_rect(draw, box, radius=int((x1-x0)*0.08), fill=fill)
    pad = (x1 - x0) * 0.18
    line_gap = (y1 - y0 - 2*pad) / 4
    for i in range(4):
        ly = y0 + pad + i*line_gap
        lw_ratio = 0.64 if i < 3 else 0.4
        draw.line([(x0+pad, ly), (x0+pad + (x1-x0-2*pad)*lw_ratio, ly)],
                   fill=line_color, width=max(int((x1-x0)*0.035),3))

def make_card(w, h, label, sub, accent):
    card = Image.new("RGBA", (w, h), (0,0,0,0))
    d = ImageDraw.Draw(card)
    rounded_rect(d, (0,0,w-1,h-1), radius=22, fill=(255,255,255,255))
    d.rectangle([0,0, 10, h], fill=accent)
    rounded_rect(d, (0,0,10,h), radius=8, fill=accent)
    icon_box = (26, 22, 26+int(w*0.26), 22+int(w*0.26))
    draw_doc_icon(d, icon_box, fill=(240,246,255,255), line_color=(*NAVY_MID, 255))
    f_label = font("InstrumentSans-Bold.ttf", 22)
    f_sub   = font("WorkSans-Regular.ttf", 15)
    d.text((28, icon_box[3] + 14), label, font=f_label, fill=(*NAVY_DARK,255))
    d.text((28, icon_box[3] + 46), sub, font=f_sub, fill=(90,105,130,255))
    return card

def text_w(draw, txt, f):
    b = draw.textbbox((0,0), txt, font=f)
    return b[2]-b[0], b[3]-b[1]

# ============================================================
# COVER IMAGE — 1280x720
# ============================================================
W, H = 1280, 720
cover = diagonal_gradient((W,H), NAVY_DARK, NAVY_MID, BLUE)
cover = cover.convert("RGB")
d = ImageDraw.Draw(cover, "RGBA")

# subtle dot grid texture, top-left quadrant only, low opacity
for gy in range(0, 260, 26):
    for gx in range(0, 260, 26):
        d.ellipse([gx, gy, gx+2.4, gy+2.4], fill=(255,255,255,26))

# badge
badge_f = font("WorkSans-Bold.ttf" if False else "WorkSans-Regular.ttf", 20)
badge_txt = "DIGITAL DOWNLOAD  ·  EDITABLE WORD FILES"
bw, bh = text_w(d, badge_txt, badge_f)
bx0, by0 = 72, 66
pad_x, pad_y = 20, 10
rounded_rect(d, (bx0, by0, bx0+bw+2*pad_x, by0+bh+2*pad_y), radius=20,
             fill=(147,197,253,38), outline=(147,197,253,140), width=1)
d.text((bx0+pad_x, by0+pad_y-2), badge_txt, font=badge_f, fill=(191,219,254,255))

# headline (two lines, left-aligned, left column ~ 62% width)
h1 = font("InstrumentSans-Bold.ttf", 52)
line1 = "Small Business"
line2 = "Compliance Starter Kit"
ly = 150
d.text((70, ly), line1, font=h1, fill=WHITE)
d.text((70, ly+70), line2, font=h1, fill=WHITE)

# subtitle (wrapped to two lines, capped width so it never reaches the card grid)
sub_f = font("WorkSans-Regular.ttf", 23)
d.text((72, ly+158), "HIPAA  ·  NIST CSF  ·  Startup Compliance", font=sub_f, fill=(191,219,254,255))
d.text((72, ly+194), "Access Review Templates", font=sub_f, fill=(191,219,254,255))

# amber divider accent
d.rectangle([72, ly+248, 72+90, ly+253], fill=AMBER)

# credit line
credit_f = font("WorkSans-Regular.ttf", 22)
d.text((72, H-70), "by Logical Coders", font=credit_f, fill=(226,232,255,230))
tagline_f = font("WorkSans-Regular.ttf", 18)
d.text((72, H-42), "South Tampa, FL", font=tagline_f, fill=(147,197,253,200))

# 4 document cards in a clean, non-overlapping 2x2 grid on the right
card_w, card_h = 235, 205
gap = 20
grid_x0, grid_y0 = 745, 145
labels = [("HIPAA", "Privacy Notice"), ("NIST CSF", "Policy Package"),
          ("Startup", "Compliance Checklist"), ("Access Review", "Report Template")]
positions = [(0,0), (1,0), (0,1), (1,1)]
angles = [-2.5, 2, 2.5, -2]
for i, (col, row) in enumerate(positions):
    lbl, sub = labels[i]
    card = make_card(card_w, card_h, lbl, sub, AMBER if i in (0,3) else BLUE)
    card = card.rotate(angles[i], expand=True, resample=Image.BICUBIC)
    px = grid_x0 + col*(card_w+gap) - (card.size[0]-card_w)//2
    py = grid_y0 + row*(card_h+gap) - (card.size[1]-card_h)//2
    shadow_blur = card.split()[3].filter(ImageFilter.GaussianBlur(9))
    shadow_layer = Image.new("RGBA", cover.size, (0,0,0,0))
    shadow_solid = Image.new("RGBA", card.size, (0,0,0,85))
    shadow_solid.putalpha(shadow_blur)
    shadow_layer.paste(shadow_solid, (px+6, py+10), shadow_solid)
    cover.paste(shadow_layer, (0,0), shadow_layer)
    cover.paste(card, (px, py), card)

cover.save(f"{OUT_DIR}/cover_compliance_starter_kit.png")
print("cover saved")

# ============================================================
# THUMBNAIL — 600x600
# ============================================================
S = 600
thumb = diagonal_gradient((S,S), NAVY_DARK, NAVY_MID, BLUE).convert("RGB")
d2 = ImageDraw.Draw(thumb, "RGBA")

for gy in range(0, S, 30):
    for gx in range(0, S, 30):
        d2.ellipse([gx, gy, gx+2, gy+2], fill=(255,255,255,16))

# shield + check icon, centered upper area
draw_shield_check(d2, S//2, 205, 92, fill=WHITE, check_color=BLUE)
# amber ring accent behind shield (drawn first would be better, but keep simple outline ring)
d2.ellipse([S//2-135, 205-135, S//2+135, 205+135], outline=(245,158,11,160), width=4)

# product name
h2 = font("InstrumentSans-Bold.ttf", 46)
name1 = "Compliance"
name2 = "Starter Kit"
w1,_ = text_w(d2, name1, h2)
w2,_ = text_w(d2, name2, h2)
d2.text(((S-w1)/2, 358), name1, font=h2, fill=WHITE)
d2.text(((S-w2)/2, 414), name2, font=h2, fill=WHITE)

# amber underline
uw = 110
d2.rectangle([(S-uw)/2, 480, (S-uw)/2+uw, 485], fill=AMBER)

# small credit
cf = font("WorkSans-Regular.ttf", 20)
ctxt = "LOGICAL CODERS"
cw,_ = text_w(d2, ctxt, cf)
d2.text(((S-cw)/2, 505), ctxt, font=cf, fill=(191,219,254,230))

thumb.save(f"{OUT_DIR}/thumbnail_compliance_starter_kit.png")
print("thumbnail saved")
