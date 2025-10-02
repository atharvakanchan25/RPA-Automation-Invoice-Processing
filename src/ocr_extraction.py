"""
OCR Extraction Module
Extracts text from invoice images/PDFs using Tesseract OCR.
"""

import cv2
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

# Optionally set the tesseract binary location (uncomment and update as needed)
import cv2
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

# Set the tesseract executable path for Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class OCRExtractor:
    # rest of your class code
    ...

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class OCRExtractor:
    """Handles OCR operations for invoice processing."""

    def __init__(self):
        self.supported_formats = ['.pdf', '.jpg', '.jpeg', '.png']

    def preprocess_image(self, image_path):
        """Preprocess image to improve OCR accuracy."""
        try:
            img = cv2.imread(image_path)
            if img is None:
                print(f"Error: Unable to read image file - {image_path}")
                return None
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            denoised = cv2.medianBlur(thresh, 3)
            return denoised
        except Exception as e:
            print(f"Error in image preprocessing: {str(e)}")
            return None

    def extract_text_from_image(self, image_path):
        """Extract text from image using Tesseract OCR."""
        try:
            processed_img = self.preprocess_image(image_path)
            if processed_img is None:
                return ""
            text = pytesseract.image_to_string(processed_img, config='--psm 6')
            return text
        except Exception as e:
            print(f"Error extracting text from image: {str(e)}")
            return ""

    def extract_text_from_pdf(self, pdf_path):
        """Convert PDF to images and extract text."""
        try:
            images = convert_from_path(pdf_path, dpi=300)
            extracted_text = ""
            for i, img in enumerate(images):
                temp_img_path = f"temp_page_{i}.jpg"
                img.save(temp_img_path, 'JPEG')
                text = self.extract_text_from_image(temp_img_path)
                extracted_text += text + "\n"
                os.remove(temp_img_path)
            return extracted_text
        except Exception as e:
            print(f"Error extracting text from PDF: {str(e)}")
            return ""

    def extract_text(self, file_path):
        """Main extraction method - handles both images and PDFs."""
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_ext}")
        if file_ext == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        else:
            text = self.extract_text_from_image(file_path)
        confidence = self._calculate_confidence(text)
        return text, confidence

    def _calculate_confidence(self, text):
        """Calculate OCR confidence score."""
        if not text:
            return 0.0
        alphanumeric = sum(c.isalnum() for c in text)
        total = len(text.strip())
        if total == 0:
            return 0.0
        confidence = (alphanumeric / total) * 100
        return round(confidence, 2)

# --- Test code ---
if __name__ == "__main__":
    extractor = OCRExtractor()
    test_file = "../data/raw_invoices/sample_invoice_1.pdf"   # Updated to match your filename
    if os.path.exists(test_file):
        text, confidence = extractor.extract_text(test_file)
        print(f"Extracted Text:\n{text}\n")
        print(f"Confidence: {confidence}%")
    else:
        print("Sample invoice not found. Place a test invoice in data/raw_invoices/")
