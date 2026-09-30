# Harajat ikonkasi: tilla tanga ustida dollar belgisi. Ishlatish: python3 make_icon.py <res_papka> | preview.png
import sys, os
from PIL import Image, ImageDraw, ImageFilter

def lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def grad(size, c1, c2):
    g = Image.new('RGB', (1, size))
    for y in range(size): g.putpixel((0, y), lerp(c1, c2, y / (size - 1)))
    return g.resize((size, size))

def dollar(d, cx, cy, h, w, col):
    import math
    rc = (h - w) / 4.0
    top, bot = (cx, cy - rc), (cx, cy + rc)
    ro = rc + w / 2
    d.arc([cx - ro, top[1] - ro, cx + ro, top[1] + ro], 90, 330, fill=col, width=int(w))
    d.arc([cx - ro, bot[1] - ro, cx + ro, bot[1] + ro], 270, 150, fill=col, width=int(w))
    for (c, a) in ((top, 330), (top, 90), (bot, 270), (bot, 150)):
        x, y = c[0] + rc * math.cos(math.radians(a)), c[1] + rc * math.sin(math.radians(a))
        d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=col)
    bw = w * 0.32
    d.rounded_rectangle([cx - bw / 2, cy - h / 2 - w * 0.55, cx + bw / 2, cy + h / 2 + w * 0.55], radius=bw / 2, fill=col)

def coin(S):
    K = 2; N = S * K
    im = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    D = N * 0.86; x0 = (N - D) / 2
    sh = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([x0, x0 + N * .03, x0 + D, x0 + D + N * .03], fill=(0, 0, 0, 90))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(N * .02)))
    def disc(box, c1, c2):
        m = Image.new('L', (N, N), 0); ImageDraw.Draw(m).ellipse(box, fill=255)
        im.paste(grad(N, c1, c2), (0, 0), m)
    disc([x0, x0, x0 + D, x0 + D], (255, 214, 102), (196, 128, 12))
    p = D * .07; disc([x0 + p, x0 + p, x0 + D - p, x0 + D - p], (196, 128, 12), (255, 226, 130))
    q = D * .11; disc([x0 + q, x0 + q, x0 + D - q, x0 + D - q], (255, 205, 80), (240, 165, 30))
    d = ImageDraw.Draw(im); c = N / 2
    dollar(d, c, c + N * .007, D * .54, D * .062, (255, 238, 180, 140))
    dollar(d, c, c, D * .54, D * .062, (10, 84, 76, 255))
    hl = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    ImageDraw.Draw(hl).arc([x0 + q * 1.3, x0 + q * 1.3, x0 + D - q * 1.3, x0 + D - q * 1.3], 200, 260, fill=(255, 255, 255, 150), width=int(D * .022))
    im.alpha_composite(hl)
    return im.resize((S, S), Image.LANCZOS)

def legacy(S, round_=False):
    K = 2; N = S * K
    bg = grad(N, (15, 118, 110), (6, 62, 56)).convert('RGBA')
    m = Image.new('L', (N, N), 0)
    dm = ImageDraw.Draw(m)
    if round_: dm.ellipse([0, 0, N - 1, N - 1], fill=255)
    else: dm.rounded_rectangle([0, 0, N - 1, N - 1], radius=int(N * .22), fill=255)
    out = Image.new('RGBA', (N, N), (0, 0, 0, 0)); out.paste(bg, (0, 0), m)
    cn = coin(N).resize((int(N * .86), int(N * .86)), Image.LANCZOS)
    out.alpha_composite(cn, ((N - cn.width) // 2, (N - cn.height) // 2))
    return out.resize((S, S), Image.LANCZOS)

if __name__ == '__main__':
    t = sys.argv[1]
    if t.endswith('.png'):
        legacy(1024).save(t); sys.exit()
    for dens, leg, fg in (('mdpi', 48, 108), ('hdpi', 72, 162), ('xhdpi', 96, 216), ('xxhdpi', 144, 324), ('xxxhdpi', 192, 432)):
        d = os.path.join(t, 'mipmap-' + dens); os.makedirs(d, exist_ok=True)
        legacy(leg).save(d + '/ic_launcher.png'); legacy(leg, True).save(d + '/ic_launcher_round.png')
        c = coin(fg); f = Image.new('RGBA', (fg, fg), (0, 0, 0, 0))
        s = int(fg * .70); c = c.resize((s, s), Image.LANCZOS); f.alpha_composite(c, ((fg - s) // 2, (fg - s) // 2))
        f.save(d + '/ic_launcher_foreground.png')
    v = os.path.join(t, 'values'); os.makedirs(v, exist_ok=True)
    open(v + '/ic_launcher_background.xml', 'w').write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#0B5D54</color>\n</resources>\n')
