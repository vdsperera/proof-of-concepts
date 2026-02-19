import pandas as pd
from pydantic import BaseModel, Field, validator, ValidationError
from typing import Optional
import os

# 1. Define the Pydantic Model for Validation
from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError
from typing import Optional
import os

# 1. Define the Pydantic Model for Validation
class Claim(BaseModel):
    Patient_Name: str
    Gender: str
    CPT_Code: str
    Diagnosis_Code: Optional[str] = Field(default=None)
    NPI: str

    @field_validator('Diagnosis_Code')
    @classmethod
    def check_diagnosis_code(cls, v):
        if v is None or str(v).strip() == '' or (isinstance(v, float) and pd.isna(v)):
            raise ValueError("Diagnosis_Code (ICD-10) is missing")
        return v

    @field_validator('NPI', mode='before')
    @classmethod
    def check_npi_length(cls, v):
        npi_str = str(v)
        # Remove decimal if it's a float like "1234567890.0"
        if npi_str.endswith('.0'):
            npi_str = npi_str[:-2]
        if len(npi_str) != 10:
            raise ValueError(f"NPI must be exactly 10 digits, got {len(npi_str)}")
        return npi_str

    @model_validator(mode='after')
    def check_nipt_gender(self):
        if self.CPT_Code == '81420' and self.Gender.lower() == 'male':
            raise ValueError("CPT_Code 81420 (NIPT) is invalid for Gender: Male")
        return self

# 2. Create Sample CSV
def create_sample_csv(filename):
    data = [
        {"Patient_Name": "John Doe", "Gender": "Male", "CPT_Code": "99213", "Diagnosis_Code": "Z00.00", "NPI": "1234567890"},
        {"Patient_Name": "Jane Smith", "Gender": "Female", "CPT_Code": "81420", "Diagnosis_Code": "O09.529", "NPI": "0987654321"},
        {"Patient_Name": "Bob Brown", "Gender": "Male", "CPT_Code": "81420", "Diagnosis_Code": "Z01.89", "NPI": "1122334455"},  # Invalid: NIPT for Male
        {"Patient_Name": "Alice Green", "Gender": "Female", "CPT_Code": "99214", "Diagnosis_Code": None, "NPI": "9988776655"},   # Invalid: Missing Dx
        {"Patient_Name": "Charlie White", "Gender": "Male", "CPT_Code": "99213", "Diagnosis_Code": "J00", "NPI": "12345"},       # Invalid: NPI short
        {"Patient_Name": "Eve Black", "Gender": "Female", "CPT_Code": "81420", "Diagnosis_Code": "O09.529", "NPI": "12345678901"}, # Invalid: NPI long
        {"Patient_Name": "David Blue", "Gender": "Male", "CPT_Code": "45378", "Diagnosis_Code": "K63.5", "NPI": "5566778899"},
        {"Patient_Name": "Sarah Red", "Gender": "Female", "CPT_Code": "81420", "Diagnosis_Code": "O09.529", "NPI": "4433221100"},
        {"Patient_Name": "Tom Grey", "Gender": "Male", "CPT_Code": "99213", "Diagnosis_Code": "", "NPI": "6677889900"},         # Invalid: Empty Dx
        {"Patient_Name": "Grace Gold", "Gender": "Female", "CPT_Code": "99212", "Diagnosis_Code": "Z00.00", "NPI": "7788911223"},
    ]
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Sample file created: {filename}")

# 3. Validation Logic
def validate_claims(input_file):
    df = pd.read_csv(input_file)
    
    clean_claims = []
    error_log = []

    for index, row in df.iterrows():
        try:
            # Convert row to dict, handling NaN/None for Pydantic
            row_dict = row.to_dict()
            # Clean up potential NaN values and ensure all input is string
            for k, v in row_dict.items():
                if pd.isna(v):
                    row_dict[k] = None
                else:
                    row_dict[k] = str(v)
            
            # Additional logic for NPI leading zeros (e.g. if it was read as int)
            # The NPI validator handles length and type conversion.
            # Validate with Pydantic
            valid_claim = Claim(**row_dict)
            clean_claims.append(valid_claim.model_dump())
            
        except ValidationError as e:
            # Capture errors
            for err in e.errors():
                # loc can be (field,) or ('__root__',) or other formats
                field_name = str(err['loc'][0]) if err['loc'] else "model"
                error_info = {
                    "Patient_Name": row['Patient_Name'],
                    "Reason": err['msg'],
                    "Field": field_name
                }
                error_log.append(error_info)
        except Exception as e:
            error_log.append({
                "Patient_Name": row['Patient_Name'],
                "Reason": str(e),
                "Field": "System"
            })

    # Saving results
    if clean_claims:
        pd.DataFrame(clean_claims).to_csv("clean_claims.csv", index=False)
        print("Successfully saved clean_claims.csv")
    
    if error_log:
        pd.DataFrame(error_log).to_csv("error_log.csv", index=False)
        print("Successfully saved error_log.csv")

if __name__ == "__main__":
    input_csv = "sample_claims.csv"
    create_sample_csv(input_csv)
    validate_claims(input_csv)
