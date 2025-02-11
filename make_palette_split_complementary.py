#!/usr/bin/env python3
import sys
import random
import colorsys
import math
from .color_data import COLORS, color_families

# ----------------------------
# Conversion & Utility Functions
# ----------------------------
def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    r = int(hex_code[0:2], 16) / 255.0
    g = int(hex_code[2:4], 16) / 255.0
    b = int(hex_code[4:6], 16) / 255.0
    return (r, g, b)

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(
        int(rgb[0]*255),
        int(rgb[1]*255),
        int(rgb[2]*255)
    )

def hex_to_rgb_tuple(hex_code):
    hex_code = hex_code.lstrip('#')
    return (int(hex_code[0:2], 16), int(hex_code[2:4], 16), int(hex_code[4:6], 16))

def color_distance(rgb1, rgb2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)))

def find_closest_color_name(target_hex, color_dict):
    target_rgb = hex_to_rgb_tuple(target_hex)
    closest_name = None
    min_dist = float('inf')
    for name, hex_code in color_dict.items():
        current_rgb = hex_to_rgb_tuple(hex_code)
        dist = color_distance(target_rgb, current_rgb)
        if dist < min_dist:
            min_dist = dist
            closest_name = name
    return closest_name

def shift_hue(hex_code, degree_offset):
    r, g, b = hex_to_rgb(hex_code)
    H, L, S = colorsys.rgb_to_hls(r, g, b)
    offset = degree_offset / 360.0
    new_H = (H + offset) % 1.0
    new_rgb = colorsys.hls_to_rgb(new_H, L, S)
    return rgb_to_hex(new_rgb)

# ----------------------------
# Split-Complementary Palette Functions
# ----------------------------
def split_complementary_palette_4(base_hex, split_offset_degrees=30, analogous_offset_degrees=15):
    """
    Returns 4 colors:
      - Color 1: Base.
      - Colors 2 & 3: Two split-complementary variants (computed from the base's complement).
      - Color 4: Chosen by a 50/50 decision: either an analogous variant of the base (using +15°)
        or a random color from Broad Neutrals.
    """
    # Convert base to HLS.
    base_rgb = hex_to_rgb(base_hex)
    H, L, S = colorsys.rgb_to_hls(*base_rgb)
    # Complement of base.
    comp_H = (H + 0.5) % 1.0
    # Compute split offsets.
    offset = split_offset_degrees / 360.0
    split1_H = (comp_H + offset) % 1.0
    split2_H = (comp_H - offset) % 1.0
    color1 = rgb_to_hex(colorsys.hls_to_rgb(H, L, S))
    color2 = rgb_to_hex(colorsys.hls_to_rgb(split1_H, L, S))
    color3 = rgb_to_hex(colorsys.hls_to_rgb(split2_H, L, S))
    # Decide on fourth color.
    use_analogous = random.choice([True, False])
    broad_neutrals = color_families.get("Broad Neutrals", [])
    # Check if any of the first three (by name) are in Broad Neutrals.
    first3_names = {find_closest_color_name(c, COLORS) for c in [color1, color2, color3]}
    if not use_analogous and any(n in broad_neutrals for n in first3_names):
        use_analogous = True
    if use_analogous:
        color4 = shift_hue(base_hex, analogous_offset_degrees)
    else:
        random_neutral = random.choice(broad_neutrals)
        color4 = COLORS[random_neutral]
    return [color1, color2, color3, color4]

