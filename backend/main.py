from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
from datetime import datetime, date

from database import engine, get_db, Base
from models import Employee, Attendance, Performance, Resume
from schemas import (
    EmployeeCreate, EmployeeResponse, AttendanceBase, AttendanceResponse,
    PerformanceBase, PerformanceResponse, LoginRequest, TokenResponse
)
from auth import (
    verify_password, get_password_hash, create_access_token,
    get_current_user, require_role
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="HRMS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/auth/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.email == request.email).first()
    if not employee or not verify_password(request.password, employee.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(
        data={"sub": employee.email, "role": employee.role, "employee_id": employee.id}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": employee.role,
        "employee_id": employee.id
    }

@app.post("/employees", response_model=EmployeeResponse)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin", "HR"]))
):
    db_employee = db.query(Employee).filter(Employee.email == employee.email).first()
    if db_employee:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(employee.password)
    db_employee = Employee(
        name=employee.name,
        email=employee.email,
        department=employee.department,
        salary=employee.salary,
        hire_date=employee.hire_date,
        role=employee.role,
        password_hash=hashed_password
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.get("/employees", response_model=List[EmployeeResponse])
def get_employees(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] in ["Admin", "HR"]:
        return db.query(Employee).all()
    else:
        employee = db.query(Employee).filter(Employee.id == current_user["employee_id"]).first()
        return [employee] if employee else []

@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] not in ["Admin", "HR"] and current_user["employee_id"] != employee_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin", "HR"]))
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee.name = employee_data.name
    employee.email = employee_data.email
    employee.department = employee_data.department
    employee.salary = employee_data.salary
    employee.hire_date = employee_data.hire_date
    employee.role = employee_data.role
    if employee_data.password:
        employee.password_hash = get_password_hash(employee_data.password)

    db.commit()
    db.refresh(employee)
    return employee

@app.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin"]))
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully"}

@app.post("/attendance", response_model=AttendanceResponse)
def create_attendance(
    attendance: AttendanceBase,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin", "HR"]))
):
    db_attendance = Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

@app.get("/attendance", response_model=List[AttendanceResponse])
def get_attendance(
    employee_id: int = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    query = db.query(Attendance)
    if employee_id:
        if current_user["role"] not in ["Admin", "HR"] and current_user["employee_id"] != employee_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        query = query.filter(Attendance.employee_id == employee_id)
    elif current_user["role"] == "Employee":
        query = query.filter(Attendance.employee_id == current_user["employee_id"])

    return query.all()

@app.post("/performance", response_model=PerformanceResponse)
def create_performance(
    performance: PerformanceBase,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["Admin", "HR"]))
):
    db_performance = Performance(**performance.dict())
    db.add(db_performance)
    db.commit()
    db.refresh(db_performance)
    return db_performance

@app.get("/performance", response_model=List[PerformanceResponse])
def get_performance(
    employee_id: int = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    query = db.query(Performance)
    if employee_id:
        if current_user["role"] not in ["Admin", "HR"] and current_user["employee_id"] != employee_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        query = query.filter(Performance.employee_id == employee_id)
    elif current_user["role"] == "Employee":
        query = query.filter(Performance.employee_id == current_user["employee_id"])

    return query.all()

@app.get("/")
def root():
    return {"message": "HRMS API is running"}
