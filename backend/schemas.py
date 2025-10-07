from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    department: str
    salary: float
    hire_date: date
    role: str

class EmployeeCreate(EmployeeBase):
    password: str

class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        from_attributes = True

class AttendanceBase(BaseModel):
    employee_id: int
    date: date
    status: str
    hours_worked: float = 8.0

class AttendanceResponse(AttendanceBase):
    id: int

    class Config:
        from_attributes = True

class PerformanceBase(BaseModel):
    employee_id: int
    month: str
    kpi_score: float
    attendance_percentage: float

class PerformanceResponse(PerformanceBase):
    id: int
    predicted_score: Optional[float] = None

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str
    employee_id: int
