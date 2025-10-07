#!/bin/bash

echo "Starting HRMS Backend Server..."
cd backend
uvicorn main:app --reload
