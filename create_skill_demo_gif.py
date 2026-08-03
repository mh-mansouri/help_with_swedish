from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1200, 640
OUTPUT = Path("assets/skill-demo.gif")


def get_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


TITLE_FONT = get_font(36)
SUBTITLE_FONT = get_font(24)
BODY_FONT = get_font(22)
SMALL_FONT = get_font(18)


def draw_background(draw: ImageDraw.ImageDraw, step: int) -> None:
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill="#07111f")
    draw.rectangle((30, 30, WIDTH - 30, HEIGHT - 30), outline="#1e293b", width=4)
    for y in range(60, HEIGHT - 60, 80):
        draw.line((40, y, WIDTH - 40, y), fill=(255, 255, 255, 20), width=1)

    # accent bar
    bar_width = 180 + step * 90
    draw.rounded_rectangle((70, 90, 70 + bar_width, 120), radius=15, fill="#22c55e")


def draw_frame(step: int) -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), "#07111f")
    draw = ImageDraw.Draw(img)
    draw_background(draw, step)

    # header
    draw.text((80, 40), "Help with Swedish", font=TITLE_FONT, fill="#f8fafc")
    draw.text((80, 80), "A practical learning path for Swedish learners", font=SUBTITLE_FONT, fill="#94a3b8")

    # left speech bubble
    draw.rounded_rectangle((80, 155, 520, 285), radius=24, fill="#e2e8f0", outline="#94a3b8", width=2)
    draw.text((110, 185), "User", font=BODY_FONT, fill="#0f172a")
    draw.text((110, 220), "“I’m A2 and want to improve", font=SMALL_FONT, fill="#334155")
    draw.text((110, 246), "speaking before a trip to Sweden.”", font=SMALL_FONT, fill="#334155")

    # right skill bubble
    draw.rounded_rectangle((620, 155, 1120, 335), radius=24, fill="#1d4ed8", outline="#38bdf8", width=2)
    draw.text((650, 185), "Skill", font=BODY_FONT, fill="#f8fafc")
    draw.text((650, 220), "Level: around A2", font=SMALL_FONT, fill="#dbeafe")
    draw.text((650, 246), "Goal: speaking + listening", font=SMALL_FONT, fill="#dbeafe")
    draw.text((650, 272), "Next step: short clips + daily shadowing", font=SMALL_FONT, fill="#dbeafe")

    # recommendations section
    draw.rounded_rectangle((80, 380, 1120, 560), radius=24, fill="#0f172a", outline="#334155", width=2)
    draw.text((110, 410), "Recommended channels", font=BODY_FONT, fill="#f8fafc")

    channels = [
        ("Peter SFI", "Grammar and clear speech"),
        ("Lätt Svenska med Oskar", "Slow, natural conversations"),
        ("Swedish Shadowing", "Pronunciation drills"),
    ]

    box_x = 110
    box_y = 445
    box_w = 300
    box_h = 80
    for index, (title, subtitle) in enumerate(channels):
        x = box_x + index * 320
        draw.rounded_rectangle((x, box_y, x + box_w, box_y + box_h), radius=16, fill="#111827", outline="#475569", width=2)
        draw.text((x + 18, box_y + 16), title, font=SMALL_FONT, fill="#f8fafc")
        draw.text((x + 18, box_y + 44), subtitle, font=ImageFont.load_default(), fill="#94a3b8")

    # animated highlight based on frame
    if step >= 2:
        highlight = 110 + min(step - 2, 2) * 320
        draw.rounded_rectangle((highlight, 445, highlight + 300, 525), radius=16, fill="#14532d", outline="#4ade80", width=3)

    # footer message
    if step <= 2:
        draw.text((100, 575), "Pick a level, choose a skill, and take one small step.", font=SMALL_FONT, fill="#cbd5e1")
    elif step <= 4:
        draw.text((100, 575), "You choose the pace. Ready for one small step?", font=SMALL_FONT, fill="#cbd5e1")
    else:
        # Note: Pillow doesn't shape Arabic-script text, so Persian is spelled
        # out in English here rather than drawn as "فارسی" (which renders as
        # disconnected, unshaped glyphs). The real webpage renders it correctly
        # via the browser.
        draw.text((100, 575), "Also works as a webpage — Swedish, English, Persian — no account needed.", font=SMALL_FONT, fill="#cbd5e1")

    return img


def build_gif() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frames = [draw_frame(step) for step in range(8)]
    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=700,
        loop=0,
        optimize=False,
    )


if __name__ == "__main__":
    build_gif()
    print(f"Created {OUTPUT}")
