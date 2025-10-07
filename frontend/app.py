import streamlit as st
import requests
import pandas as pd
from datetime import datetime, date
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

API_BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="HRMS", page_icon="👥", layout="wide")

# ------------------ Login Page ------------------
def login_page():
    st.title("🔐 HRMS Login")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### Sign in to continue")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", type="primary", use_container_width=True):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/auth/login",
                    json={"email": email, "password": password}
                )
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.token = data["access_token"]
                    st.session_state.role = data["role"]
                    st.session_state.employee_id = data["employee_id"]
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            except Exception as e:
                st.error(f"Login failed: {str(e)}")

        st.markdown("---")
        st.info("**Demo Credentials:**\n\n"
                "**Admin:** admin@company.com / admin123\n\n"
                "**HR:** hr@company.com / hr123\n\n"
                "**Employee:** john.doe@company.com / password123")

# ------------------ Helpers ------------------
def get_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}

# ------------------ Admin Dashboard ------------------
def admin_dashboard():
    st.title("👑 Admin Dashboard")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", "👥 Employees", "📅 Attendance", "📈 Performance", "🤖 AI Features"
    ])

    # -------- Overview Tab --------
    with tab1:
        st.header("System Overview")
        try:
            response = requests.get(f"{API_BASE_URL}/employees", headers=get_headers())
            if response.status_code == 200:
                employees = response.json()

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Employees", len(employees))

                departments = {}
                for emp in employees:
                    dept = emp.get("department", "Unknown")
                    departments[dept] = departments.get(dept, 0) + 1
                col2.metric("Departments", len(departments))

                avg_salary = sum(emp.get("salary", 0) for emp in employees) / len(employees) if employees else 0
                col3.metric("Avg Salary", f"${avg_salary:,.2f}")

                col4.metric("Active Today", len(employees))

                st.subheader("Department Distribution")
                if departments:
                    dept_df = pd.DataFrame(list(departments.items()), columns=["Department", "Count"])
                    st.bar_chart(dept_df.set_index("Department"))
        except Exception as e:
            st.error(f"Error loading overview: {str(e)}")

    # -------- Employees Tab --------
    with tab2:
        st.header("Employee Management")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Employee List")
            try:
                response = requests.get(f"{API_BASE_URL}/employees", headers=get_headers())
                if response.status_code == 200:
                    employees = response.json()
                    if employees:
                        df = pd.DataFrame(employees)
                        st.dataframe(df, use_container_width=True)
                        csv = df.to_csv(index=False)
                        st.download_button("📥 Export to CSV", csv, "employees.csv", "text/csv")
            except Exception as e:
                st.error(f"Error loading employees: {str(e)}")
        with col2:
            st.subheader("Add New Employee")
            with st.form("add_employee_form"):
                name = st.text_input("Name")
                email = st.text_input("Email")
                department = st.selectbox("Department", ["Engineering", "HR", "Sales", "Marketing", "Finance"])
                salary = st.number_input("Salary", min_value=0.0, step=1000.0)
                hire_date = st.date_input("Hire Date")
                role = st.selectbox("Role", ["Employee", "HR", "Admin"])
                password = st.text_input("Password", type="password")

                if st.form_submit_button("Add Employee"):
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/employees",
                            headers=get_headers(),
                            json={
                                "name": name,
                                "email": email,
                                "department": department,
                                "salary": salary,
                                "hire_date": hire_date.isoformat(),
                                "role": role,
                                "password": password
                            }
                        )
                        if response.status_code == 200:
                            st.success("Employee added successfully!")
                            st.rerun()
                        else:
                            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Error adding employee: {str(e)}")

    # -------- Attendance Tab --------
    with tab3:
        st.header("Attendance Management")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Attendance Records")
            try:
                response = requests.get(f"{API_BASE_URL}/attendance", headers=get_headers())
                if response.status_code == 200:
                    attendance = response.json()
                    if attendance:
                        df = pd.DataFrame(attendance)
                        st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Error loading attendance: {str(e)}")
        with col2:
            st.subheader("Mark Attendance")
            with st.form("mark_attendance_form"):
                response = requests.get(f"{API_BASE_URL}/employees", headers=get_headers())
                if response.status_code == 200:
                    employees = response.json()
                    employee_options = {f"{emp['name']} ({emp['id']})": emp['id'] for emp in employees}

                    selected_employee = st.selectbox("Employee", list(employee_options.keys()))
                    attendance_date = st.date_input("Date", value=date.today())
                    status = st.selectbox("Status", ["Present", "Absent", "Leave", "Half Day"])
                    hours = st.number_input("Hours Worked", min_value=0.0, max_value=12.0, value=8.0, step=0.5)

                    if st.form_submit_button("Mark Attendance"):
                        try:
                            response = requests.post(
                                f"{API_BASE_URL}/attendance",
                                headers=get_headers(),
                                json={
                                    "employee_id": employee_options[selected_employee],
                                    "date": attendance_date.isoformat(),
                                    "status": status,
                                    "hours_worked": hours
                                }
                            )
                            if response.status_code == 200:
                                st.success("Attendance marked!")
                                st.rerun()
                            else:
                                st.error("Error marking attendance")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")

    # -------- Performance Tab --------
    with tab4:
        st.header("Performance Management")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Performance Records")
            try:
                response = requests.get(f"{API_BASE_URL}/performance", headers=get_headers())
                if response.status_code == 200:
                    performance = response.json()
                    if performance:
                        df = pd.DataFrame(performance)
                        st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Error loading performance: {str(e)}")
        with col2:
            st.subheader("Add Performance Record")
            with st.form("add_performance_form"):
                response = requests.get(f"{API_BASE_URL}/employees", headers=get_headers())
                if response.status_code == 200:
                    employees = response.json()
                    employee_options = {f"{emp['name']} ({emp['id']})": emp['id'] for emp in employees}

                    selected_employee = st.selectbox("Employee", list(employee_options.keys()))
                    month = st.text_input("Month (e.g., 2024-01)")
                    kpi_score = st.slider("KPI Score", 0.0, 10.0, 5.0, 0.1)
                    attendance_pct = st.slider("Attendance %", 0.0, 100.0, 90.0, 1.0)

                    if st.form_submit_button("Add Record"):
                        try:
                            response = requests.post(
                                f"{API_BASE_URL}/performance",
                                headers=get_headers(),
                                json={
                                    "employee_id": employee_options[selected_employee],
                                    "month": month,
                                    "kpi_score": kpi_score,
                                    "attendance_percentage": attendance_pct
                                }
                            )
                            if response.status_code == 200:
                                st.success("Performance record added!")
                                st.rerun()
                            else:
                                st.error("Error adding record")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")

    # -------- AI Features Tab --------
    with tab5:
        ai_features_page()

