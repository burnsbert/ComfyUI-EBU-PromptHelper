#!/usr/bin/env python3
import sys
import random
import colorsys
import math
from .color_data import COLORS, color_families

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    r = int(hex_code[0:2], 16) / 255.0
    g = int(hex_code[2:4], 16) / 255.0
    b = int(hex_code[4:6], 16) / 255.0
    return (r, g, b)

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))

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

def complementary_palette(base_hex):
    """Returns 4 colors: base, complement, analogous (+15°), complement of analogous."""
    base = base_hex
    comp = shift_hue(base_hex, 180)
    analogous = shift_hue(base_hex, 15)
    comp_analogous = shift_hue(analogous, 180)
    return [base, comp, analogous, comp_analogous]

def complementary_palette_5(base_hex):
    """
    Returns 5 colors:
      [base, complement, analogous (+15°), extra analogous variant (-15°), complement-of-analogous (+15°)]
    """
    base = base_hex
    comp = shift_hue(base_hex, 180)
    analogous = shift_hue(base_hex, 15)
    extra = shift_hue(base_hex, -15)
    comp_analogous = shift_hue(analogous, 180)
    return [base, comp, analogous, extra, comp_analogous]

def generate_random_base_color():
    families = ['Reds', 'Pinks', 'Oranges', 'Yellows', 'Greens', 'Blues', 'Purples']
    candidate_colors = []
    for fam in families:
        candidate_colors.extend(color_families.get(fam, []))
    name = random.choice(candidate_colors)
    return name, COLORS[name]

def generate_complementary_palette():
    """Generate 4-color complementary palette ensuring unique names."""
    max_attempts = 50

    for _ in range(max_attempts):
        _, base_hex = generate_random_base_color()
        palette_hexes = complementary_palette(base_hex)
        palette_names = [find_closest_color_name(h, COLORS) for h in palette_hexes]
        if len(set(palette_names)) == 4:
            return palette_names

    # Fallback: If we can't get 4 unique colors after max attempts,
    # start with base and complement, then add unique colors
    _, base_hex = generate_random_base_color()
    comp_hex = shift_hue(base_hex, 180)
    base_name = find_closest_color_name(base_hex, COLORS)
    comp_name = find_closest_color_name(comp_hex, COLORS)

    # Start with base and complement
    palette = [base_name, comp_name]

    # Try to add two more unique colors
    all_colors = list(COLORS.keys())
    while len(palette) < 4 and all_colors:
        candidate = random.choice(all_colors)
        if candidate not in palette:
            palette.append(candidate)
        all_colors.remove(candidate)

    # If we still don't have 4 colors, pad with duplicates
    while len(palette) < 4:
        palette.append(palette[-1])

    return palette

def generate_complementary_palette_5():
    """Generate 5-color complementary palette ensuring unique names."""
    max_attempts = 50

    for _ in range(max_attempts):
        _, base_hex = generate_random_base_color()
        palette_hexes = complementary_palette_5(base_hex)
        palette_names = [find_closest_color_name(h, COLORS) for h in palette_hexes]
        if len(set(palette_names)) == 5:
            return palette_names

    # Fallback: If we can't get 5 unique colors after max attempts,
    # start with base and complement, then add unique colors
    _, base_hex = generate_random_base_color()
    comp_hex = shift_hue(base_hex, 180)
    base_name = find_closest_color_name(base_hex, COLORS)
    comp_name = find_closest_color_name(comp_hex, COLORS)

    # Start with base and complement
    palette = [base_name, comp_name]

    # Try to add three more unique colors
    all_colors = list(COLORS.keys())
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
        palette = generate_complementary_palette_5()
    else:
        palette = generate_complementary_palette()
    print("Complementary Palette (Color Names):", palette)