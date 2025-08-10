"""
app.py
Main pipeline runner for the manhwa translation project.
This file coordinates the scraper, OCR, translator, image writer, and PDF generator.
"""

from config import SCRAPER_CONFIG, OCR_TRANSLATOR_CONFIG, IMAGE_WRITER_CONFIG, PDF_GENERATOR_CONFIG
from image_scraper import scrape_images
from AI_translator import process_all_images
from image_writer import write_translations_on_images
from pdf_generator import generate_pdf


IMAGE_SCRAPER_URL = "https://example.com/manhwa"
IMAGE_SELECTOR = '[id="page_list"] img[alt*="Page"]'



def main():
    print("\n===== STEP 1: SCRAPING IMAGES =====")
    scrape_images(
        url=IMAGE_SCRAPER_URL,
        selector=IMAGE_SELECTOR,
        output_folder=SCRAPER_CONFIG["output_folder"]
    )

    print("\n===== STEP 2: OCR & TRANSLATION =====")
    # from config import SCRAPER_CONFIG, OCR_TRANSLATOR_CONFIG
    process_all_images(
        image_folder=SCRAPER_CONFIG.get("output_folder"),
        translation_file=OCR_TRANSLATOR_CONFIG.get("translation_file"),
        api_key=OCR_TRANSLATOR_CONFIG.get("api_key"),
        model=OCR_TRANSLATOR_CONFIG.get("model"),
    )

    print("\n===== STEP 3: WRITING TRANSLATIONS ON IMAGES =====")
    write_translations_on_images(
        translation_file=OCR_TRANSLATOR_CONFIG["translation_file"],
        image_folder=SCRAPER_CONFIG["output_folder"],
        output_folder=IMAGE_WRITER_CONFIG["output_folder"],
        font_path=IMAGE_WRITER_CONFIG["font_path"],
        font_size=IMAGE_WRITER_CONFIG["font_size"],
        words_per_line=IMAGE_WRITER_CONFIG["words_per_line"]
    )

    print("\n===== STEP 4: GENERATING FINAL PDF =====")
    generate_pdf(
        image_folder=PDF_GENERATOR_CONFIG["image_folder"],
        output_pdf=PDF_GENERATOR_CONFIG["output_pdf"]
    )
    print("\n🎉 All steps completed! Your translated PDF is ready.")


if __name__ == "__main__":
    main()
