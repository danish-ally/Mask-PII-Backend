import pytesseract
import cv2

# Path to Tesseract (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_boxes(image_path):
    image = cv2.imread(image_path)
    data = pytesseract.image_to_data(
        image, output_type=pytesseract.Output.DICT)
    return data
