from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUT = ASSETS / "og-luke-kennard.png"

W, H = 1200, 630
FONT_REG = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
FONT_BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")


def font(path, size):
    return ImageFont.truetype(str(path), size)


regular = font(FONT_REG, 28)
small = font(FONT_REG, 19)
tiny = font(FONT_BOLD, 17)
bold = font(FONT_BOLD, 32)
display = font(FONT_BOLD, 82)
stat_font = font(FONT_BOLD, 42)


def draw_wrapped(draw, xy, text, font_obj, fill, max_width, line_gap=8):
    x, y = xy
    words = text.split()
    lines = []
    current = ""
    for word in words:
        probe = f"{current} {word}".strip()
        if draw.textbbox((0, 0), probe, font=font_obj)[2] <= max_width:
            current = probe
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    for line in lines:
        draw.text((x, y), line, font=font_obj, fill=fill)
        y += font_obj.size + line_gap
    return y


bg = Image.new("RGBA", (W, H), (12, 7, 38, 255))
draw = ImageDraw.Draw(bg)

for r, alpha in [(760, 42), (560, 58), (360, 74)]:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.ellipse((W - r // 2 - 120, -r // 2 - 160, W + r // 2 - 120, r // 2 + 160), fill=(229, 96, 32, alpha))
    bg = Image.alpha_composite(bg, layer.filter(ImageFilter.GaussianBlur(26)))

pattern = Image.new("RGBA", (W, H), (0, 0, 0, 0))
pd = ImageDraw.Draw(pattern)
for x in range(-160, W + 220, 58):
    pd.line((x, H, x + 330, 0), fill=(255, 184, 28, 34), width=3)
for y in range(88, H, 92):
    pd.line((0, y, W, y - 48), fill=(255, 255, 255, 18), width=2)
bg = Image.alpha_composite(bg, pattern)
draw = ImageDraw.Draw(bg)

draw.rectangle((0, 0, W, H), outline=(229, 96, 32, 255), width=10)
draw.text((70, 58), "PHOENIX SUNS · GET TO KNOW", font=bold, fill=(255, 255, 255, 245))
draw.text((72, 96), "PREPARED BY ACCELERATED VELOCITY CONSULTING", font=tiny, fill=(255, 184, 28, 235))

draw.text((70, 164), "LUKE", font=display, fill=(255, 255, 255, 255))
draw.text((70, 250), "KENNARD", font=display, fill=(247, 148, 29, 255))
draw_wrapped(
    draw,
    (74, 356),
    "A clean shooting correction for Phoenix: elite spacing, simple role clarity, and a specialist skill that travels.",
    regular,
    (239, 235, 228, 235),
    575,
    8,
)

stats = [("47.8%", "REPORTED 3P"), ("$13M", "REPORTED DEAL"), ("2017", "NO. 12 PICK")]
x = 72
for value, label in stats:
    draw.rounded_rectangle((x, 512, x + 168, 582), radius=16, fill=(12, 7, 38, 190), outline=(255, 184, 28, 132), width=2)
    draw.text((x + 17, 521), value, font=stat_font, fill=(255, 255, 255, 255))
    draw.text((x + 18, 560), label, font=tiny, fill=(255, 184, 28, 240))
    x += 188

portrait = Image.open(ASSETS / "luke-kennard.png").convert("RGBA")
portrait.thumbnail((500, 600), Image.Resampling.LANCZOS)
px = 770
py = 72 + (500 - portrait.height) // 2

plate = Image.new("RGBA", (430, 504), (255, 255, 255, 0))
pdraw = ImageDraw.Draw(plate)
pdraw.rounded_rectangle((0, 0, 430, 504), radius=30, fill=(255, 255, 255, 24), outline=(255, 255, 255, 72), width=2)
pdraw.rounded_rectangle((20, 392, 410, 482), radius=20, fill=(12, 7, 38, 210), outline=(229, 96, 32, 180), width=2)
bg.alpha_composite(plate, (730, 62))
bg.alpha_composite(portrait, (px, py))

draw = ImageDraw.Draw(bg)
draw.text((766, 474), "REPORTED SUNS SIGNING", font=tiny, fill=(255, 184, 28, 245))
draw.text((766, 502), "Elite shooting specialist", font=bold, fill=(255, 255, 255, 245))
draw.text((766, 545), "Get to Know · Player Feature", font=small, fill=(239, 235, 228, 210))
draw.text((955, 578), "AVC", font=bold, fill=(255, 255, 255, 170))

bg.convert("RGB").save(OUT, quality=95)
print(OUT)