# ------------------ HR Dashboard ------------------
def hr_dashboard():
    st.title("👔 HR Dashboard")
    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 Employees", "📅 Attendance", "📈 Performance", "🤖 AI Features"
    ])
    with tab1:
        st.header("Employee Management")
        try:
            response = requests.get(f"{API_BASE_URL}/employees", headers=get_headers())
            if response.status_code == 200:
                employees = response.json()
                if employees:
                    df = pd.DataFrame(employees)
                    st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading employees: {str(e)}")
    with tab2:
        st.header("Attendance Records")
        try:
            response = requests.get(f"{API_BASE_URL}/attendance", headers=get_headers())
            if response.status_code == 200:
                attendance = response.json()
                if attendance:
                    df = pd.DataFrame(attendance)
                    st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading attendance: {str(e)}")
    with tab3:
        st.header("Performance Records")
        try:
            response = requests.get(f"{API_BASE_URL}/performance", headers=get_headers())
            if response.status_code == 200:
                performance = response.json()
                if performance:
                    df = pd.DataFrame(performance)
                    st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading performance: {str(e)}")
    with tab4:
        ai_features_page()

# ------------------ Employee Dashboard ------------------
def employee_dashboard():
    st.title("👤 Employee Dashboard")
    employee_id = st.session_state.employee_id

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 My Info", "📅 My Attendance", "📈 My Performance", "💬 HR Chatbot"
    ])

    # -------- My Info Tab --------
    with tab1:
        st.header("My Information")
        try:
            response = requests.get(f"{API_BASE_URL}/employees/{employee_id}", headers=get_headers())
            if response.status_code == 200:
                employee = response.json()
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Name", employee["name"])
                    st.metric("Email", employee["email"])
                    st.metric("Department", employee["department"])
                with col2:
                    st.metric("Role", employee["role"])
                    st.metric("Hire Date", employee["hire_date"])
                    st.metric("Salary", f"${employee['salary']:,.2f}")
        except Exception as e:
            st.error(f"Error loading information: {str(e)}")

    # -------- My Attendance Tab --------
    with tab2:
        st.header("My Attendance")
        try:
            response = requests.get(
                f"{API_BASE_URL}/attendance?employee_id={employee_id}",
                headers=get_headers()
            )
            if response.status_code == 200:
                attendance = response.json()
                if attendance:
                    df = pd.DataFrame(attendance)
                    st.dataframe(df, use_container_width=True)
                    present_days = len([a for a in attendance if a["status"] == "Present"])
                    total_days = len(attendance)
                    attendance_pct = (present_days / total_days * 100) if total_days > 0 else 0
                    st.metric("Attendance Rate", f"{attendance_pct:.1f}%")
                else:
                    st.info("No attendance records found")
        except Exception as e:
            st.error(f"Error loading attendance: {str(e)}")

    # -------- My Performance Tab --------
    with tab3:
        st.header("My Performance")
        try:
            response = requests.get(
                f"{API_BASE_URL}/performance?employee_id={employee_id}",
                headers=get_headers()
            )
            if response.status_code == 200:
                performance = response.json()
                if performance:
                    df = pd.DataFrame(performance)
                    st.dataframe(df, use_container_width=True)
                    avg_kpi = sum(p["kpi_score"] for p in performance) / len(performance)
                    st.metric("Average KPI Score", f"{avg_kpi:.2f}")
                else:
                    st.info("No performance records found")
        except Exception as e:
            st.error(f"Error loading performance: {str(e)}")

    # -------- HR Chatbot Tab --------
    with tab4:
        st.subheader("💬 HR Chatbot")
        st.write("Chat about leave policies, payroll, benefits, and more")
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        # Only show history here, input handled outside tabs
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

