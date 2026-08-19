from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
import math
import random

INPUT = "your_banner.png"
OUTPUT = "github_pixel_art_animated.gif"

img = Image.open(INPUT).convert("RGBA")
W, H = img.size
random.seed(42)

# Floating pixel positions
particles = []
for _ in range(28):
    x = random.randint(15, W - 15)
    y = random.randint(8, H - 15)
    r = random.choice([1, 1, 1, 2])
    phase = random.random() * 2 * math.pi
    particles.append((x, y, r, phase))

frames = []

for i in range(20):
    # Very subtle brightness breathing
    factor = 1.0 + 0.018 * math.sin(2 * math.pi * i / 20)
    frame = ImageEnhance.Brightness(img.convert("RGB")).enhance(factor).convert("RGBA")

    # Monitor glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    pulse = (math.sin(2 * math.pi * i / 10) + 1) / 2
    alpha = int(10 + 18 * pulse)
    gd.rectangle((318, 198, 560, 340),
                 outline=(40, 130, 255, alpha), width=2)
    gd.rectangle((333, 215, 515, 330),
                 outline=(30, 170, 255, alpha // 2), width=1)
    frame = Image.alpha_composite(frame, glow.filter(ImageFilter.GaussianBlur(4)))

    # Subtle screen flicker
    screen = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(screen)
    flicker = (math.sin(2 * math.pi * (i + 2) / 7) + 1) / 2
    a = int(6 + 16 * flicker)
    sd.rectangle((145, 260, 290, 370), fill=(35, 130, 255, a))
    sd.rectangle((161, 276, 274, 335), fill=(70, 190, 255, a // 2))
    frame = Image.alpha_composite(frame, screen.filter(ImageFilter.GaussianBlur(2)))

    # Floating pixels
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for x, y, r, phase in particles:
        yy = y + int(2 * math.sin(phase + 2 * math.pi * i / 20))
        twinkle = (math.sin(phase + 2 * math.pi * i / 10) + 1) / 2
        a = int(25 + 80 * twinkle)
        od.rectangle((x, yy, x + r, yy + r),
                     fill=(130, 190, 255, a))
    frame = Image.alpha_composite(frame, overlay)

    # Blinking cursor/glow near the main monitor
    cursor = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cursor)
    if i % 4 != 3:
        cd.rectangle((475, 289, 481, 296), fill=(255, 80, 220, 220))
    frame = Image.alpha_composite(frame, cursor)

    frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=128))

frames[0].save(
    OUTPUT,
    save_all=True,
    append_images=frames[1:],
    duration=90,   # milliseconds per frame
    loop=0,        # infinite loop
    optimize=True,
    disposal=2
)

print(f"Created: {OUTPUT}")
