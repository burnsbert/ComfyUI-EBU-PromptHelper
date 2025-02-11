#!/usr/bin/env python3
import sys
import random
from .color_data import COLORS, color_families

def generate_art_house_palette_4():
    greys = color_families.get("Greys", [])
    if len(greys) < 3:
        raise ValueError("Not enough grey colors available.")

    warm_colors = set(color_families.get("Warm Colors", []))
    excluded = set(color_families.get("Metallics", [])) | set(color_families.get("Greys", [])) | set(color_families.get("Pastels", []))
    valid_warm = list(warm_colors - excluded)
    if not valid_warm:
        raise ValueError("No valid Warm Colors available.")

    max_attempts = 50
    for _ in range(max_attempts):
        grey_palette = random.sample(greys, 3)
        warm_color = random.choice(valid_warm)
        palette = grey_palette + [warm_color]
        if len(set(palette)) == 4:
            return palette

    # Fallback: If we couldn't get 4 unique colors after max attempts,
    # try different combinations of greys and warm colors
    grey_palette = random.sample(greys, 3)
    for warm_color in valid_warm:
        palette = grey_palette + [warm_color]
        if len(set(palette)) == 4:
            return palette

    # Ultimate fallback - use any 3 unique greys and duplicate the last one
    grey_palette = random.sample(greys, 3)
    return grey_palette + [grey_palette[-1]]

def generate_art_house_palette_5():
    greys = color_families.get("Greys", [])
    if len(greys) < 4:
        raise ValueError("Not enough grey colors available for 5-color palette.")

    warm_colors = set(color_families.get("Warm Colors", []))
    excluded = set(color_families.get("Metallics", [])) | set(color_families.get("Greys", [])) | set(color_families.get("Pastels", []))
    valid_warm = list(warm_colors - excluded)
    if not valid_warm:
        raise ValueError("No valid Warm Colors available.")

    max_attempts = 50
    for _ in range(max_attempts):
        grey_palette = random.sample(greys, 4)
        warm_color = random.choice(valid_warm)
        palette = grey_palette + [warm_color]
        if len(set(palette)) == 5:
            return palette

    # Fallback: If we couldn't get 5 unique colors after max attempts,
    # try different combinations of greys and warm colors
    grey_palette = random.sample(greys, 4)
    for warm_color in valid_warm:
        palette = grey_palette + [warm_color]
        if len(set(palette)) == 5:
            return palette

    # Ultimate fallback - use any 4 unique greys and duplicate the last one
    grey_palette = random.sample(greys, 4)
    return grey_palette + [grey_palette[-1]]

if __name__ == '__main__':
    use_five = '-5' in sys.argv
    if use_five:
        palette = generate_art_house_palette_5()
    else:
        palette = generate_art_house_palette_4()
    print("Art-House Palette (Unique Color Names):", palette)
