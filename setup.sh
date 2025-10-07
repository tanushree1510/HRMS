#!/bin/bash

echo "=========================================="
echo "HRMS Setup Script"
echo "=========================================="

echo ""
echo "Step 1: Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "Step 2: Creating necessary directories..."
mkdir -p db
mkdir -p uploads/resumes
mkdir -p ml_models

echo ""
echo "Step 3: Seeding database with sample data..."
cd backend
python seed_data.py
cd ..

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To start the application:"
echo ""
echo "1. Start Backend (Terminal 1):"
echo "   cd backend && uvicorn main:app --reload"
echo ""
echo "2. Start Frontend (Terminal 2):"
echo "   cd frontend && streamlit run app.py"
echo ""
echo "3. Login at http://localhost:8501"
echo "   Admin: admin@company.com / admin123"
echo ""
echo "=========================================="
