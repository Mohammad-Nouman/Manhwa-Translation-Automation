import os
from fpdf import FPDF
from typing import List



class PDFGenerator:
    def __init__(self, output_pdf: str):
        """
        Initialize PDF generator.

        Args:
            output_pdf (str): Path where the generated PDF will be saved.
        """
        self.output_pdf = output_pdf
        self.pdf = FPDF()

    def add_images(self, image_paths: List[str]) -> None:
        """
        Add images to the PDF, one per page.

        Args:
            image_paths (List[str]): List of image file paths to include.
        """
        for img_path in image_paths:
            if not os.path.isfile(img_path):
                print(f"⚠ Skipping missing image: {img_path}")
                continue

            self.pdf.add_page()
            self.pdf.image(img_path, x=10, y=10, w=190)

    def save_pdf(self) -> None:
        """
        Save the PDF to the output path.
        """
        os.makedirs(os.path.dirname(self.output_pdf), exist_ok=True)
        self.pdf.output(self.output_pdf)
        print(f"✅ PDF saved to {self.output_pdf}")


def generate_pdf(image_folder: str, output_pdf: str) -> None:
    """
    Generate a PDF from all images in a given folder.

    Args:
        image_folder (str): Path to folder containing images.
        output_pdf (str): Path where PDF will be saved.
    """
    image_files = sorted(
        [
            os.path.join(image_folder, f)
            for f in os.listdir(image_folder)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
    )

    if not image_files:
        print(f"⚠ No images found in {image_folder}")
        return

    pdf_gen = PDFGenerator(output_pdf)
    pdf_gen.add_images(image_files)
    pdf_gen.save_pdf()
