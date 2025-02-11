#!/usr/bin/env python3
import sys
import random
import math
import colorsys
from .color_data import COLORS, color_families

# ----------------------------
# Conversion & Utility Functions
# ----------------------------
def hex_to_rgb(hex_code):
    """Convert a hex color code to an RGB tuple with components in the range [0, 1]."""
    hex_code = hex_code.lstrip('#')
    if len(hex_code) != 6:
        raise ValueError("Hex code must be 6 digits long.")
    r = int(hex_code[0:2], 16) / 255.0
    g = int(hex_code[2:4], 16) / 255.0
    b = int(hex_code[4:6], 16) / 255.0
    return (r, g, b)

def rgb_to_hex(rgb):
    """Convert an RGB tuple with components in the range [0, 1] to a hex color code."""
    return '#{:02x}{:02x}{:02x}'.format(
        int(rgb[0] * 255),
        int(rgb[1] * 255),
        int(rgb[2] * 255)
    )

def hex_to_rgb_tuple(hex_code):
    """Convert a hex code to an (R, G, B) tuple with values 0-255."""
    hex_code = hex_code.lstrip('#')
    return (
        int(hex_code[0:2], 16),
        int(hex_code[2:4], 16),
        int(hex_code[4:6], 16)
    )

def color_distance(rgb1, rgb2):
    """Compute the Euclidean distance between two RGB colors (in 0-255 space)."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)))

def find_closest_color_name(target_hex, color_dict):
    """
    Given a target hex code and a dictionary mapping color names to hex codes,
    return the name of the closest matching color based on Euclidean distance in RGB space.
    """
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

def shift_hue(hex_code, degree_offset=15):
    """
    Shifts the hue of the given hex color by the specified degree offset.
    The degree_offset is added to the hue (in degrees) and wrapped around if necessary.
    """
    r, g, b = hex_to_rgb(hex_code)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    offset = degree_offset / 360.0
    new_h = (h + offset) % 1.0
    new_rgb = colorsys.hls_to_rgb(new_h, l, s)
    return rgb_to_hex(new_rgb)

# ----------------------------
# Triadic Palette Functions
# ----------------------------
def triadic_palette(base_hex):
    """
    Given a base hex color code, returns a list of three hex color codes that form a triadic palette.
    The palette consists of the original color and two additional colors that are 120° apart.
    """
    base_rgb = hex_to_rgb(base_hex)
    base_h, base_l, base_s = colorsys.rgb_to_hls(*base_rgb)
    hue2 = (base_h + 1/3) % 1.0
    hue3 = (base_h + 2/3) % 1.0
    color2 = rgb_to_hex(colorsys.hls_to_rgb(hue2, base_l, base_s))
    color3 = rgb_to_hex(colorsys.hls_to_rgb(hue3, base_l, base_s))
    return [base_hex, color2, color3]

def generate_random_triadic_palette():
    """
    1. Picks a random color from the families: Reds, Pinks, Oranges, Yellows, Greens, Blues, Purples.
    2. Generates a triadic palette (3 colors) using the selected color.
    3. Converts the hex codes to their closest color names.
    4. Returns a list of 3 color names.
    """
    families = ['Reds', 'Pinks', 'Oranges', 'Yellows', 'Greens', 'Blues', 'Purples']
    candidate_colors = []
    for fam in families:
        candidate_colors.extend(color_families.get(fam, []))
    random_color_name = random.choice(candidate_colors)
    base_hex = COLORS[random_color_name]
    palette_hexes = triadic_palette(base_hex)
    palette_names = [find_closest_color_name(h, COLORS) for h in palette_hexes]
    return palette_names

def generate_four_color_palette():
    """
    Builds on the 3-color triadic palette to add a fourth color.
    The fourth color is chosen from one of three methods (analogous, tetradic, or Broad Neutral)
    so that the final palette has 4 unique color names.
    """
    max_attempts = 50
    for _ in range(max_attempts):
        triadic_names = generate_random_triadic_palette()
        base_color_name = triadic_names[0]
        base_hex = COLORS[base_color_name]

        allowed_methods = ['analogous', 'tetradic']
        broad_neutrals = color_families.get('Broad Neutrals', [])
        if not any(name in broad_neutrals for name in triadic_names):
            allowed_methods.append('broad_neutral')

        methods_to_try = allowed_methods.copy()
        fourth_color_name = None

        while methods_to_try:
            chosen_method = random.choice(methods_to_try)
            if chosen_method == 'analogous':
                fourth_hex = shift_hue(base_hex, degree_offset=15)
            elif chosen_method == 'tetradic':
                fourth_hex = shift_hue(base_hex, degree_offset=180)
            elif chosen_method == 'broad_neutral':
                fourth_name_candidate = random.choice(broad_neutrals)
                fourth_hex = COLORS[fourth_name_candidate]
            else:
                raise ValueError("Unknown method selected.")

            candidate_name = find_closest_color_name(fourth_hex, COLORS)
            if candidate_name not in triadic_names:
                fourth_color_name = candidate_name
                break
            else:
                methods_to_try.remove(chosen_method)

        if fourth_color_name is not None:
            palette = triadic_names + [fourth_color_name]
            if len(set(palette)) == 4:
                return palette

    # Fallback: If we can't get 4 unique colors after max attempts,
    # start with triadic palette and add any unique color
    triadic_names = generate_random_triadic_palette()
    all_colors = list(COLORS.keys())
    while all_colors:
        random_color = random.choice(all_colors)
        if random_color not in triadic_names:
            return triadic_names + [random_color]
        all_colors.remove(random_color)

    # Ultimate fallback - duplicate the last color if everything else fails
    return triadic_names + [triadic_names[-1]]

def generate_triadic_palette_5():
    """
    Builds on the 3-color triadic palette to add two extra colors for a total of 5.
    For each extra slot, there is an independent 50% chance of selecting a color from Broad Neutrals;
    otherwise, an analogous variant is generated.
    """
    max_attempts = 50
    for _ in range(max_attempts):
        triadic_names = generate_random_triadic_palette()
        base_color_name = triadic_names[0]
        base_hex = COLORS[base_color_name]
        broad_neutrals = color_families.get("Broad Neutrals", [])
        current_palette = triadic_names.copy()

        # Try to add two extra colors
        for i in range(2):
            if random.random() < 0.5 and broad_neutrals:
                # Filter out colors already in the palette
                available_neutrals = [n for n in broad_neutrals if n not in current_palette]
                if available_neutrals:
                    extra_name = random.choice(available_neutrals)
                    current_palette.append(extra_name)
                    continue

            # If we couldn't use a neutral or random chose analogous
            offset = 15 if i == 0 else -15
            extra_hex = shift_hue(base_hex, degree_offset=offset)
            extra_name = find_closest_color_name(extra_hex, COLORS)
            if extra_name not in current_palette:
                current_palette.append(extra_name)

        if len(current_palette) == 5 and len(set(current_palette)) == 5:
            return current_palette

    # Fallback: If we can't get 5 unique colors,
    # start with triadic palette and add unique random colors
    triadic_names = generate_random_triadic_palette()
    current_palette = triadic_names.copy()
    all_colors = list(COLORS.keys())

    while len(current_palette) < 5 and all_colors:
        random_color = random.choice(all_colors)
        if random_color not in current_palette:
            current_palette.append(random_color)
        all_colors.remove(random_color)

    # If we still don't have 5 colors, pad with duplicates
    while len(current_palette) < 5:
        current_palette.append(current_palette[-1])

    return current_palette

# ----------------------------
# Main Execution
# ----------------------------
if __name__ == "__main__":
    use_five = '-5' in sys.argv
    if use_five:
        palette = generate_triadic_palette_5()
    else:
        palette = generate_four_color_palette()
    print("Triadic Palette (Color Names):", palette)