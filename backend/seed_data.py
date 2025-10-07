import sys
from datetime import date, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Employee, Attendance, Performance
from auth import get_password_hash

Base.metadata.create_all(bind=engine)

def seed_employees(db: Session):
    employees_data = [
        {
            "name": "Admin User",
            "email": "admin@company.com",
            "department": "Management",
            "salary": 120000.0,
            "hire_date": date(2020, 1, 15),
            "role": "Admin",
            "password": "admin123"
        },
        {
            "name": "HR Manager",
            "email": "hr@company.com",
            "department": "HR",
            "salary": 85000.0,
            "hire_date": date(2020, 3, 10),
            "role": "HR",
            "password": "hr123"
        },
        {
            "name": "John Doe",
            "email": "john.doe@company.com",
            "department": "Engineering",
            "salary": 95000.0,
            "hire_date": date(2021, 6, 1),
            "role": "Employee",
            "password": "password123"
        },
        {
            "name": "Jane Smith",
            "email": "jane.smith@company.com",
            "department": "Engineering",
            "salary": 92000.0,
            "hire_date": date(2021, 7, 15),
            "role": "Employee",
            "password": "password123"
        },
        {
            "name": "Michael Brown",
            "email": "michael.brown@company.com",
            "department": "Sales",
            "salary": 78000.0,
            "hire_date": date(2022, 1, 20),
            "role": "Employee",
            "password": "password123"
        },
        {
            "name": "Emily Davis",
            "email": "emily.davis@company.com",
            "department": "Marketing",
            "salary": 72000.0,
            "hire_date": date(2022, 3, 5),
            "role": "Employee",
            "password": "password123"
        },
        {
            "name": "David Wilson",
            "email": "david.wilson@company.com",
            "department": "Engineering",
            "salary": 98000.0,
            "hire_date": date(2021, 9, 12),
            "role": "Employee",
            "password": "password123"
        },
        {
            "name": "Sarah Johnson",
            "email": "sarah.johnson@company.com",
            "department": "Finance",
            "salary": 88000.0,
            "hire_date": date(2022, 2, 18),
            "role": "Employee",
            "password": "password123"
        },
        {
            "name": "Robert Taylor",
            "email": "robert.taylor@company.com",
            "department": "Sales",
            "salary": 75000.0,
            "hire_date": date(2022, 5, 8),
            "role": "Employee",
            "password": "password123"
        },
        {
            "name": "Lisa Anderson",
            "email": "lisa.anderson@company.com",
            "department": "Marketing",
            "salary": 70000.0,
            "hire_date": date(2022, 6, 22),
            "role": "Employee",
            "password": "password123"
        },
        {
            "name": "James Martinez",
            "email": "james.martinez@company.com",
            "department": "Engineering",
            "salary": 96000.0,
            "hire_date": date(2021, 11, 3),
            "role": "Employee",
            "password": "password123"
        },
        {
            "name": "Patricia Garcia",
            "email": "patricia.garcia@company.com",
            "department": "HR",
            "salary": 68000.0,
            "hire_date": date(2022, 8, 15),
            "role": "Employee",
            "password": "password123"
        },
        {
            "name": "Christopher Lee",
            "email": "christopher.lee@company.com",
            "department": "Finance",
            "salary": 82000.0,
            "hire_date": date(2022, 4, 10),
            "role": "Employee",
            "password": "password123"
        },
        {
            "name": "Jennifer White",
            "email": "jennifer.white@company.com",
            "department": "Sales",
            "salary": 76000.0,
            "hire_date": date(2022, 7, 28),
            "role": "Employee",
            "password": "password123"
        },
        {
            "name": "Daniel Harris",
            "email": "daniel.harris@company.com",
            "department": "Engineering",
            "salary": 94000.0,
            "hire_date": date(2022, 9, 5),
            "role": "Employee",
            "password": "password123"
        }
    ]

    for emp_data in employees_data:
        existing = db.query(Employee).filter(Employee.email == emp_data["email"]).first()
        if not existing:
            password = emp_data.pop("password")
            employee = Employee(
                **emp_data,
                password_hash=get_password_hash(password[:72])
            )
            db.add(employee)

    db.commit()
    print("✓ Employees seeded successfully")

def seed_attendance(db: Session):
    employees = db.query(Employee).all()
    start_date = date.today() - timedelta(days=30)

    for emp in employees:
        for i in range(22):
            attendance_date = start_date + timedelta(days=i)

            if attendance_date.weekday() < 5:
                existing = db.query(Attendance).filter(
                    Attendance.employee_id == emp.id,
                    Attendance.date == attendance_date
                ).first()

                if not existing:
                    import random
                    status = random.choices(
                        ["Present", "Absent", "Leave"],
                        weights=[85, 5, 10]
                    )[0]

                    hours = 8.0 if status == "Present" else 0.0

                    attendance = Attendance(
                        employee_id=emp.id,
                        date=attendance_date,
                        status=status,
                        hours_worked=hours
                    )
                    db.add(attendance)

    db.commit()
    print("✓ Attendance records seeded successfully")

def seed_performance(db: Session):
    employees = db.query(Employee).all()

    months = ["2024-01", "2024-02", "2024-03"]

    for emp in employees:
        for month in months:
            existing = db.query(Performance).filter(
                Performance.employee_id == emp.id,
                Performance.month == month
            ).first()

            if not existing:
                import random
                attendance_records = db.query(Attendance).filter(
                    Attendance.employee_id == emp.id
                ).all()

                if attendance_records:
                    present_count = len([a for a in attendance_records if a.status == "Present"])
                    total_count = len(attendance_records)
                    attendance_pct = (present_count / total_count * 100) if total_count > 0 else 0
                else:
                    attendance_pct = 85.0

                kpi_score = random.uniform(6.0, 9.5)

                performance = Performance(
                    employee_id=emp.id,
                    month=month,
                    kpi_score=round(kpi_score, 2),
                    attendance_percentage=round(attendance_pct, 2)
                )
                db.add(performance)

    db.commit()
    print("✓ Performance records seeded successfully")

def main():
    db = SessionLocal()
    try:
        print("Starting database seeding...")
        seed_employees(db)
        seed_attendance(db)
        seed_performance(db)
        print("\n✅ All data seeded successfully!")
        print("\nDemo Login Credentials:")
        print("Admin: admin@company.com / admin123")
        print("HR: hr@company.com / hr123")
        print("Employee: john.doe@company.com / password123")
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
