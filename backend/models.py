from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    department = Column(String, nullable=False)
    salary = Column(Float, nullable=False)
    hire_date = Column(Date, nullable=False)
    role = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)

    attendance_records = relationship("Attendance", back_populates="employee")
    performance_records = relationship("Performance", back_populates="employee")

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    date = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    hours_worked = Column(Float, default=8.0)

    employee = relationship("Employee", back_populates="attendance_records")

class Performance(Base):
    __tablename__ = "performance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    month = Column(String, nullable=False)
    kpi_score = Column(Float, nullable=False)
    attendance_percentage = Column(Float, nullable=False)
    predicted_score = Column(Float, nullable=True)

    employee = relationship("Employee", back_populates="performance_records")

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    match_score = Column(Float, nullable=True)
