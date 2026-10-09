import fitz  # PyMuPDF
import numpy as np
from PIL import Image
from io import BytesIO
import sys
import os
# Check if the script is run with the correct number of arguments
if len(sys.argv) != 2:
    print("Usage: python auto_crop_pdf.py <input_pdf>")
    sys.exit(1)
# Get command line arguments
input_pdf = sys.argv[1]

def auto_crop_pdf_page(input_pdf, page_number, output_pdf, dpi=150, margin=10):
    doc = fitz.open(input_pdf)
    page = doc[page_number]

    # Render the page to an image
    pix = page.get_pixmap(dpi=dpi)
    img = Image.open(BytesIO(pix.tobytes()))
    gray = img.convert("L")
    np_img = np.array(gray)

    # Find bounding box of non-white area
    threshold = 245  # adjust this threshold if needed
    mask = np_img < threshold
    coords = np.argwhere(mask)

    if coords.size == 0:
        print("Page appears blank.")
        return

    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0)

    # Add optional margin (in pixels)
    x0 = max(x0 - margin, 0)
    y0 = max(y0 - margin, 0)
    x1 = min(x1 + margin, np_img.shape[1])
    y1 = min(y1 + margin, np_img.shape[0])

    # Convert pixel coordinates to PDF points (1 point = 1/72 inch)
    scale = 72 / dpi
    rect = fitz.Rect(x0 * scale, y0 * scale, x1 * scale, y1 * scale)
    if int(page.rect.width) == int(rect.width) and int(page.rect.height) == int(rect.height):
        print(f"No cropping needed for {input_pdf}.")
        return
    # Set crop box
    page.set_cropbox(rect)
    print(f"Crop box set to: {rect}")

    # Save cropped PDF
    out_doc = fitz.open()
    out_doc.insert_pdf(doc, from_page=page_number, to_page=page_number)
    out_doc.save(output_pdf)
    out_doc.close()
    print(f"Cropped PDF saved as: {output_pdf}")

# Example usage
auto_crop_pdf_page(input_pdf, page_number=0, output_pdf=input_pdf, margin=0)
