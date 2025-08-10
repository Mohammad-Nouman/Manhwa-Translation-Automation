# ocr_translator.py

import os
import base64
import requests
from typing import List



def encode_image(image_path: str) -> str:
    """
    Encode an image to a Base64 string.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Base64-encoded string of the image content.
    """
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def ai_translate(image_path: str, api_key: str, model: str) -> str:
    """
    Perform OCR and translation on a given image using the OpenRouter API.

    Args:
        image_path (str): Path to the image file.
        api_key (str): OpenRouter API key.
        model (str): AI model name.

    Returns:
        str: Translated text or an error message.
    """
    img_b64 = encode_image(image_path)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Read all Korean text visible in this manhwa and try "
                            "to relate the story, then translate it to English. "
                            "Only provide the translated text."
                        ),
                    },
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{img_b64}"},
                ],
            }
        ],
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60
    )

    if response.status_code == 200:
        try:
            return response.json()["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            return "ERROR: Bad response format"
    return f"ERROR: {response.status_code} {response.text}"


def process_all_images(
    image_folder: str,
    translation_file: str,
    api_key: str,
    model: str
) -> None:
    """
    Process all images in a folder: OCR + translate + save to file.

    Args:
        image_folder (str): Directory containing images to process.
        translation_file (str): File path to save all translations.
        api_key (str): OpenRouter API key.
        model (str): AI model name.
    """
    translations: List[str] = []

    for img_file in sorted(os.listdir(image_folder), key=extract_page_number):
        if img_file.lower().endswith(".jpg"):
            img_path = os.path.join(image_folder, img_file)
            print(f"Processing {img_file}...")
            translation = ai_translate(img_path, api_key, model)
            translations.append(f"{img_file}:\n{translation}\n")
            print(f"✅ Done: {translation[:100]}...")

    with open(translation_file, "w", encoding="utf-8") as file:
        file.write("\n".join(translations))

    print(f"All translations saved to {translation_file}")
