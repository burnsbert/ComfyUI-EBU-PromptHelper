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
        int(rgb[0] * 255),
        int(rgb[1] * 255),
        int(rgb[2] * 255)
    )

def hex_to_rgb_tuple(hex_code):
    hex_code = hex_code.lstrip('#')
    return (int(hex_code[0:2], 16),
            int(hex_code[2:4], 16),
            int(hex_code[4:6], 16))

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
# Compound (Double Split-Complementary) 5-Color Palette Function
# ----------------------------
def compound_palette_five(base_hex, analogous_offset=15, split_offset=30):
    color1 = base_hex
    color2 = shift_hue(base_hex, analogous_offset)
    color3 = shift_hue(base_hex, 180 - split_offset)
    color4 = shift_hue(base_hex, 180 + split_offset)
    color5 = shift_hue(base_hex, -analogous_offset)
    return [color1, color2, color3, color4, color5]

def generate_random_base_color():
    families = ['Reds', 'Pinks', 'Oranges', 'Yellows', 'Greens', 'Blues', 'Purples']
    candidate_colors = []
    for fam in families:
        candidate_colors.extend(color_families.get(fam, []))
    name = random.choice(candidate_colors)
    return name, COLORS[name]

def generate_modified_compound_palette_five():
    """
    Generate a 5-color compound (double split-complementary) palette.
    """
    max_attempts = 50

    for _ in range(max_attempts):
        _, base_hex = generate_random_base_color()
        palette_hexes = compound_palette_five(base_hex, analogous_offset=15, split_offset=30)
        palette_names = [find_closest_color_name(h, COLORS) for h in palette_hexes]
        if len(set(palette_names)) == 5:
            return palette_names

    # Fallback: If we can't get 5 unique colors after max attempts,
    # try with different offset values
    for offset_mult in [1.2, 1.5, 2.0]:  # Try larger offsets
        _, base_hex = generate_random_base_color()
        palette_hexes = compound_palette_five(
            base_hex,
            analogous_offset=15 * offset_mult,
            split_offset=30 * offset_mult
        )
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

def generate_modified_compound_palette_four_from_five():
    """
    Generate a 4-color palette by randomly sampling 4 colors from the 5-color compound palette.
    """
    max_attempts = 50

    for _ in range(max_attempts):
        five_palette = generate_modified_compound_palette_five()
        four_palette = random.sample(five_palette, 4)
        if len(set(four_palette)) == 4:
            return four_palette

    # Fallback: If we can't get 4 unique colors after max attempts,
    # generate a new 5-color palette and take the first 4 unique colors
    five_palette = generate_modified_compound_palette_five()
    unique_colors = []
    seen = set()

    for color in five_palette:
        if color not in seen and len(unique_colors) < 4:
            unique_colors.append(color)
            seen.add(color)

    # If we still don't have 4 colors, pad with duplicates
    while len(unique_colors) < 4:
        unique_colors.append(unique_colors[-1])

    return unique_colors

if __name__ == '__main__':
    use_five = '-5' in sys.argv
    if use_five:
        palette = generate_modified_compound_palette_five()
    else:
        palette = generate_modified_compound_palette_four_from_five()
    print("Compound Palette (Color Names):", palette)