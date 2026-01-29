from pydantic import BaseModel, EmailStr, Field,ConfigDict,field_validator
from datetime import date

class EmployeeCreate(BaseModel):
    employee_id:str= Field(..., min_length=1)
    full_name: str = Field(..., min_length=1)
    email: EmailStr
    department: str = Field(..., min_length=1)

    @field_validator("employee_id", mode="before")
    @classmethod
    def normalize_employee_id(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Employee ID cannot be empty")
        return value.strip().lower()

class EmployeeResponse(BaseModel):
    id: int
    employee_id: str
    full_name: str
    email: str
    department: str

    model_config = ConfigDict(from_attributes=True)

    # class Config:
    #     orm_mode = True

class AttendanceCreate(BaseModel):
    date: date
    status: str

class AttendanceResponse(BaseModel):
    
    message:str
