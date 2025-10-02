"""
RPA Bot Module
Automates invoice entry into dummy ERP system using Selenium
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


class ERPBot:
    """RPA bot for automating ERP data entry"""
    
    def __init__(self, erp_url='http://localhost:8501'):
        self.erp_url = erp_url
        self.driver = None
    
    def initialize_browser(self):
        """Initialize Selenium WebDriver"""
        try:
            # Setup Chrome driver
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            options.add_argument('--start-maximized')
            # options.add_argument('--headless')  # Uncomment for headless mode
            
            self.driver = webdriver.Chrome(service=service, options=options)
            print("Browser initialized successfully")
            return True
        
        except Exception as e:
            print(f"Error initializing browser: {str(e)}")
            return False
    
    def fill_invoice_form(self, invoice_data):
        """
        Automate filling invoice form in ERP system
        Args:
            invoice_data: Dictionary with invoice fields
        Returns:
            Boolean success status
        """
        try:
            # Navigate to ERP page
            self.driver.get(self.erp_url)
            time.sleep(2)
            
            # Wait for page to load
            wait = WebDriverWait(self.driver, 10)
            
            # Fill Invoice Number
            invoice_num_field = wait.until(
                EC.presence_of_element_located((By.NAME, "invoice_number"))
            )
            invoice_num_field.clear()
            invoice_num_field.send_keys(invoice_data.get('invoice_number', ''))
            
            # Fill Vendor
            vendor_field = self.driver.find_element(By.NAME, "vendor")
            vendor_field.clear()
            vendor_field.send_keys(invoice_data.get('vendor', ''))
            
            # Fill Amount
            amount_field = self.driver.find_element(By.NAME, "amount")
            amount_field.clear()
            amount_field.send_keys(str(invoice_data.get('amount', 0)))
            
            # Fill Tax
            if invoice_data.get('tax'):
                tax_field = self.driver.find_element(By.NAME, "tax")
                tax_field.clear()
                tax_field.send_keys(str(invoice_data.get('tax', 0)))
            
            # Fill Date
            date_field = self.driver.find_element(By.NAME, "date")
            date_field.clear()
            date_field.send_keys(invoice_data.get('date', ''))
            
            # Submit form
            submit_button = self.driver.find_element(By.NAME, "submit")
            submit_button.click()
            
            time.sleep(2)
            
            # Check for success message
            success_msg = self.driver.find_element(By.CLASS_NAME, "success-message")
            if success_msg:
                print(f"✓ Invoice {invoice_data.get('invoice_number')} submitted successfully")
                return True
            
            return False
        
        except Exception as e:
            print(f"Error filling form: {str(e)}")
            return False
    
    def close_browser(self):
        """Close browser and cleanup"""
        if self.driver:
            self.driver.quit()
            print("Browser closed")


# Test function
if __name__ == "__main__":
    bot = ERPBot()
    
    # Test invoice data
    test_invoice = {
        'invoice_number': 'INV-BOT-001',
        'vendor': 'Automation Test Corp',
        'amount': 750.00,
        'tax': 75.00,
        'date': '2024-10-02'
    }
    
    if bot.initialize_browser():
        success = bot.fill_invoice_form(test_invoice)
        print(f"Form filling: {'SUCCESS' if success else 'FAILED'}")
        bot.close_browser()
