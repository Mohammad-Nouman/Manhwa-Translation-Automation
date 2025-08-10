import os
import re
import textwrap
from typing import Dict
from PIL import Image, ImageDraw, ImageFont




def extract_page_number(aria_label: str) -> int:
    """
    Extract the last number from the aria-label string.
    Example: "Page 1 of 10" -> returns 10
    """
    if not aria_label:
        return 0

    # Find all numbers in the aria-label
    numbers = re.findall(r'\d+', aria_label)
    if numbers:
        return int(numbers[-1])  # Take the last number
    return 0


def load_translations(file_path: str) -> Dict[str, str]:
    """
    Load translations from a text file.

    Expected file format:
        filename.jpg:
        Translated text...

    Args:
        file_path (str): Path to the translation file.

    Returns:
        Dict[str, str]: A mapping of image filenames to translations.
    """
    translations = {}
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.read().split("\n")
        current_file = None

        for line in lines:
            if line.endswith(":"):
                current_file = line[:-1].strip()
            elif current_file and line.strip():
                translations[current_file] = line.strip()
                current_file = None

    return translations


def write_translations_on_images(
    translation_file: str,
    image_folder: str,
    output_folder: str,
    font_path: str,
    font_size: int,
    words_per_line: int
) -> None:
    """
    Overlay translations from a file onto images and save them to the output folder.

    Args:
        translation_file (str): Path to the translation file.
        image_folder (str): Directory containing original images.
        output_folder (str): Directory to save images with translations applied.
        font_path (str): Path to a .ttf or .otf font file.
        font_size (int): Font size for text overlay.
        words_per_line (int): Max words per line before wrapping.
    """
    translations = load_translations(translation_file)
    os.makedirs(output_folder, exist_ok=True)

    for img_file in sorted(os.listdir(image_folder), key=extract_page_number):
        if not img_file.lower().endswith(".jpg"):
            continue

        img_path = os.path.join(image_folder, img_file)
        output_path = os.path.join(output_folder, img_file)

        # Open and prepare image
        image = Image.open(img_path).convert("RGB")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_path, font_size)

        text = translations.get(img_file, "")
        if not text:
            print(f"⚠ No translation for {img_file}, skipping text overlay.")
            image.save(output_path)
            continue

        # Wrap text by words_per_line
        wrapped_text = textwrap.fill(text, width=words_per_line)

        # Positioning
        margin = 50
        text_x = margin
        text_y = image.height - font_size * (wrapped_text.count("\n") + 3)

        # Draw background rectangle
        rect_height = font_size * (wrapped_text.count("\n") + 2)
        draw.rectangle(
            [(0, text_y - 10), (image.width, text_y + rect_height)],
            fill=(0, 0, 0, 180),
        )

        # Draw text
        draw.text((text_x, text_y), wrapped_text, font=font, fill=(255, 255, 255))
        image.save(output_path)

        print(f"✅ Saved: {output_path}")
