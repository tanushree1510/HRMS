# AI-Powered Human Resource Management System (HRMS)

A complete, production-ready HRMS built with FastAPI, Streamlit, and SQLite. Features role-based access control, attendance tracking, performance management, and AI-powered resume screening, performance prediction, and HR chatbot.

## Features

### Core HR Features
- **Employee Management**: Full CRUD operations for employee records
- **Attendance Tracking**: Daily attendance marking with history
- **Performance Management**: KPI tracking and performance records
- **Role-Based Access**: Admin, HR, and Employee dashboards
- **JWT Authentication**: Secure login with role-based permissions
- **Data Export**: CSV export for reports

### AI Features
1. **Resume Screening**: Upload job description and multiple resumes to find matching candidates using TF-IDF and cosine similarity
2. **Performance Prediction**: Train RandomForest model on employee KPI and attendance data to predict future performance
3. **HR Chatbot**: Rule-based chatbot answering FAQs about leave policies, payroll, benefits, onboarding, and company policies

### Role-Based Dashboards
- **Admin**: Full system access, employee management, AI features
- **HR**: Employee viewing, attendance, performance management, AI features
- **Employee**: Personal information, attendance history, performance records, chatbot

## Tech Stack

- **Backend**: FastAPI (Python async REST APIs)
- **Frontend**: Streamlit (role-based dashboards)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT with passlib/bcrypt
- **ML/AI**: scikit-learn, TF-IDF, PyPDF2, python-docx
- **Deployment**: Local Mac (no Docker required)



## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- macOS (tested on Mac, should work on Linux/Windows)

### Step 1: Install Dependencies

```bash
cd hrms_project
pip install -r requirements.txt
```

### Step 2: Initialize Database with Sample Data

```bash
cd backend
python seed_data.py
```

This will create:
- 15 employees (Admin, HR, and Employee roles)
- 1 month of attendance records
- 3 months of performance data

### Step 3: Start Backend Server

```bash
# From backend directory
uvicorn main:app --reload
```

Backend will run on: http://localhost:8000

### Step 4: Start Frontend (New Terminal)

```bash
# From hrms_project root directory
cd frontend
streamlit run app.py
```

Frontend will run on: http://localhost:8501

## Usage

### Login Credentials

**Admin Account:**
- Email: admin@company.com
- Password: admin123
- Access: Full system access

**HR Account:**
- Email: hr@company.com
- Password: hr123
- Access: Employee and attendance management

**Employee Account:**
- Email: john.doe@company.com
- Password: password123
- Access: Personal information only


## Quick Start Summary

```bash
# 1. Install dependencies
cd hrms_project
pip install -r requirements.txt

# 2. Seed database
cd backend
python seed_data.py

# 3. Start backend (Terminal 1)
uvicorn main:app --reload

# 4. Start frontend (Terminal 2)
cd ../frontend
streamlit run app.py

# 5. Login at http://localhost:8501
# Admin: admin@company.com / admin123
```

Enjoy your AI-powered HRMS!
