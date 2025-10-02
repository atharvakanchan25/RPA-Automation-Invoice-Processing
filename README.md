# Invoice Processing Automation using RPA & OCR

[Live Demo](https://rpa-automation-invoice-processing-fkcxx5yozkcx58qmljgurp.streamlit.app/)

Automated invoice processing system that extracts, validates, and stores invoice data using OCR and RPA techniques.

## 🎯 Project Overview

This system automates the manual invoice entry process by:
- Extracting text from PDF/image invoices using Tesseract OCR
- Parsing key fields (Invoice No, Vendor, Amount, Date, Tax)
- Validating data against business rules
- Storing in SQLite database
- Providing real-time dashboard for monitoring

## 🛠️ Tech Stack

- **Python 3.8+**
- **Tesseract OCR** - Text extraction
- **OpenCV** - Image preprocessing
- **Selenium** - RPA automation
- **SQLite** - Database
- **Streamlit** - Dashboard
- **Pandas** - Data manipulation
- **Plotly** - Visualizations

## 📦 Installation

1. Clone repository:
 
git remote add origin https://github.com/atharvakanchan25/RPA-Automation-Invoice-Processing.git
cd RPA-Invoice-Processing

2. Install dependencies:
pip install -r requirements.txt


3. Install Tesseract OCR:
- Windows: Download from [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
- Linux: `sudo apt-get install tesseract-ocr`
- Mac: `brew install tesseract`

## 🚀 Usage

### Live Streamlit Dashboard
Access the live demo here: [https://rpa-automation-invoice-processing-fkcxx5yozkcx58qmljgurp.streamlit.app/](https://rpa-automation-invoice-processing-fkcxx5yozkcx58qmljgurp.streamlit.app/)

### Run Dashboard locally:
streamlit run src/dashboard.py

### Process Single Invoice:
from src.ocr_extraction import OCRExtractor
from src.data_parser import InvoiceParser

extractor = OCRExtractor()
parser = InvoiceParser()

text, confidence = extractor.extract_text('invoice.pdf')
invoice_data = parser.parse_invoice(text)
print(invoice_data)

## 📊 Features

- ✅ Multi-format support (PDF, JPG, PNG)
- ✅ Intelligent OCR with preprocessing
- ✅ Regex-based data extraction
- ✅ Business rule validation
- ✅ Duplicate detection
- ✅ Database storage
- ✅ Interactive dashboard
- ✅ Statistics and reporting

## 🎓 For Recruiters

**Skills Demonstrated:**
- Python automation
- OCR implementation
- RPA concepts
- Database design
- Web dashboard development
- Data validation
- Project structuring

**Impact:**
- 80% faster processing
- Reduced manual errors
- Scalable architecture

## 📝 License

MIT License

## 👤 Author

[Atharva Kanchan] - [atharvakanchan959@gmail.com]
