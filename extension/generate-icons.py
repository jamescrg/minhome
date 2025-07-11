#!/usr/bin/env python3
from PIL import Image, ImageDraw


def draw_bookmark_plus(size):
    # Create a new image with transparency
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Scale factor
    scale = size / 16

    # Lime-600 color
    lime_green = "#65A30D"

    # Draw bookmark outline
    # Simplified version - draw as a rectangle with cut bottom
    bookmark_points = []

    # Top left corner with rounding
    bookmark_points.extend(
        [
            (4 * scale, 0 * scale),
            (12 * scale, 0 * scale),
            (14 * scale, 2 * scale),
            (14 * scale, 15.5 * scale),
            (8 * scale, 13.101 * scale),
            (2 * scale, 15.5 * scale),
            (2 * scale, 2 * scale),
            (4 * scale, 0 * scale),
        ]
    )

    # Draw filled bookmark
    draw.polygon(bookmark_points, fill=lime_green)

    # Draw inner cutout (to create outline effect)
    inner_points = [
        (4 * scale, 1 * scale),
        (12 * scale, 1 * scale),
        (13 * scale, 2 * scale),
        (13 * scale, 14.566 * scale),
        (8 * scale, 12.084 * scale),
        (3 * scale, 14.566 * scale),
        (3 * scale, 2 * scale),
        (4 * scale, 1 * scale),
    ]

    # Create a mask for the inner cutout
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.polygon(inner_points, fill=255)

    # Apply the mask to create the outline effect
    img_with_cutout = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    img_with_cutout.paste(img, (0, 0))
    img_with_cutout.paste((0, 0, 0, 0), (0, 0), mask)

    # Draw the plus sign
    plus_width = 1 * scale
    plus_center_x = 8 * scale
    plus_center_y = 6.5 * scale
    plus_size = 2 * scale

    # Horizontal bar of plus
    draw.rectangle(
        [
            (plus_center_x - plus_size, plus_center_y - plus_width / 2),
            (plus_center_x + plus_size, plus_center_y + plus_width / 2),
        ],
        fill=lime_green,
    )

    # Vertical bar of plus
    draw.rectangle(
        [
            (plus_center_x - plus_width / 2, plus_center_y - plus_size),
            (plus_center_x + plus_width / 2, plus_center_y + plus_size),
        ],
        fill=lime_green,
    )

    return img


# Generate icons in different sizes
sizes = [
    (16, "icon-16.png"),
    (32, "icon-32.png"),
    (48, "icon.png"),
    (128, "icon-128.png"),
]

for size, filename in sizes:
    icon = draw_bookmark_plus(size)
    icon.save(filename, "PNG")
    print(f"Generated {filename} ({size}x{size})")

print("All icons generated successfully!")
