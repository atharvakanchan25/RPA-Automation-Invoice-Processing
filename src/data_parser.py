import re
from datetime import datetime


class InvoiceParser:
    """Parse raw OCR text to extract structured invoice data"""
    
    def __init__(self):
        # Regex patterns for common invoice fields
        self.patterns = {
            'invoice_number': [
                r'Invoice\s*#?\s*:?\s*([A-Z0-9\-]+)',
                r'Invoice\s*Number\s*:?\s*([A-Z0-9\-]+)',
                r'Bill\s*No\.?\s*:?\s*([A-Z0-9\-]+)'
            ],
            'date': [
                r'Date\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'Invoice\s*Date\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})'
            ],
            'vendor': [
                r'^([A-Z][A-Za-z\s&\.]+(?:Inc|LLC|Ltd|Corp|Company)?)',
                r'From\s*:?\s*([A-Z][A-Za-z\s&\.]+)'
            ],
            'amount': [
                r'Total\s*:?\s*\$?\s*([\d,]+\.?\d{0,2})',
                r'Amount\s*Due\s*:?\s*\$?\s*([\d,]+\.?\d{0,2})',
                r'Grand\s*Total\s*:?\s*\$?\s*([\d,]+\.?\d{0,2})'
            ],
            'tax': [
                r'Tax\s*:?\s*\$?\s*([\d,]+\.?\d{0,2})',
                r'GST\s*:?\s*\$?\s*([\d,]+\.?\d{0,2})',
                r'VAT\s*:?\s*\$?\s*([\d,]+\.?\d{0,2})'
            ]
        }
    
    def parse_invoice(self, text):
        """
        Parse invoice text and extract key fields
        Args:
            text: Raw OCR extracted text
        Returns:
            Dictionary with parsed invoice data
        """
        invoice_data = {
            'invoice_number': None,
            'date': None,
            'vendor': None,
            'amount': None,
            'tax': None,
            'status': 'pending',
            'confidence': {}
        }
        
        # Extract each field
        for field, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    invoice_data[field] = match.group(1).strip()
                    invoice_data['confidence'][field] = 95  # Simplified confidence
                    break
            
            # Set default confidence for missing fields
            if not invoice_data[field]:
                invoice_data['confidence'][field] = 0
        
        # Format and clean extracted data
        invoice_data = self._clean_data(invoice_data)
        
        return invoice_data
    
    def _clean_data(self, data):
        """Clean and format extracted data"""
        
        # Clean amount (remove commas, ensure float)
        if data['amount']:
            try:
                data['amount'] = float(data['amount'].replace(',', ''))
            except ValueError:
                data['amount'] = None
        
        # Clean tax
        if data['tax']:
            try:
                data['tax'] = float(data['tax'].replace(',', ''))
            except ValueError:
                data['tax'] = None
        
        # Clean invoice number (uppercase, remove extra spaces)
        if data['invoice_number']:
            data['invoice_number'] = data['invoice_number'].upper().strip()
        
        # Clean vendor name
        if data['vendor']:
            data['vendor'] = ' '.join(data['vendor'].split())
        
        # Parse date to standard format
        if data['date']:
            data['date'] = self._standardize_date(data['date'])
        
        return data
    
    def _standardize_date(self, date_str):
        """Convert various date formats to YYYY-MM-DD"""
        date_formats = [
            '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y',
            '%d/%m/%y', '%m/%d/%y', '%d %B %Y', '%d %b %Y'
        ]
        
        for fmt in date_formats:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        return date_str  # Return original if parsing fails


# Test function
if __name__ == "__main__":
    parser = InvoiceParser()
    
    # Sample OCR text with properly terminated triple quotes
    sample_text = """
    ABC Company Inc.
    123 Business Street

    Invoice Number: INV-2024-001
    Date: 15/09/2024

    Item Description      Quantity    Price
    Product A             2           $50.00
    Product B             1           $75.00

    Subtotal:                        $125.00
    Tax:                            $9.25

    Grand Total:                    $134.25
    """

    parsed_data = parser.parse_invoice(sample_text)
    print("Parsed Invoice Data:")
    for key, value in parsed_data.items():
        if key != 'confidence':
            print(f"{key}: {value}")
    print("Confidence Scores:", parsed_data['confidence'])
