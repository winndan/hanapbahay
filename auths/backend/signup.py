from fasthtml.common import *
from db_connect import supabase
from monsterui.all import *
import re
from pydantic import BaseModel, EmailStr, ValidationError

# ✅ Password validation regex (8+ chars, 1 uppercase, 1 lowercase, 1 number, 1 special char)
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

# ✅ Pydantic Schema for Signup Validation
class SignupSchema(BaseModel):
    display_name: str
    email: EmailStr
    password: str
    confirm_password: str

# ✅ Success Toast
def ex_alerts2():
    return Alert("✅ Your account has been successfully created!", cls=AlertT.success)

# ✅ Error Toast
def ex_alerts3(message="An error occurred. Please try again."):
    return Alert(
        DivLAligned(UkIcon('triangle-alert'), 
                    P(f"❌ {message}")),
        cls=AlertT.error
    )

# ✅ Signup Function with Improved Error Handling
async def signup_account(display_name: str, email: str, password: str, confirm_password: str, session):
    try:
        # ✅ Validate input using Pydantic
        try:
            data = SignupSchema(
                display_name=display_name,
                email=email,
                password=password,
                confirm_password=confirm_password
            )
        except ValidationError as e:
            return ex_alerts3(f"Validation error: {e.errors()[0]['msg']}")

        # ✅ Validate password match
        if data.password != data.confirm_password:
            return ex_alerts3("Passwords do not match!")

        # ✅ Validate password strength
        if not re.fullmatch(PASSWORD_REGEX, data.password):
            return ex_alerts3("Weak password! Must contain 8+ characters, 1 uppercase, 1 lowercase, 1 number, and 1 special character.")

        print(f"🔍 Attempting to create user: {data.email}")

        # ✅ Perform user signup (Email confirmation required by Supabase)
        response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password,
            "options": {"data": {"display_name": data.display_name}}
        })

        print(f"🔍 Supabase Signup Full Response: {response}")  # ✅ Debugging response

        # ✅ Ensure signup was successful
        user = response.user
        if not user:
            print("🚨 ERROR: User object missing in response!")
            return ex_alerts3("Signup failed! Supabase did not return user details.")

        print(f"🟢 Signup Successful for: {user.email}")

        # ❌ REMOVE AUTO-LOGIN (Since email confirmation is required)
        print("🔴 Email confirmation required. Auto-login disabled.")

        # ✅ Show confirmation message instead of redirecting
        return [
            ex_alerts2(),
            Alert(
                DivLAligned(UkIcon('mail'), 
                            P(f"✅ Account created successfully! Please check {data.email} for a confirmation link.")),
                cls=AlertT.success
            ),
            Script("setTimeout(() => { window.location.replace('/signin'); }, 5000);")  # Redirect after 5 sec
        ]

    except Exception as e:
        print(f"❌ Exception in signup_account: {e}")
        return ex_alerts3(f"Unexpected error: {str(e)}")

# ✅ Check Password Strength
async def check_password(password: str):
    if not re.fullmatch(PASSWORD_REGEX, password):
        return Small(cls="text-red-500")("❌ Weak password! Must contain at least 8 characters, 1 uppercase, 1 lowercase, 1 number, and 1 special character.")
    return Small(cls="text-green-500")("✅ Strong password!")

# ✅ Check Password Confirmation
async def check_confirm_password(password: str, confirm_password: str):
    if password != confirm_password:
        return Small(cls="text-red-500")("❌ Passwords do not match!")
    return Small(cls="text-green-500")("✅ Passwords match.")
