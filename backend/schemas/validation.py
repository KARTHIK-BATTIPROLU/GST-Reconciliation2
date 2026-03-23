"""
Pydantic schemas for input validation.
"""

from pydantic import BaseModel, Field, field_validator
import re

class GSTINQuery(BaseModel):
    gstin: str

    @field_validator('gstin')
    def validate_gstin(cls, v):
        # Basic regex for GSTIN format: 2 digits, 5 letters, 4 digits, 1 letter, 1 alphanumeric, 'Z', 1 alphanumeric
        # Allowing a bit of leniency for testing if needed, but stricter is better for production
        if not re.match(r'^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z0-9]{1}Z[A-Z0-9]{1}$', v):
            raise ValueError("Invalid GSTIN format")
        return v

class InvoiceQuery(BaseModel):
    invoice_id: str
    
    @field_validator('invoice_id')
    def validate_invoice_id(cls, v):
        if len(v) > 50 or not re.match(r'^[A-Za-z0-9\-_]+$', v):
             raise ValueError("Invalid Invoice ID")
        return v
