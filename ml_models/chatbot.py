import os
from typing import Optional

FAQ_DATABASE = {
    "leave": {
        "keywords": ["leave", "vacation", "time off", "pto", "sick", "holiday"],
        "response": "Leave Policy:\n- Annual Leave: 15 days per year\n- Sick Leave: 10 days per year\n- Public Holidays: 12 days per year\n- Apply for leave through the HRMS system at least 3 days in advance.\n- Medical certificate required for sick leave exceeding 3 consecutive days."
    },
    "payroll": {
        "keywords": ["payroll", "salary", "payment", "pay day", "compensation", "payslip"],
        "response": "Payroll Information:\n- Salary is paid on the last working day of each month\n- Payslips are available in the HRMS portal\n- Tax deductions are applied as per local regulations\n- Contact HR at hr@company.com for payroll queries"
    },
    "policy": {
        "keywords": ["policy", "policies", "rules", "regulations", "guidelines", "code of conduct"],
        "response": "Company Policies:\n- Working Hours: 9 AM - 6 PM, Monday to Friday\n- Dress Code: Business casual\n- Remote Work: Available with manager approval\n- Performance Reviews: Conducted quarterly\n- Full policy documents available on the company intranet"
    },
    "benefits": {
        "keywords": ["benefit", "benefits", "insurance", "health", "medical", "pension"],
        "response": "Employee Benefits:\n- Health Insurance: Comprehensive coverage for employee and family\n- Retirement Plan: 401(k) with company matching\n- Life Insurance: 2x annual salary coverage\n- Professional Development: Annual training budget\n- Contact benefits@company.com for detailed information"
    },
    "onboarding": {
        "keywords": ["onboarding", "joining", "new employee", "first day", "orientation"],
        "response": "Onboarding Process:\n- First day orientation at 9 AM\n- IT equipment setup on day 1\n- Complete HR paperwork within first week\n- Buddy program assigned for first 30 days\n- Training schedule provided by your manager"
    },
    "contact": {
        "keywords": ["contact", "reach", "email", "phone", "support"],
        "response": "HR Contact Information:\n- Email: hr@company.com\n- Phone: +1-555-0123\n- Office Hours: 9 AM - 5 PM, Monday to Friday\n- Emergency Contact: +1-555-0911 (24/7)"
    }
}

def get_chatbot_response(user_input: str) -> str:
    user_input_lower = user_input.lower()

    for category, data in FAQ_DATABASE.items():
        for keyword in data["keywords"]:
            if keyword in user_input_lower:
                return data["response"]

    return (
        "I'm sorry, I couldn't find specific information about that. "
        "Here are some topics I can help with:\n"
        "- Leave and time off policies\n"
        "- Payroll and salary information\n"
        "- Company policies and guidelines\n"
        "- Employee benefits\n"
        "- Onboarding process\n"
        "- HR contact information\n\n"
        "Please rephrase your question or contact HR directly at hr@company.com"
    )

def chatbot_with_gpt(user_input: str, api_key: Optional[str] = None) -> str:
    if not api_key:
        return get_chatbot_response(user_input)

    try:
        import openai
        openai.api_key = api_key

        system_prompt = (
            "You are an HR assistant chatbot. Answer questions about leave policies, "
            "payroll, company policies, benefits, and onboarding. Be helpful and professional. "
            "If you don't know something, direct the user to contact HR at hr@company.com"
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            max_tokens=300
        )

        return response.choices[0].message.content
    except Exception as e:
        return get_chatbot_response(user_input)