def split_complementary_palette_5(base_hex, split_offset_degrees=30, analogous_offset_degrees=15):
    """
    Returns 5 colors. We start with the 4-color split-complementary palette and then add an extra color.
    The extra color is chosen as follows:
      - If the 4-color version used an analogous variant for the fourth color, we add the opposite analogous variant
        (i.e. base shifted by -analogous_offset_degrees) if it isn't already present.
      - Otherwise (if a Broad Neutral was chosen), we add a second random Broad Neutral (that is unique).
    """
    max_attempts = 50  # Prevent infinite loops
    for attempt in range(max_attempts):
        base_palette = split_complementary_palette_4(base_hex, split_offset_degrees, analogous_offset_degrees)
        # Determine what the fourth color was.
        fourth_name = find_closest_color_name(base_palette[3], COLORS)
        extra_color = None

        if fourth_name in color_families.get("Broad Neutrals", []):
            # Fourth was a Broad Neutral; pick another different one.
            current_names = [find_closest_color_name(h, COLORS) for h in base_palette]
            candidates = [n for n in color_families.get("Broad Neutrals", [])
                        if n not in current_names]
            if candidates:
                extra_color = COLORS[random.choice(candidates)]
        else:
            # Fourth was analogous; add the opposite analogous variant.
            extra_color = shift_hue(base_hex, -analogous_offset_degrees)

        if extra_color is None:
            continue

        # Verify extra_color is unique
        full_palette = base_palette + [extra_color]
        if len(set([find_closest_color_name(h, COLORS) for h in full_palette])) == 5:
            return full_palette

    # If we couldn't generate a valid 5-color palette after max attempts,
    # fall back to the 4-color palette plus a random color
    base_palette = split_complementary_palette_4(base_hex, split_offset_degrees, analogous_offset_degrees)
    all_colors = list(COLORS.keys())
    current_names = [find_closest_color_name(h, COLORS) for h in base_palette]

    while all_colors:
        random_color = random.choice(all_colors)
        if random_color not in current_names:
            return base_palette + [COLORS[random_color]]
        all_colors.remove(random_color)

    # Absolute fallback - just duplicate the last color if everything else fails
    return base_palette + [base_palette[-1]]

def generate_random_base_color():
    families = ['Reds', 'Pinks', 'Oranges', 'Yellows', 'Greens', 'Blues', 'Purples']
    candidate_colors = []
    for fam in families:
        candidate_colors.extend(color_families.get(fam, []))
    random_color_name = random.choice(candidate_colors)
    return random_color_name, COLORS[random_color_name]

def generate_split_complementary_palette_4():
    """Generate a 4-color split-complementary palette ensuring unique names."""
    max_attempts = 50

    for _ in range(max_attempts):
        _, base_hex = generate_random_base_color()
        palette_hexes = split_complementary_palette_4(base_hex)
        palette_names = [find_closest_color_name(h, COLORS) for h in palette_hexes]
        if len(set(palette_names)) == 4:
            return palette_names

    # Fallback: Try with different offset values
    for split_offset in [45, 60]:  # Try larger split offsets
        _, base_hex = generate_random_base_color()
        palette_hexes = split_complementary_palette_4(base_hex, split_offset_degrees=split_offset)
        palette_names = [find_closest_color_name(h, COLORS) for h in palette_hexes]
        if len(set(palette_names)) == 4:
            return palette_names

    # Ultimate fallback - generate any 4 unique colors
    all_colors = list(COLORS.keys())
    palette = []
    while len(palette) < 4 and all_colors:
        candidate = random.choice(all_colors)
        if candidate not in palette:
            palette.append(candidate)
        all_colors.remove(candidate)

    # If we still don't have 4 colors, pad with duplicates
    while len(palette) < 4:
        palette.append(palette[-1])

    return palette

def generate_split_complementary_palette_5():
    """Generate a 5-color split-complementary palette ensuring unique names."""
    max_attempts = 50

    for _ in range(max_attempts):
        _, base_hex = generate_random_base_color()
        palette_hexes = split_complementary_palette_5(base_hex)
        palette_names = [find_closest_color_name(h, COLORS) for h in palette_hexes]
        if len(set(palette_names)) == 5:
            return palette_names

    # Fallback: Try with different offset values
    for split_offset in [45, 60]:  # Try larger split offsets
        _, base_hex = generate_random_base_color()
        palette_hexes = split_complementary_palette_5(base_hex, split_offset_degrees=split_offset)
        palette_names = [find_closest_color_name(h, COLORS) for h in palette_hexes]
        if len(set(palette_names)) == 5:
            return palette_names

    # Ultimate fallback - generate any 5 unique colors
    all_colors = list(COLORS.keys())
    palette = []
    while len(palette) < 5 and all_colors:
        candidate = random.choice(all_colors)
        if candidate not in palette:
            palette.append(candidate)
        all_colors.remove(candidate)

    # If we still don't have 5 colors, pad with duplicates
    while len(palette) < 5:
        palette.append(palette[-1])

    return palette

if __name__ == '__main__':
    five_flag = '-5' in sys.argv
    if five_flag:
        palette = generate_split_complementary_palette_5()
    else:
        palette = generate_split_complementary_palette_4()
    print("Split-Complementary Palette (Color Names):", palette)