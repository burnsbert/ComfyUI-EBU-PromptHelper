#!/usr/bin/env python3
import sys
import random
from .color_data import COLORS

def generate_chaotic_palette(num_colors=4):
    all_colors = list(COLORS.keys())
    return random.sample(all_colors, num_colors)

if __name__ == '__main__':
    use_five = '-5' in sys.argv
    num = 5 if use_five else 4
    palette = generate_chaotic_palette(num_colors=num)
    print(f"Chaotic {num}-Color Palette (Color Names):", palette)
