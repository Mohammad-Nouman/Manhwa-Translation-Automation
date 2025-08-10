"""
config.py
Centralized configuration for the manhwa translation pipeline.
Modify the values here to change pipeline behavior without editing core modules.
"""

# ========= SCRAPER SETTINGS =========
SCRAPER_CONFIG = {
    "output_folder": "manhwa_images"  # Where raw images from scraper will be stored
}

# ========= OCR & TRANSLATION SETTINGS =========
OCR_TRANSLATOR_CONFIG = {
    "translation_file": "translations.txt",
    # source/target can be kept for other flows if you want, but OpenRouter uses api_key+model:
    "source_lang": "ko",
    "target_lang": "en",
    # **New: OpenRouter settings**
    "api_key": "YOUR_OPENROUTER_API_KEY_HERE",  # you can set env var instead
    "model": "google/gemma-3-4b-it:free",
}

# ========= IMAGE WRITER SETTINGS =========
IMAGE_WRITER_CONFIG = {
    "output_folder": "manhwa_translated",  # Where translated images will be stored
    "font_path": "arial.ttf",              # Path to font file
    "font_size": 21,                       # Font size for translated text
    "words_per_line": 5                    # Wrap text after this many words
}

# ========= PDF GENERATOR SETTINGS =========
PDF_GENERATOR_CONFIG = {
    "output_pdf": "manhwa_translated.pdf",   # Final PDF file path
    "image_folder": "manhwa_translated"      # Folder containing translated images
}
