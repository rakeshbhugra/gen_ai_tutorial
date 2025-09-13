from pydantic import BaseModel, EmailStr, field_validator, Field
import pandas as pd
import re

class CustomerRecord(BaseModel):
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

    # allow extra fields
    class Config:
        extra = "allow"

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        digits = re.sub(r'[^\d]', '', v)
        if len(digits) < 10:
            raise ValueError('Phone must have at least 10 digits')
        return v

class DataFrameValidator:
    def __init__(self):
        pass

    def validate(self, dataframe):
        if dataframe.empty:
            raise ValueError("DataFrame is empty")

        # check required columns
        required_cols = [
            'Customer ID', 'Customer Name', 'Email', 'Phone',
            'Amount Due', 'Due Date', 'User Status', 'Payment Status'
        ]

        for col in required_cols:
            if col not in dataframe.columns:
                raise ValueError(f"Missing required column: {col}")

        # check each row, if it matches the customer record schema
        for idx, row in  dataframe.iterrows():
            try:
                CustomerRecord(**row.to_dict())
            except Exception as e:
                raise ValueError(f"Row {idx} validation error: {str(e)}")


        return dataframe

if __name__ == "__main__":
    df = pd.read_excel("capstone_project_db_management/sample_upload.xlsx") 

    validator = DataFrameValidator()

    try:
        valid_df = validator.validate(df)
        print("DataFrame is valid")
    except Exception as e:
        print(f"Validation error: {str(e)}")