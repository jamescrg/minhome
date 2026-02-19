#!/usr/bin/env python3
from PIL import Image, ImageDraw


def draw_house(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    s = size / 24  # Scale from 24x24 viewBox
    color = "#3f6212"  # Matcha green matching favicon
    width = max(2 * s, 1)

    # House body: M3 10v9a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-9
    body_points = [
        (3 * s, 10 * s),
        (3 * s, 19 * s),
        (5 * s, 21 * s),
        (19 * s, 21 * s),
        (21 * s, 19 * s),
        (21 * s, 10 * s),
    ]
    draw.line(body_points, fill=color, width=round(width), joint="curve")

    # Roof: M3 10 l9-8 l9 8 (simplified from the arc path)
    roof_points = [
        (3 * s, 10 * s),
        (12 * s, 3 * s),
        (21 * s, 10 * s),
    ]
    draw.line(roof_points, fill=color, width=round(width), joint="curve")

    # Door: M9 21v-8h6v8
    door_points = [
        (9 * s, 21 * s),
        (9 * s, 13 * s),
        (15 * s, 13 * s),
        (15 * s, 21 * s),
    ]
    draw.line(door_points, fill=color, width=round(width), joint="curve")

    return img


sizes = [
    (16, "icon-16.png"),
    (32, "icon-32.png"),
    (48, "icon.png"),
    (128, "icon-128.png"),
]

for size, filename in sizes:
    icon = draw_house(size)
    icon.save(filename, "PNG")
    print(f"Generated {filename} ({size}x{size})")

print("All icons generated successfully!")
