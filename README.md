
# Manhwa Translation Automation

This project automates the process of scraping, OCR (text extraction), translation, and rewriting text in manhwa/comic images.

## Features
- **Image Scraper**: Downloads all pages from an online manhwa/comic chapter.
- **OCR Extraction**: Uses EasyOCR to detect and extract Korean text from images.
- **Translation**: Translates the extracted text into English using a translation API.
- **Image Writer**: Overwrites the translated text back onto the original images with word wrapping.
- **Configurable**: All settings such as font size, output folders, and languages are stored in a `config.py` file.

## Project Structure
```
manhwa_translator
├── main.py                  # Main runner file
├── config.py               # Configuration variables
├── scraper.py              # Downloads all pages of the manhwa
├── ocr_translator.py       # Extracts text and translates
├── image_writer.py         # Writes translated text onto images
├── translations.txt        # Stores original and translated text
└── README.md               # This file
```

## Setup & Installation

1. Clone the repository:
```bash
  git clone https://github.com/yourusername/manhwa-translation-automation.git
cd manhwa-translation-automation
```

2. Install dependencies:
```bash
  pip install -r requirements.txt
```

3. Make sure Tesseract OCR is installed if using it instead of EasyOCR.

4. Update the `config.py` file with your desired settings.

## Usage
Run the main script:
```bash
  python app.py
```

The script will:
1. Scrape all images from the target URL.
2. Extract text from the images.
3. Translate the text.
4. Write translated text onto images.
5. Save the final results in the output folder.

## Configuration
Edit `config.py` to change:
- Output folders
- Languages for OCR and translation
- Font settings
- API keys (if required for translation)

## Example Workflow
```text
===== STEP 1: SCRAPING IMAGES =====
Downloaded: page_1.jpg
Downloaded: page_2.jpg

===== STEP 2: OCR & TRANSLATION =====
Detected text: 안녕하세요
Translated text: Hello

===== STEP 3: WRITING TRANSLATIONS =====
Image updated: page_1.jpg
```

