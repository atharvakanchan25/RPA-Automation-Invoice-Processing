"""
Validation Module
Validates extracted invoice data against business rules
"""

import os
import json
from datetime import datetime


class InvoiceValidator:
    """Validate invoice data against business rules"""
    
    def __init__(self, vendor_list_path='data/vendor_master.json'):
        self.vendor_list_path = vendor_list_path
        self.approved_vendors = self._load_vendor_list()
        self.processed_invoices = set()
    
    def _load_vendor_list(self):
        """Load approved vendor list from JSON"""
        if os.path.exists(self.vendor_list_path):
            with open(self.vendor_list_path, 'r') as f:
                return json.load(f).get('vendors', [])
        else:
            # Create default vendor list
            default_vendors = ['ABC Company Inc', 'XYZ Corp', 'Tech Solutions Ltd']
            return default_vendors
    
    def validate_invoice(self, invoice_data):
        """
        Validate invoice data
        Args:
            invoice_data: Dictionary with invoice fields
        Returns:
            Tuple (is_valid, validation_errors)
        """
        errors = []
        
        # 1. Check if invoice number exists
        if not invoice_data.get('invoice_number'):
            errors.append("Invoice number is missing")
        else:
            # Check for duplicate invoice number
            if invoice_data['invoice_number'] in self.processed_invoices:
                errors.append(f"Duplicate invoice number: {invoice_data['invoice_number']}")
        
        # 2. Validate vendor
        if not invoice_data.get('vendor'):
            errors.append("Vendor name is missing")
        elif not self._is_vendor_approved(invoice_data['vendor']):
            errors.append(f"Vendor '{invoice_data['vendor']}' not in approved list")
        
        # 3. Validate amount
        if not invoice_data.get('amount'):
            errors.append("Invoice amount is missing")
        elif invoice_data['amount'] <= 0:
            errors.append("Invoice amount must be greater than 0")
        
        # 4. Validate date
        if not invoice_data.get('date'):
            errors.append("Invoice date is missing")
        else:
            if not self._is_valid_date(invoice_data['date']):
                errors.append("Invalid invoice date format")
        
        # 5. Check OCR confidence
        avg_confidence = self._calculate_avg_confidence(invoice_data.get('confidence', {}))
        if avg_confidence < 70:
            errors.append(f"Low OCR confidence ({avg_confidence}%). Manual review required.")
        
        # Determine if valid
        is_valid = len(errors) == 0
        
        # Update status
        if is_valid:
            invoice_data['status'] = 'approved'
            self.processed_invoices.add(invoice_data['invoice_number'])
        else:
            invoice_data['status'] = 'review_required'
        
        return is_valid, errors
    
    def _is_vendor_approved(self, vendor_name):
        """Check if vendor exists in approved list"""
        # Case-insensitive partial match
        vendor_lower = vendor_name.lower()
        for approved in self.approved_vendors:
            if approved.lower() in vendor_lower or vendor_lower in approved.lower():
                return True
        return False
    
    def _is_valid_date(self, date_str):
        """Validate date format"""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def _calculate_avg_confidence(self, confidence_dict):
        """Calculate average confidence score"""
        if not confidence_dict:
            return 0
        
        scores = [v for v in confidence_dict.values() if isinstance(v, (int, float))]
        if not scores:
            return 0
        
        return round(sum(scores) / len(scores), 2)


# Test function
if __name__ == "__main__":
    validator = InvoiceValidator()
    
    # Test invoice data
    test_invoice = {
        'invoice_number': 'INV-2024-001',
        'vendor': 'ABC Company Inc',
        'amount': 137.50,
        'tax': 12.50,
        'date': '2024-09-15',
        'confidence': {
            'invoice_number': 95,
            'vendor': 90,
            'amount': 98,
            'date': 92
        }
    }
    
    is_valid, errors = validator.validate_invoice(test_invoice)
    
    print(f"Validation Result: {'PASSED' if is_valid else 'FAILED'}")
    if errors:
        print("Errors:")
        for error in errors:
            print(f"  - {error}")
