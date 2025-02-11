import random
import re
import os
from datetime import datetime, timedelta
from .weather_utils import generate_weather_description
from .color_data import COLORS, color_families
# Palette generation module imports:
from .make_palette_analogous import generate_analogous_palette_4, generate_analogous_palette_5
from .make_palette_art_house import generate_art_house_palette_4, generate_art_house_palette_5
from .make_palette_chaotic import generate_chaotic_palette
from .make_palette_complementary import generate_complementary_palette, generate_complementary_palette_5
from .make_palette_double_complementary import generate_double_complementary_palette_4, generate_double_complementary_palette_5
from .make_palette_modified_compound import generate_modified_compound_palette_five, generate_modified_compound_palette_four_from_five
from .make_palette_split_complementary import generate_split_complementary_palette_4, generate_split_complementary_palette_5
from .make_palette_triadic import generate_four_color_palette, generate_triadic_palette_5

class EbuPromptHelperRandomColorPalette:
    """
    EBU Random Color Palette Generator Node
    Inputs:
      - include_analogous_palettes (BOOLEAN): Include analogous palettes (default True)
      - include_art_house_palettes (BOOLEAN): Include art house palettes (default True)
      - include_chaotic_palettes (BOOLEAN): Include chaotic palettes (default True)
      - include_complementary_palettes (BOOLEAN): Include complementary palettes (default True)
      - include_compound_palettes (BOOLEAN): Include compound palettes (default True)
      - include_split_complementary_palettes (BOOLEAN): Include split complementary palettes (default True)
      - include_tetradic_palettes (BOOLEAN): Include tetradic palettes (default True)
      - include_triadic_palettes (BOOLEAN): Include triadic palettes (default True)
      - palette_size (STRING): Drop‑down selection for palette size. Options:
           "3 colors", "4 colors", or "5 colors".
           (If "3 colors" is selected, a standard 4‑color palette is generated and its first 3 colors are returned.)
      - prefer_color_family (STRING): Drop‑down for a preferred color family.
           Options: "None", "Reds", "Pinks", "Oranges", "Yellows", "Greens", "Blues", "Purples",
           "Browns", "Greys", "Neutrals", "Metallics", "Pastels", "Peaches", "Warm Colors", "Cool Colors".
           (If not "None", the palette is regenerated up to 50 times until the condition is met.)
      - avoid_color_family (STRING): Drop‑down for a color family to avoid.
           Options: "None", "Reds", "Pinks", "Oranges", "Yellows", "Greens", "Blues", "Purples",
           "Browns", "Greys", "Neutrals", "Metallics", "Pastels", "Peaches", "Warm Colors", "Cool Colors".
           (If not "None", the palette is regenerated up to 50 times until the condition is met.)
      - seed (INT): Seed for random generation (0 means non‑deterministic).
    Returns:
      - palette (STRING): A comma‑separated list of color names (always at least 3), in lower-case.
      - color1 (STRING): The first color in the palette (lower-case).
      - color2 (STRING): The second color in the palette (lower-case).
      - color3 (STRING): The third color in the palette (lower-case).
      - color4 (STRING): The fourth color if available, or "" if not.
      - color5 (STRING): The fifth color if available, or "" if not.
      - palette_type (STRING): The chosen palette type.
      - hex_values (STRING): A comma‑separated list of hex values corresponding to each color.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "include_analogous_palettes": ("BOOLEAN", {"default": True}),
                "include_art_house_palettes": ("BOOLEAN", {"default": True}),
                "include_chaotic_palettes": ("BOOLEAN", {"default": True}),
                "include_complementary_palettes": ("BOOLEAN", {"default": True}),
                "include_compound_palettes": ("BOOLEAN", {"default": True}),
                "include_split_complementary_palettes": ("BOOLEAN", {"default": True}),
                "include_tetradic_palettes": ("BOOLEAN", {"default": True}),
                "include_triadic_palettes": ("BOOLEAN", {"default": True}),
                "palette_size": (["3 colors", "4 colors", "5 colors"], {"default": "4 colors"}),
                "prefer_color_family": (
                    ["None", "Reds", "Pinks", "Oranges", "Yellows", "Greens", "Blues", "Purples",
                     "Browns", "Greys", "Neutrals", "Metallics", "Pastels", "Peaches", "Warm Colors", "Cool Colors"],
                    {"default": "None"}
                ),
                "avoid_color_family": (
                    ["None", "Reds", "Pinks", "Oranges", "Yellows", "Greens", "Blues", "Purples",
                     "Browns", "Greys", "Neutrals", "Metallics", "Pastels", "Peaches", "Warm Colors", "Cool Colors"],
                    {"default": "None"}
                ),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("palette_string", "color1", "color2", "color3", "color4", "color5", "palette_type", "hex_values")
    FUNCTION = "generate_palette"
    CATEGORY = "Prompts"

    def generate_palette(
            self,
            include_analogous_palettes,
            include_art_house_palettes,
            include_chaotic_palettes,
            include_complementary_palettes,
            include_compound_palettes,
            include_split_complementary_palettes,
            include_tetradic_palettes,
            include_triadic_palettes,
            palette_size,
            prefer_color_family,
            avoid_color_family,
            seed):

        # Set the random seed.
        random.seed(seed)

        # If the same color family is specified for both prefer and avoid, cancel them out.
        if (prefer_color_family != "None" and
            avoid_color_family != "None" and
            prefer_color_family == avoid_color_family):
            print("Warning: The same color family was selected for both prefer and avoid. Cancelling these conditions.")
            prefer_color_family = "None"
            avoid_color_family = "None"

        # Build a list of enabled palette types.
        enabled_types = []
        if include_analogous_palettes:
            enabled_types.append("analogous")
        if include_art_house_palettes:
            enabled_types.append("art house")
        if include_chaotic_palettes:
            enabled_types.append("chaotic")
        if include_complementary_palettes:
            enabled_types.append("complementary")
        if include_compound_palettes:
            enabled_types.append("compound")
        if include_split_complementary_palettes:
            enabled_types.append("split complementary")
        if include_tetradic_palettes:
            enabled_types.append("tetradic")
        if include_triadic_palettes:
            enabled_types.append("triadic")

        # If none are enabled, log a warning and default to all palette types.
        if not enabled_types:
            print("Warning: No palette types were enabled. Defaulting to all palette types.")
            enabled_types = [
                "analogous", "art house", "chaotic", "complementary",
                "compound", "split complementary", "tetradic", "triadic"
            ]

        # Determine target palette size (numeric).
        if palette_size == "3 colors":
            target_size = 3
        elif palette_size == "4 colors":
            target_size = 4
        elif palette_size == "5 colors":
            target_size = 5
        else:
            raise Exception("Invalid palette size: " + palette_size)

        max_attempts = 50
        chosen_palette = None
        chosen_type = None  # To record which palette type was chosen.

        for attempt in range(max_attempts):
            chosen_type = random.choice(enabled_types)
            if chosen_type == "analogous":
                if target_size == 5:
                    palette = generate_analogous_palette_5()
                else:
                    palette = generate_analogous_palette_4()
                    if target_size == 3:
                        palette = palette[:3]
            elif chosen_type == "art house":
                if target_size == 5:
                    palette = generate_art_house_palette_5()
                else:
                    palette = generate_art_house_palette_4()
                    if target_size == 3:
                        palette = palette[:3]
            elif chosen_type == "chaotic":
                if target_size == 5:
                    palette = generate_chaotic_palette(num_colors=5)
                elif target_size == 4:
                    palette = generate_chaotic_palette(num_colors=4)
                elif target_size == 3:
                    palette = generate_chaotic_palette(num_colors=4)[:3]
            elif chosen_type == "complementary":
                if target_size == 5:
                    palette = generate_complementary_palette_5()
                else:
                    palette = generate_complementary_palette()
                    if target_size == 3:
                        palette = palette[:3]
            elif chosen_type == "compound":
                if target_size == 5:
                    palette = generate_modified_compound_palette_five()
                else:
                    palette = generate_modified_compound_palette_four_from_five()
                    if target_size == 3:
                        palette = palette[:3]
            elif chosen_type == "split complementary":
                if target_size == 5:
                    palette = generate_split_complementary_palette_5()
                else:
                    palette = generate_split_complementary_palette_4()
                    if target_size == 3:
                        palette = palette[:3]
            elif chosen_type == "tetradic":
                if target_size == 5:
                    palette = generate_double_complementary_palette_5()
                else:
                    palette = generate_double_complementary_palette_4()
                    if target_size == 3:
                        palette = palette[:3]
            elif chosen_type == "triadic":
                if target_size == 5:
                    palette = generate_triadic_palette_5()
                else:
                    palette = generate_four_color_palette()
                    if target_size == 3:
                        palette = palette[:3]
            else:
                raise Exception("Unknown palette type chosen: " + chosen_type)

            # --- Check the "prefer" condition ---
            condition_preferred = True
            if prefer_color_family != "None":
                if prefer_color_family in ["Warm Colors", "Cool Colors"]:
                    warm_list = color_families.get("Warm Colors", [])
                    cool_list = color_families.get("Cool Colors", [])
                    warm_count = sum(1 for color in palette if color in warm_list)
                    cool_count = sum(1 for color in palette if color in cool_list)
                    if prefer_color_family == "Warm Colors":
                        condition_preferred = (warm_count >= cool_count + 1)
                    else:
                        condition_preferred = (cool_count >= warm_count + 1)
                else:
                    preferred_list = color_families.get(prefer_color_family, [])
                    condition_preferred = any(color in preferred_list for color in palette)

            # --- Check the "avoid" condition ---
            condition_avoid = True
            if avoid_color_family != "None":
                if avoid_color_family in ["Warm Colors", "Cool Colors"]:
                    warm_list = color_families.get("Warm Colors", [])
                    cool_list = color_families.get("Cool Colors", [])
                    warm_count = sum(1 for color in palette if color in warm_list)
                    cool_count = sum(1 for color in palette if color in cool_list)
                    if avoid_color_family == "Warm Colors":
                        condition_avoid = (warm_count <= cool_count - 1)
                    else:
                        condition_avoid = (cool_count <= warm_count - 1)
                else:
                    avoid_list = color_families.get(avoid_color_family, [])
                    condition_avoid = not any(color in avoid_list for color in palette)

            if condition_preferred and condition_avoid:
                chosen_palette = palette
                break

        if chosen_palette is None:
            print(f"Warning: Attempted {max_attempts} times to meet color preferences but wasn't able to.")
            chosen_palette = palette

        display_palette = [color.lower() for color in chosen_palette]
        palette_str = ", ".join(display_palette)
        padded_display = display_palette.copy()
        while len(padded_display) < 5:
            padded_display.append("")
        color1, color2, color3, color4, color5 = padded_display[:5]
        hex_list = [COLORS.get(color, "") for color in chosen_palette]
        hex_values_str = ", ".join(hex_list)

        return (palette_str, color1, color2, color3, color4, color5, chosen_type, hex_values_str)

class EbuPromptHelperReplace:
    """
    EBU Prompt Helper Replace Node

    This node replaces occurrences of one or more target words within an input prompt with a specified replacement string.
    The target words should be provided as a single string, where multiple words are separated by the '|' character.
    For example, if the `word_to_replace` input is "person|man|woman", then any occurrence of "person", "man", or "woman"
    in the prompt will be replaced with the value provided in `replace_with`.

    Inputs:
      - prompt_text (STRING): A multiline string representing the input prompt.
      - word_to_replace (STRING): A single-line string containing one or more words separated by '|'.
      - replace_with (STRING): A multiline string that will replace each occurrence of the target words.
      - case_sensitive (BOOLEAN): A toggle to control if the replacement is case‑sensitive (default True).
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt_text": ("STRING", {"multiline": True, "default": ""}),
                "word_to_replace": ("STRING", {"multiline": False, "default": ""}),
                "replace_with": ("STRING", {"multiline": True, "default": ""}),
                "case_sensitive": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("updated_prompt_text",)
    FUNCTION = "replace_text"
    CATEGORY = "Example"

    def replace_text(self, prompt_text, word_to_replace, replace_with, case_sensitive):
        if not word_to_replace.strip():
            return (prompt_text,)
        words = word_to_replace.split("|")
        revised = prompt_text
        if case_sensitive:
            for word in words:
                revised = revised.replace(word, replace_with)
        else:
            import re
            for word in words:
                pattern = re.compile(re.escape(word), re.IGNORECASE)
                revised = pattern.sub(replace_with, revised)
        return (revised,)

