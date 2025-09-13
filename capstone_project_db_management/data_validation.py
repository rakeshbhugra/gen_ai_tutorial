from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from typing import Optional, Literal
import pandas as pd
import re


class CustomerRecord(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True
    )
    
    customer_id: str = Field(..., alias='Customer ID')
    customer_name: str = Field(..., alias='Customer Name')
    email: EmailStr = Field(..., alias='Email')
    phone: str = Field(..., alias='Phone')
    service_type: str = Field(..., alias='Service Type')
    amount_due: float = Field(..., alias='Amount Due', gt=0)
    due_date: str = Field(..., alias='Due Date')
    user_status: str = Field(..., alias='User Status')
    last_contact: str = Field(..., alias='Last Contact')
    payment_status: str = Field(..., alias='Payment Status')
    follow_up_required: str = Field(..., alias='Follow Up Required')
    source_file: Optional[str] = Field(None, alias='source_file')
    upload_timestamp: Optional[str] = Field(None, alias='upload_timestamp')
    
    @field_validator('customer_id')
    @classmethod
    def validate_customer_id(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Customer ID cannot be empty')
        return v
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        digits = re.sub(r'[^\d]', '', v)
        if len(digits) < 10:
            raise ValueError('Phone must have at least 10 digits')
        return v


class DataFrameValidator:
    def __init__(self, schema=CustomerRecord):
        self.schema = schema
    
    def validate(self, dataframe: pd.DataFrame, errors: str = "skip") -> pd.DataFrame:
        """
        Validate a DataFrame against the schema.
        
        Args:
            dataframe: DataFrame to validate
            errors: "raise" to raise exception, "skip" to filter out invalid rows
        
        Returns:
            Validated DataFrame (with invalid rows removed if errors="skip")
        """
        if dataframe.empty:
            if errors == "raise":
                raise ValueError("DataFrame is empty")
            return pd.DataFrame()
        
        # Check required columns
        required_cols = [
            'Customer ID', 'Customer Name', 'Email', 'Phone',
            'Service Type', 'Amount Due', 'Due Date', 'User Status',
            'Last Contact', 'Payment Status', 'Follow Up Required'
        ]
        
        missing = [col for col in required_cols if col not in dataframe.columns]
        if missing:
            if errors == "raise":
                raise ValueError(f"Missing columns: {', '.join(missing)}")
            return pd.DataFrame()
        
        valid_rows = []
        invalid_rows = []
        
        for idx, row in dataframe.iterrows():
            try:
                # Validate row
                self.schema(**row.to_dict())
                valid_rows.append(idx)
            except Exception as e:
                invalid_rows.append((idx, str(e)))
                if errors == "raise":
                    raise ValueError(f"Row {idx}: {str(e)}")
        
        # Return filtered DataFrame
        if errors == "skip" and valid_rows:
            return dataframe.loc[valid_rows].reset_index(drop=True)
        elif errors == "skip":
            return pd.DataFrame()
        
        return dataframe


def validate_upload(df: pd.DataFrame, show_errors: bool = True) -> tuple[bool, pd.DataFrame, str]:
    """
    Simple validation wrapper for Streamlit.
    
    Returns:
        Tuple of (is_valid, valid_df, message)
    """
    validator = DataFrameValidator()
    
    try:
        # Try validation with error skipping
        valid_df = validator.validate(df, errors="skip")
        
        if valid_df.empty:
            return False, valid_df, "No valid records found"
        
        if len(valid_df) < len(df):
            invalid_count = len(df) - len(valid_df)
            return True, valid_df, f"{len(valid_df)} valid records, {invalid_count} invalid records skipped"
        
        return True, valid_df, f"All {len(valid_df)} records are valid"
        
    except Exception as e:
        return False, pd.DataFrame(), f"Validation error: {str(e)}"