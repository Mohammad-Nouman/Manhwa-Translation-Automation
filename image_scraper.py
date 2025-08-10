# image_scraper.py
import os
import requests
from bs4 import BeautifulSoup
from typing import Optional
from urllib.parse import urljoin


def scrape_images(url: str, selector: str, output_folder: str) -> None:
    """
    Scrapes and downloads images from a given web page.

    Args:
        url (str): The URL of the web page to scrape.
        selector (str): CSS selector to find the image elements.
        output_folder (str): Directory to save the downloaded images.

    Raises:
        Exception: If the page request fails (non-200 status code).

    Example:
        scrape_images(
            url="https://example.com/comic",
            selector="div.comic-page img",
            output_folder="manhwa_images"
        )
    """
    os.makedirs(output_folder, exist_ok=True)

    print(f"Fetching page: {url}")
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        raise Exception(f"Failed to fetch {url} (status {response.status_code})")

    soup = BeautifulSoup(response.text, "html.parser")
    images = soup.select(selector)
    print(f"Found {len(images)} image(s) with selector '{selector}'.")

    for idx, img_tag in enumerate(images, start=1):
        img_url: Optional[str] = img_tag.get("src")
        if not img_url:
            continue

        # If src is relative, make it absolute
        if img_url.startswith("/"):
            img_url = urljoin(url, img_url)

        try:
            img_data = requests.get(img_url, headers={"User-Agent": "Mozilla/5.0"}).content
            img_name = os.path.join(output_folder, f"image_{idx}.jpg")
            with open(img_name, "wb") as f:
                f.write(img_data)
            print(f"✅ Downloaded: {img_name}")
        except Exception as e:
            print(f"❌ Failed to download {img_url}: {e}")

    print(f"📦 Total images downloaded: {len(images)}")
