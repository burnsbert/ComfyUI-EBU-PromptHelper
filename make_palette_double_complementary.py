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
# Double Complementary (Tetradic) Palette Functions
# ----------------------------
def tetradic_palette(hex_code, shift_fraction=1/6):
    """
    Generate a tetradic palette from a base hex color.
    Returns 4 hex color codes that form two complementary pairs.
    """
    base_rgb = hex_to_rgb(hex_code)
    base_h, base_l, base_s = colorsys.rgb_to_hls(*base_rgb)
    h1 = base_h
    h2 = (base_h + 0.5) % 1.0
    h3 = (base_h + shift_fraction) % 1.0
    h4 = (base_h + shift_fraction + 0.5) % 1.0
    return [rgb_to_hex(colorsys.hls_to_rgb(h1, base_l, base_s)),
            rgb_to_hex(colorsys.hls_to_rgb(h2, base_l, base_s)),
            rgb_to_hex(colorsys.hls_to_rgb(h3, base_l, base_s)),
            rgb_to_hex(colorsys.hls_to_rgb(h4, base_l, base_s))]

def generate_random_base_color():
    families = ['Reds', 'Pinks', 'Oranges', 'Yellows', 'Greens', 'Blues', 'Purples']
    candidate_colors = []
    for fam in families:
        candidate_colors.extend(color_families.get(fam, []))
    random_color_name = random.choice(candidate_colors)
    return random_color_name, COLORS[random_color_name]

def generate_double_complementary_palette_4():
    """Generate a 4-color double complementary (tetradic) palette."""
    greys = set(color_families.get("Greys", []))
    while True:
        _, base_hex = generate_random_base_color()
        palette_hexes = tetradic_palette(base_hex)
        palette_names = [find_closest_color_name(h, COLORS) for h in palette_hexes]
        if len(set(palette_names)) == 4 and not any(palette_names.count(n) > 1 for n in greys):
            return palette_names

def generate_double_complementary_palette_5():
    """
    Generate a 5-color double complementary (tetradic) palette.
    We start with the 4-color palette and add an extra analogous variant of the base (e.g. base+30°)
    if it’s unique.
    """
    while True:
        base_name, base_hex = generate_random_base_color()
        base_palette = tetradic_palette(base_hex)
        extra = shift_hue(base_hex, 30)
        palette_hexes = base_palette + [extra]
        palette_names = [find_closest_color_name(h, COLORS) for h in palette_hexes]
        if len(set(palette_names)) == 5:
            return palette_names

if __name__ == '__main__':
    five_flag = '-5' in sys.argv
    if five_flag:
        palette = generate_double_complementary_palette_5()
    else:
        palette = generate_double_complementary_palette_4()
    print("Double Complementary Palette (Color Names):", palette)
