import sys
from pdf2image import convert_from_path

from contour import get_contours

def load_pdf(pdf_path):
    # Convert PDF to list of images
    images = convert_from_path(pdf_path)

    # Save images to files
    for i, image in enumerate(images):
        image.save(f'temp.png', 'PNG')
        cropped_images = get_contours(image_path='temp.png', save_partial_images=False)

        print(f"image {i} segments {len(cropped_images)}")
        for img in cropped_images:
            # Do OCR here
            pass
if __name__ == '__main__':
    load_pdf(sys.argv[1])
