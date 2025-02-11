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
# Analogous Palette Functions
# ----------------------------
def analogous_palette(base_hex, offset_degrees=15):
   """Returns three analogous colors: base, base+offset, and base-offset."""
   return [base_hex,
           shift_hue(base_hex, offset_degrees),
           shift_hue(base_hex, -offset_degrees)]

def generate_random_base_color():
   families = ['Reds', 'Pinks', 'Oranges', 'Yellows', 'Greens', 'Blues', 'Purples']
   candidate_colors = []
   for fam in families:
       candidate_colors.extend(color_families.get(fam, []))
   random_color_name = random.choice(candidate_colors)
   return random_color_name, COLORS[random_color_name]

# ----------------------------
# Palette Generation: 4 vs. 5 Colors
# ----------------------------
def generate_analogous_palette_4():
   """4-color version: 3 analogous colors + 1 Broad Neutral."""
   broad_neutrals = color_families.get("Broad Neutrals", [])
   max_attempts = 50

   for _ in range(max_attempts):
       _, base_hex = generate_random_base_color()
       analog_hexes = analogous_palette(base_hex, offset_degrees=15)
       analog_names = [find_closest_color_name(h, COLORS) for h in analog_hexes]
       fourth = random.choice(broad_neutrals)
       palette = analog_names + [fourth]
       if len(set(palette)) == 4:
           return palette

   # Fallback: If we can't get 4 unique colors after max attempts,
   # try with a larger offset
   _, base_hex = generate_random_base_color()
   analog_hexes = analogous_palette(base_hex, offset_degrees=30)
   analog_names = [find_closest_color_name(h, COLORS) for h in analog_hexes]

   # Try to find a unique neutral color
   for neutral in broad_neutrals:
       test_palette = analog_names + [neutral]
       if len(set(test_palette)) == 4:
           return test_palette

   # Ultimate fallback - use any unique color as the fourth
   all_colors = list(COLORS.keys())
   for color in all_colors:
       if color not in analog_names:
           return analog_names + [color]

   # If everything fails, duplicate the last color
   return analog_names + [analog_names[-1]]

def generate_analogous_palette_5():
   """
   5-color version: 3 original analogous colors +
   one extra analogous variant (e.g. base+30°) +
   one Broad Neutral.
   """
   broad_neutrals = color_families.get("Broad Neutrals", [])
   max_attempts = 50

   for _ in range(max_attempts):
       _, base_hex = generate_random_base_color()
       # Original analogous (3 colors)
       analog_hexes = analogous_palette(base_hex, offset_degrees=15)
       analog_names = [find_closest_color_name(h, COLORS) for h in analog_hexes]
       # Extra analogous: base shifted by +30°
       extra = find_closest_color_name(shift_hue(base_hex, 30), COLORS)
       fourth = random.choice(broad_neutrals)
       palette = analog_names + [extra, fourth]
       if len(set(palette)) == 5:
           return palette

   # Fallback: Try with different offset values
   for offset in [20, 25, 30]:
       _, base_hex = generate_random_base_color()
       analog_hexes = analogous_palette(base_hex, offset_degrees=offset)
       analog_names = [find_closest_color_name(h, COLORS) for h in analog_hexes]
       extra = find_closest_color_name(shift_hue(base_hex, offset*2), COLORS)

       # Try each neutral color
       current_palette = analog_names + [extra]
       if len(set(current_palette)) == 4:  # Make sure first 4 are unique
           for neutral in broad_neutrals:
               test_palette = current_palette + [neutral]
               if len(set(test_palette)) == 5:
                   return test_palette

   # Ultimate fallback - start with analogous colors and add unique colors
   _, base_hex = generate_random_base_color()
   analog_hexes = analogous_palette(base_hex, offset_degrees=30)
   current_palette = [find_closest_color_name(h, COLORS) for h in analog_hexes]

   # Try to add two more unique colors
   all_colors = list(COLORS.keys())
   while len(current_palette) < 5 and all_colors:
       candidate = random.choice(all_colors)
       if candidate not in current_palette:
           current_palette.append(candidate)
       all_colors.remove(candidate)

   # If we still don't have 5 colors, pad with duplicates
   while len(current_palette) < 5:
       current_palette.append(current_palette[-1])

   return current_palette

if __name__ == '__main__':
   five_flag = '-5' in sys.argv
   if five_flag:
       palette = generate_analogous_palette_5()
   else:
       palette = generate_analogous_palette_4()
   print("Analogous Palette with Broad Neutral Twist (Color Names):", palette)