class EbuPromptHelperRandomize:
    """
    EBU PromptHelper Randomize Node

    This node takes an input prompt and replaces occurrences of a specified target substring
    (word_to_replace) with a randomly selected option from a provided string of options.
    The options string is split based on the chosen delimiter, which can be newlines, commas, or semi‑colons.
    The seed input controls the random selection, allowing for deterministic output if desired.

    Inputs:
      - prompt_text (STRING): A multiline string representing the input prompt.
      - word_to_replace (STRING): A single-line string indicating the substring to replace.
      - replacement_options (STRING): A string containing replacement options.
      - seed (INT): Ensures that node runs every time
      - case_sensitive (BOOLEAN): A toggle to control if the replacement is case‑sensitive (default True).
      - delimit_options_with (STRING): Dropdown with options ["newlines", "commas", "semi-colons"]
          that determines how to split the options string.

    Returns:
      - updated_prompt_text (STRING): The prompt after replacement.
      - word_selected (STRING): The randomly selected replacement option.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt_text": ("STRING", {"multiline": True, "default": ""}),
                "word_to_replace": ("STRING", {"multiline": False, "default": ""}),
                "replacement_options": ("STRING", {"multiline": True, "default": ""}),
                "seed": ("INT", {"default": 0, "step": 1, "display": "number"}),
                "case_sensitive": ("BOOLEAN", {"default": True}),
                "delimit_options_with": (["newlines", "commas", "semi-colons"], {"default": "newlines"})
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("updated_prompt_text", "word_selected")
    FUNCTION = "randomize_text"
    CATEGORY = "Prompts"

    def randomize_text(self, prompt_text, word_to_replace, replacement_options, seed, case_sensitive, delimit_options_with):
        random.seed(seed)

        # Split the options string based on the selected delimiter.
        if delimit_options_with == "newlines":
            options = [opt.strip() for opt in replacement_options.splitlines() if opt.strip()]
        elif delimit_options_with == "commas":
            options = [opt.strip() for opt in replacement_options.split(',') if opt.strip()]
        elif delimit_options_with == "semi-colons":
            options = [opt.strip() for opt in replacement_options.split(';') if opt.strip()]
        else:
            options = [opt.strip() for opt in replacement_options.splitlines() if opt.strip()]

        if not options:
            return (prompt_text, "")

        selected = random.choice(options)

        if case_sensitive:
            new_prompt = prompt_text.replace(word_to_replace, selected)
        else:
            import re
            pattern = re.compile(re.escape(word_to_replace), re.IGNORECASE)
            new_prompt = pattern.sub(selected, prompt_text)

        return (new_prompt, selected)

class EbuPromptHelperCombineTwoStrings:
    """
    EBU PromptHelper Combine Two Strings Node

    This node takes two input strings and combines them into one string using a provided join string.
    Only non-empty input strings are included in the final result. For example, if one of the inputs is
    empty, only the non-empty string is returned.

    Inputs:
      - str1 (STRING): The first string to combine. (Multiline supported.)
      - str2 (STRING): The second string to combine. (Multiline supported.)
      - join_str (STRING): The string used to join the two input strings. Defaults to "\n\n".

    Returns:
      - combined (STRING): The resulting combined string.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "str1": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "str2": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "join_str": ("STRING", {
                    "multiline": True,
                    "default": "\n\n"
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("combined",)

    FUNCTION = "combine_two_strings"

    CATEGORY = "Prompts"

    def combine_two_strings(self, str1, str2, join_str):
        strs = []
        if str1:
            strs.append(str1)
        if str2:
            strs.append(str2)
        combined = join_str.join(strs)
        return (combined,)

class EbuPromptHelperListSampler:
    """
    EBU PromptHelper List Sampler Node

    This node takes a multi-line string (representing a list) as input, processes each line
    by removing any leading numbers (e.g., "1. ", "23. ") and trimming whitespace, and then
    randomly shuffles the remaining non-empty lines. It returns a sample containing a specified
    number of lines (or all lines if there are fewer than requested). If the toggle is enabled,
    the sampled list will be numbered starting at 1.

    Inputs:
      - list (STRING): A multi-line string containing the list items. Each line may optionally
        start with a number and a dot.
      - seed (INT): A seed for the random number generator. Use 0 for non-deterministic output.
      - number_of_elements (INT, optional): The maximum number of list elements to sample. Defaults to 10.
      - number_sampled_list (BOOLEAN, optional): If True, the sampled list will be numbered (default False).

    Returns:
      - (STRING): A newline-separated string of the sampled list items.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "list": ("STRING", {"multiline": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
            "optional": {
                "number_of_elements": ("INT", {"default": 10, "min": 1, "max": 1000}),
                "number_sampled_list": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "sample_list"
    CATEGORY = "utils"

    def sample_list(self, list, seed, number_of_elements=10, number_sampled_list=False):
        # Split the input string into lines.
        lines = list.split('\n')

        # Process lines: remove leading numbers and ignore empty or whitespace-only lines.
        processed_lines = []
        for line in lines:
            # Remove leading numbers followed by a dot (e.g., "1. ", "23. ").
            processed_line = re.sub(r'^\d+\.\s*', '', line)
            processed_line = processed_line.strip()
            if processed_line:  # Only add non-empty lines.
                processed_lines.append(processed_line)

        # Set the random seed.
        random.seed(seed)

        # Shuffle the processed lines.
        random.shuffle(processed_lines)

        # Select the specified number of elements, or all available if there are fewer.
        selected_lines = processed_lines[:min(number_of_elements, len(processed_lines))]

        # If numbering is enabled, number each line starting at 1.
        if number_sampled_list:
            numbered_lines = []
            for idx, line in enumerate(selected_lines, start=1):
                numbered_lines.append(f"{idx}. {line}")
            selected_lines = numbered_lines

        # Join the selected lines into a single string separated by newlines.
        output = '\n'.join(selected_lines)

        return (output,)

class EbuPromptHelperLoadFileAsString:
    """
    EBU PromptHelper Load File as String Node

    This node loads the contents of a file as a string. Provide the directory and file name, and the node
    will attempt to read the file using UTF-8 encoding. If an error occurs (e.g., if the file is not found),
    the node will print an error message and return an empty string.

    Inputs:
      - directory (STRING): The directory path where the file is located.
      - file_name (STRING): The name of the file to load.

    Returns:
      - (STRING): The content of the file as a string, or an empty string if an error occurred.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory": ("STRING", {"default": ""}),
                "file_name": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "load_file"
    CATEGORY = "File Operations"

    def load_file(self, directory, file_name):
        full_path = os.path.join(directory, file_name)
        try:
            with open(full_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return (content,)
        except Exception as e:
            print(f"Error reading file: {e}")
            return ("",)

class EbuPromptHelperCurrentDateTime:
    """
    EBU PromptHelper Current DateTime Node

    This node returns the current datetime (at the moment of execution) in several formats:

      - date: "February 10, 2025"
      - time: "1:15pm"
      - datetime: "2025-02-10 1:15:33pm"
      - datetime_for_filename: "2025-02-10_13-15-33"

    No input parameters are required.
    """
    @classmethod
    def INPUT_TYPES(cls):
        # No inputs required.
        return {"required": {}}

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("date", "time", "datetime", "datetime_for_filename")
    FUNCTION = "generate_datetime"
    CATEGORY = "Utility"

    def generate_datetime(self):
        # Get the current datetime.
        dt = datetime.now()

        # Format the date as "February 10, 2025" (with the day inserted without a leading zero).
        date_str = dt.strftime("%B {day}, %Y").format(day=dt.day)

        # Format the time as "1:15pm" (12-hour format with any leading zero removed and lowercase am/pm).
        time_str = dt.strftime("%I:%M%p").lstrip("0").lower()

        # Format the full datetime as "2025-02-10 1:15:33pm".
        datetime_str = dt.strftime("%Y-%m-%d ") + dt.strftime("%I:%M:%S%p").lstrip("0").lower()

        # Format the datetime for filenames as "2025-02-10_13-15-33".
        datetime_filename_str = dt.strftime("%Y-%m-%d_%H-%M-%S")

        return (date_str, time_str, datetime_str, datetime_filename_str)

class EbuPromptHelperConsumeListItem:
    """
    EBU PromptHelper Consume List Item Node

    This node takes an optional prompt, a target substring to replace, and a list of options provided
    as a newline-separated string. It randomly selects one option from the list (using the provided seed
    for reproducibility), removes that option from the list, and replaces all occurrences of the target
    substring in the prompt with the selected option. The revised list (with the selected option removed)
    is also returned.

    Inputs:
      - word_to_replace (STRING): The substring in the prompt to be replaced.
      - list (STRING): A newline-separated list of options.
      - seed (INT): A seed for the random number generator (0 means non-deterministic).
      - prompt_text (STRING, optional): A multiline string representing the input prompt. Defaults to an empty string.

    Returns:
      - updated_prompt_text (STRING): The prompt with the target substring replaced by the selected option.
      - word_selected (STRING): The randomly selected option from the list.
      - revised_list (STRING): The remaining options (after the selected one is removed) joined by a single newline
        between each option, with no extra newline at the beginning.
    """
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "word_to_replace": ("STRING", {}),
                "list": ("STRING", {"multiline": True, "default": ""}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
            "optional": {
                "prompt_text": ("STRING", {"multiline": True, "default": ""})
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("updated_prompt_text", "word_selected", "revised_list")
    FUNCTION = "consume_list_item"
    CATEGORY = "utils"

    def consume_list_item(self, word_to_replace, list, seed, prompt_text=""):
        # Split the input string into a list of options using newlines.
        options = [opt.strip() for opt in list.splitlines() if opt.strip()]

        # Set the random seed.
        random.seed(seed)

        if options:
            # Randomly select an option.
            word_selected = random.choice(options)

            # Remove the selected option from the list.
            options.remove(word_selected)

            # Join the remaining options with a single newline between them.
            revised_list = '\n'.join(options)
            # Ensure there is no extra newline at the beginning.
            revised_list = revised_list.lstrip('\n')

            # Replace all occurrences of the target substring in the prompt with the selected option.
            updated_prompt_text = prompt_text.replace(word_to_replace, word_selected)
            return (updated_prompt_text, word_selected, revised_list)
        else:
            # If no options are provided, return the prompt (or empty string) and empty values for the other outputs.
            return (prompt_text, "", "")

class EbuPromptHelperSeasonWeatherTimeOfDay:
    """
    EBU PromptHelper Season Weather Time-Of-Day Node

    This node generates a random abstract description of a datetime within a specified year and time range,
    and then produces a weather description based on that abstract datetime. The abstract datetime is
    expressed in terms of a time of day and a seasonal descriptor (for example, "early morning during early winter of 2020").

    Two new parameters allow you to skew the randomness:
      - year_skew: How to bias the year selection.
      - time_of_day_skew: How to bias the time selection.

    The available options for each are:
      - "no skew" (default): Uniform random selection.
      - "earlier of two": Generate two random values and pick the earlier (lower) one.
      - "later of two": Generate two random values and pick the later (higher) one.
      - "middle of three": Generate three random values and pick the median.

    Inputs:
      - year_from (INT): The earliest year for the random date (e.g., 1980).
      - year_to (INT): The latest year for the random date (e.g., 2022).
      - time_from (STRING): The start of the time range (e.g., "6:00am").
      - time_to (STRING): The end of the time range (e.g., "7:00pm").
      - seed (INT): to ensure it runs every time
      - year_skew (STRING): Dropdown with options ["no skew", "earlier of two", "later of two", "middle of three"].
      - time_of_day_skew (STRING): Dropdown with the same options as above.

    Returns:
      - when (STRING): An abstract datetime description (e.g., "early morning during early winter of 2020").
      - when_no_year (STRING): The abstract datetime description with the year removed (e.g., "early morning during early winter").
      - weather (STRING): A weather description (e.g., "cool and snowy") selected based on the abstract datetime.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "year_from": ("INT", {"default": 1980, "step": 1, "display": "number"}),
                "year_to": ("INT", {"default": 2025, "step": 1, "display": "number"}),
                "time_from": ("STRING", {"multiline": False, "default": "6:00am"}),
                "time_to": ("STRING", {"multiline": False, "default": "7:00pm"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "year_skew": (["no skew", "earlier of two", "later of two", "middle of three"], {"default": "no skew"}),
                "time_of_day_skew": (["no skew", "earlier of two", "later of two", "middle of three"], {"default": "no skew"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("when", "when_no_year", "weather")
    FUNCTION = "generate_info"
    CATEGORY = "Example"

    def generate_info(self, year_from, year_to, time_from, time_to, seed, year_skew, time_of_day_skew):
        random.seed(seed)
        when = self.generate_random_datetime(year_from, year_to, time_from, time_to, year_skew, time_of_day_skew)
        weather = generate_weather_description(when)  # Use external weather function
        # Remove the " of [year]" part from the abstract datetime.
        when_no_year = when.rsplit(" of ", 1)[0]
        return (when, when_no_year, weather)

    def generate_random_datetime(self, year_from, year_to, time_from, time_to, year_skew, time_of_day_skew):
        # Helper: Convert a time string (e.g., "6:00am") to a datetime object.
        def time_str_to_dt(time_str):
            return datetime.strptime(time_str, '%I:%M%p')

        # Helper: Generate a skewed random integer between min_val and max_val (inclusive).
        def generate_skewed_random(min_val, max_val, skew):
            if skew == "no skew":
                return random.randint(min_val, max_val)
            elif skew == "earlier of two":
                return min(random.randint(min_val, max_val), random.randint(min_val, max_val))
            elif skew == "later of two":
                return max(random.randint(min_val, max_val), random.randint(min_val, max_val))
            elif skew == "middle of three":
                vals = [random.randint(min_val, max_val) for _ in range(3)]
                return sorted(vals)[1]
            else:
                return random.randint(min_val, max_val)

        # Helper: Generate a random date between start_year and end_year using the specified skew.
        def random_date(start_year, end_year, skew):
            start_date = datetime(start_year, 1, 1)
            end_date = datetime(end_year + 1, 1, 1)
            delta_days = (end_date - start_date).days
            day_offset = generate_skewed_random(0, delta_days - 1, skew)
            return start_date + timedelta(days=day_offset)

        # Helper: Determine the abstract time of day based on the hour.
        def get_time_of_day(hour):
            if 5 <= hour < 8:
                return "early morning"
            elif 8 <= hour < 10:
                return "morning"
            elif 10 <= hour < 12:
                return "late morning"
            elif 12 <= hour < 15:
                return "early afternoon"
            elif 15 <= hour < 18:
                return "late afternoon"
            elif 18 <= hour < 20:
                return "early evening"
            elif 20 <= hour < 22:
                return "evening"
            elif 22 <= hour or hour < 5:
                return "night"
            else:
                return "unknown time"

        # Helper: Determine the seasonal descriptor based on the month.
        def get_season_part(month):
            if month in [12, 1, 2]:
                season = "winter"
            elif month in [3, 4, 5]:
                season = "spring"
            elif month in [6, 7, 8]:
                season = "summer"
            elif month in [9, 10, 11]:
                season = "fall"
            else:
                season = "unknown season"
            if month in [12, 1, 2]:
                return f"early {season}" if month == 12 else f"late {season}"
            elif month in [3, 4, 5]:
                if month == 3:
                    return f"early {season}"
                elif month == 5:
                    return f"late {season}"
                else:
                    return f"middle of the {season}"
            elif month in [6, 7, 8]:
                if month == 6:
                    return f"early {season}"
                elif month == 8:
                    return f"late {season}"
                else:
                    return f"middle of the {season}"
            elif month in [9, 10, 11]:
                if month == 9:
                    return f"early {season}"
                elif month == 11:
                    return f"late {season}"
                else:
                    return f"middle of the {season}"

        # Convert time strings to datetime objects.
        time_from_dt = time_str_to_dt(time_from)
        time_to_dt = time_str_to_dt(time_to)
        if time_from_dt > time_to_dt:
            raise ValueError("time_from must be before time_to")

        # Generate a random date using the year skew.
        random_date_obj = random_date(year_from, year_to, year_skew)

        # Calculate the total seconds in the time window and generate a skewed random second offset.
        total_seconds = int((time_to_dt - time_from_dt).total_seconds())
        sec_offset = generate_skewed_random(0, total_seconds, time_of_day_skew)
        random_time = time_from_dt + timedelta(seconds=sec_offset)

        # Determine the descriptive strings.
        tod_str = get_time_of_day(random_time.hour)
        season_str = get_season_part(random_date_obj.month)

        return f"{tod_str} during {season_str} of {random_date_obj.year}"

# Node registration mappings.
NODE_CLASS_MAPPINGS = {
    "EbuPromptHelperCombineTwoStrings": EbuPromptHelperCombineTwoStrings,
    "EbuPromptHelperConsumeListItem": EbuPromptHelperConsumeListItem,
    "EbuPromptHelperCurrentDateTime": EbuPromptHelperCurrentDateTime,
    "EbuPromptHelperListSampler": EbuPromptHelperListSampler,
    "EbuPromptHelperLoadFileAsString": EbuPromptHelperLoadFileAsString,
    "EbuPromptHelperRandomColorPalette": EbuPromptHelperRandomColorPalette,
    "EbuPromptHelperRandomize": EbuPromptHelperRandomize,
    "EbuPromptHelperReplace": EbuPromptHelperReplace,
    "EbuPromptHelperSeasonWeatherTimeOfDay": EbuPromptHelperSeasonWeatherTimeOfDay,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "EbuPromptHelperCombineTwoStrings": "EBU PromptHelper Combine Two Strings",
    "EbuPromptHelperConsumeListItem": "EBU PromptHelper Consume List Item",
    "EbuPromptHelperCurrentDateTime": "EBU PromptHelper Current DateTime",
    "EbuPromptHelperListSampler": "EBU PromptHelper List Sampler",
    "EbuPromptHelperLoadFileAsString": "EBU PromptHelper Load File as String",
    "EbuPromptHelperRandomColorPalette": "EBU PromptHelper Color Palette",
    "EbuPromptHelperRandomize": "EBU PromptHelper Randomize",
    "EbuPromptHelperReplace": "EBU PromptHelper Replace",
    "EbuPromptHelperSeasonWeatherTimeOfDay": "EBU PromptHelper Season Weather Time-Of-Day",
}
