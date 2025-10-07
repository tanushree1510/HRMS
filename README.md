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

## Project Structure

```
hrms_project/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # JWT authentication
│   └── seed_data.py         # Database seeding script
├── frontend/
│   └── app.py               # Streamlit application
├── ml_models/
│   ├── resume_screening.py  # Resume screening AI
│   ├── performance_prediction.py  # Performance prediction AI
│   ├── chatbot.py           # HR chatbot
│   └── performance_model.pkl     # Trained model (generated)
├── db/
│   └── hrms.db              # SQLite database (generated)
├── uploads/
│   └── resumes/             # Uploaded resumes storage
├── sample_data/
│   ├── job_description.txt  # Sample JD
│   └── resumes/             # 20 sample resumes
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

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

### Testing AI Features

#### 1. Resume Screening

1. Login as Admin or HR
2. Navigate to "AI Features" → "Resume Screening"
3. Upload Job Description: `sample_data/job_description.txt`
4. Upload Resumes: Select multiple files from `sample_data/resumes/`
5. Click "Screen Resumes"
6. View matching resumes with scores (12 matching, 8 non-matching)

**What it does**: Uses TF-IDF vectorization and cosine similarity to compare resume text against job description requirements. Returns only resumes meeting the threshold with match scores.

#### 2. Performance Prediction

1. Navigate to "AI Features" → "Performance Prediction"
2. Click "Train Model" (trains on existing performance data)
3. Adjust KPI Score and Attendance % sliders
4. Click "Predict" to see predicted performance score

**What it does**: Trains a RandomForest regression model on historical employee KPI scores and attendance percentages to predict future performance.

#### 3. HR Chatbot

1. Navigate to "HR Chatbot" tab (available in all dashboards)
2. Ask questions like:
   - "What is the leave policy?"
   - "When do I get paid?"
   - "Tell me about company benefits"
   - "How do I contact HR?"

**What it does**: Rule-based FAQ system with keyword matching. Returns relevant HR policy information. Can be upgraded with GPT API key for more intelligent responses.

## API Endpoints

### Authentication
- `POST /auth/login` - Login and get JWT token

### Employees
- `GET /employees` - List all employees
- `GET /employees/{id}` - Get employee details
- `POST /employees` - Create employee (Admin/HR only)
- `PUT /employees/{id}` - Update employee (Admin/HR only)
- `DELETE /employees/{id}` - Delete employee (Admin only)

### Attendance
- `GET /attendance` - List attendance records
- `POST /attendance` - Mark attendance (Admin/HR only)

### Performance
- `GET /performance` - List performance records
- `POST /performance` - Add performance record (Admin/HR only)

### API Documentation
Visit http://localhost:8000/docs for interactive API documentation (Swagger UI)

## Database Schema

### Employees Table
- id, name, email, department, salary, hire_date, role, password_hash

### Attendance Table
- id, employee_id, date, status, hours_worked

### Performance Table
- id, employee_id, month, kpi_score, attendance_percentage, predicted_score

### Resumes Table
- id, filename, filepath, uploaded_at, match_score

## Configuration

### Security
- JWT secret key is set in `backend/auth.py` (change for production)
- Default token expiry: 24 hours
- Passwords hashed with bcrypt

### Database
- SQLite database located at `db/hrms.db`
- Automatically created on first run
- Use `seed_data.py` to reset with sample data

## Troubleshooting

### Backend won't start
- Check if port 8000 is available: `lsof -i :8000`
- Verify Python version: `python --version` (should be 3.8+)
- Reinstall dependencies: `pip install -r requirements.txt`

### Frontend won't start
- Check if port 8501 is available: `lsof -i :8501`
- Ensure backend is running first
- Try: `streamlit run app.py --server.port 8502` for different port

### Resume screening not working
- Check file formats (PDF, DOCX, TXT only)
- Ensure uploads directory exists: `mkdir -p uploads/resumes`
- Install missing packages: `pip install PyPDF2 python-docx`

### Database errors
- Delete and recreate: `rm db/hrms.db && python backend/seed_data.py`
- Check write permissions on `db/` directory

## Sample Data Summary

- **Employees**: 15 (1 Admin, 1 HR, 13 Employees)
- **Departments**: Engineering, HR, Sales, Marketing, Finance, Management
- **Attendance**: 22 working days for each employee
- **Performance**: 3 months of KPI data
- **Resumes**: 20 total (12 matching, 8 non-matching)

## Future Enhancements

- Email notifications for attendance/performance
- Advanced reporting and analytics
- Integration with GPT API for smarter chatbot
- Multi-company support
- Mobile app integration
- Real-time dashboard updates
- Document management system
- Leave request workflow

## Technologies Used

- **FastAPI**: Modern async web framework
- **Streamlit**: Interactive web UI
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database
- **scikit-learn**: Machine learning
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX text extraction
- **python-jose**: JWT tokens
- **passlib**: Password hashing
- **pandas**: Data manipulation
- **uvicorn**: ASGI server

## License

This project is open source and available for educational and commercial use.

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review API documentation at http://localhost:8000/docs
3. Check backend logs in terminal
4. Verify all dependencies are installed

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