# ------------------ AI Features Page ------------------
def ai_features_page():
    st.header("🤖 AI Features")

    ai_tab1, ai_tab2, ai_tab3 = st.tabs([
        "📄 Resume Screening", "📊 Performance Prediction", "💬 HR Chatbot"
    ])

    # Resume Screening Tab
    with ai_tab1:
        st.subheader("Resume Screening")
        st.write("Upload a Job Description and multiple resumes to find matching candidates")
        jd_file = st.file_uploader("Upload Job Description (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])
        resume_files = st.file_uploader("Upload Resumes (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"], accept_multiple_files=True)
        if st.button("Screen Resumes") and jd_file and resume_files:
            with st.spinner("Screening resumes..."):
                try:
                    import sys, os
                    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
                    from ml_models.resume_screening import get_top_matching_resumes

                    os.makedirs("uploads", exist_ok=True)
                    jd_path = f"uploads/temp_jd_{jd_file.name}"
                    with open(jd_path, "wb") as f:
                        f.write(jd_file.getbuffer())

                    resume_paths = []
                    os.makedirs("uploads/resumes", exist_ok=True)
                    for resume_file in resume_files:
                        resume_path = f"uploads/resumes/{resume_file.name}"
                        with open(resume_path, "wb") as f:
                            f.write(resume_file.getbuffer())
                        resume_paths.append(resume_path)

                    results = get_top_matching_resumes(jd_path, resume_paths)
                    if results:
                        st.success(f"Found {len(results)} matching resumes!")
                        df = pd.DataFrame(results)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.warning("No matching resumes found")
                    os.remove(jd_path)
                except Exception as e:
                    st.error(f"Error screening resumes: {str(e)}")

    # Performance Prediction Tab
    with ai_tab2:
        st.subheader("Performance Prediction")
        st.write("Train and predict employee performance based on KPI scores and attendance")
        if st.button("Train Model"):
            with st.spinner("Training performance prediction model..."):
                try:
                    import sys, numpy as np
                    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
                    from ml_models.performance_prediction import train_performance_model, save_model

                    response = requests.get(f"{API_BASE_URL}/performance", headers=get_headers())
                    if response.status_code == 200:
                        performance_data = response.json()
                        if len(performance_data) < 10:
                            st.warning("Need at least 10 performance records to train the model")
                        else:
                            X = np.array([[p["kpi_score"], p["attendance_percentage"]] for p in performance_data])
                            y = np.array([p["kpi_score"] * (p["attendance_percentage"] / 100) for p in performance_data])
                            model, metrics = train_performance_model(X, y)
                            save_model(model)
                            st.success("Model trained successfully!")
                            st.write(f"R² Score: {metrics['r2_score']:.4f}")
                            st.write(f"Mean Squared Error: {metrics['mse']:.4f}")
                except Exception as e:
                    st.error(f"Error training model: {str(e)}")

        st.markdown("---")
        st.write("**Predict Performance**")
        col1, col2 = st.columns(2)
        with col1:
            kpi_score = st.slider("KPI Score", 0.0, 10.0, 7.0, 0.1)
        with col2:
            attendance_pct = st.slider("Attendance %", 0.0, 100.0, 85.0, 1.0)
        if st.button("Predict"):
            try:
                import sys
                sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
                from ml_models.performance_prediction import load_model, predict_performance, prepare_features
                model = load_model()
                if model is None:
                    st.warning("Please train the model first")
                else:
                    features = prepare_features(kpi_score, attendance_pct)
                    prediction = predict_performance(model, features)
                    st.success(f"Predicted Performance Score: {prediction:.2f}")
            except Exception as e:
                st.error(f"Error making prediction: {str(e)}")

    # HR Chatbot Tab
    with ai_tab3:
        st.subheader("💬 HR Chatbot")
        st.write("Chat about leave policies, payroll, benefits, and more")
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

# ------------------ Chat Input (Outside Tabs) ------------------
def chatbot_input():
    user_input = st.chat_input("Ask a question...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    import sys, os
                    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
                    from ml_models.chatbot import get_chatbot_response
                    response = get_chatbot_response(user_input)
                    st.write(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
        st.experimental_rerun()

# ------------------ Main ------------------
def main():
    if "token" not in st.session_state:
        login_page()
    else:
        st.sidebar.title("🏢 HRMS")
        st.sidebar.write(f"**Role:** {st.session_state.role}")

        if st.sidebar.button("Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        if st.session_state.role == "Admin":
            admin_dashboard()
        elif st.session_state.role == "HR":
            hr_dashboard()
        else:
            employee_dashboard()

        # Chat input outside tabs/forms/columns
        chatbot_input()

if __name__ == "__main__":
    main()
