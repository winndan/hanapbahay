from fasthtml.common import *
from db_connection import supabase
import re

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

# 👉 Backend: Handle login request
async def signin_account(email: str, password: str):
    try:
        # 👉 Show loading indicator
        loading_indicator = Script("document.getElementById('loading-indicator').classList.remove('hidden');")
        
        # 👉 Perform user login
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        # 👉 Hide loading indicator after process
        hide_loading_indicator = Script("document.getElementById('loading-indicator').classList.add('hidden');")

        # 👉 Check for login errors
        if not response.user:
            return [
                hide_loading_indicator,
                add_toast("❌ Error: Invalid email or password!", "error")
            ]

        # 👉 Redirect to dashboard upon successful login
        return [
            hide_loading_indicator,
            add_toast("✅ Login successful! Redirecting...", "success"),
            Script("window.location.href = '/user';")
        ]
    
    except Exception as e:
        return add_toast(f"❌ Error: {str(e)}", "error")
