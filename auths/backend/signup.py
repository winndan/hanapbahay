from fasthtml.common import *
from db_connect import supabase
import re

# Password validation regex (8+ chars, 1 uppercase, 1 lowercase, 1 number, 1 special char)
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

# 👉 Toast Notification Function
def add_toast(message: str, status: str):
    toast_colors = {
        "success": "text-green-500 bg-green-100 border border-green-400",
        "error": "text-red-500 bg-red-100 border border-red-400",
        "warning": "text-yellow-500 bg-yellow-100 border border-yellow-400",
        "info": "text-blue-500 bg-blue-100 border border-blue-400"
    }
    return Div(cls=f"p-4 rounded-md {toast_colors.get(status, 'bg-gray-100')} p-3",
               id="toast-container")(
        P(message, cls="font-medium")
    )

async def signup_account(display_name: str, email: str, password: str, confirm_password: str):
    try:
        if password != confirm_password:
            return add_toast("❌ Error: Passwords do not match!", "error")

        if not re.match(PASSWORD_REGEX, password):
            return add_toast("❌ Error: Weak password!", "error")

        # 👉 Show loading indicator
        loading_indicator = Script("document.getElementById('loading-indicator').classList.remove('hidden');")

        # 👉 Perform user signup (Ensure `display_name` is stored correctly)
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {"data": {"display_name": display_name}}  # Ensure metadata is included
        })

        # 👉 Hide loading indicator after process
        hide_loading_indicator = Script("document.getElementById('loading-indicator').classList.add('hidden');")

        # 👉 Check for signup errors
        if not response.user:
            return [
                hide_loading_indicator,
                add_toast("❌ Error: Signup failed! Please try again.", "error")
            ]

        # 👉 Retrieve user details to ensure metadata is updated
        user = supabase.auth.get_user()
        retrieved_display_name = user.user_metadata.get("display_name", "") if user and user.user_metadata else ""

        # 👉 Clear form fields after successful signup
        return [
            hide_loading_indicator,
            add_toast(f"✅ Welcome, {retrieved_display_name}! Please verify your email.", "success"),
            Script("document.querySelector('form').reset();")
        ]

    except Exception as e:
        error_message = str(e).lower()
        if "user already registered" in error_message or "email already exists" in error_message:
            return add_toast("❌ Error: Email already exists! Please try another email.", "error")
        return add_toast(f"❌ Error: {str(e)}", "error")

async def check_password(password: str):
    if not re.match(PASSWORD_REGEX, password):
        return Small(cls="text-red-500")("❌ Weak password!")
    return Small(cls="text-green-500")("✅ Strong password!")

async def check_confirm_password(password: str, confirm_password: str):
    if password != confirm_password:
        return Small(cls="text-red-500")("❌ Passwords do not match!")
    return Small(cls="text-green-500")("✅ Passwords match.")
