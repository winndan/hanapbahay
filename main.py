import os
from fasthtml.common import *
from monsterui.all import *
from db_connect import supabase
from homepage.homepage import homepage
from auths.frontend.signup import signup_page
from auths.frontend.signin import signin_page
from dashboard.frontend.user import user_page
from auths.backend.signup import signup_account, check_password, check_confirm_password
from booking.backend.bookings import book_room


# ✅ Middleware to protect routes
def before(req, session):
    """Automatically check if the user is logged in before serving protected routes."""
    auth = req.scope['auth'] = session.get('user_id', None)
    if not auth:
        return RedirectResponse('/signin', status_code=303)  # Redirect if no user
bware = Beforeware(before, skip=['/', '/signin', '/signup', '/api/signin', '/api/signup'])

app, rt = fast_app(hdrs=Theme.slate.headers(daisy=True), live=True, before=bware)

# 🏠 Frontend Routes
@rt("/")
def home():
    return homepage()

@rt("/signup")
def get_signup_page():
    return signup_page()

@rt("/signin")
def get_signin_page():
    return signin_page()

@rt("/user")
def get_user_dashboard(auth, session):
    """Retrieve user session and display the user dashboard."""
    display_name = session.get("display_name", "User")
    return user_page(display_name)

# 🔒 Backend Authentication Routes
@rt("/api/signup")
def post_signup_account(display_name: str, email: str, password: str, confirm_password: str):
    return signup_account(display_name, email, password, confirm_password)

@rt("/api/signin")
def post_signin_account(email: str, password: str, session):
    """Handles user login and stores session information."""
    try:
        print("🔍 Step 1: Received login request for email:", email)

        if supabase is None:
            print("🚨 ERROR: Supabase client is not initialized!")
            return Script("window.location.href='/signin';")

        login_response = supabase.auth.sign_in_with_password({"email": email, "password": password})

        print("🔍 Step 2: Login Response:", login_response)

        if not login_response or not getattr(login_response, "user", None):
            print("🚨 ERROR: Invalid credentials!")
            return Script("window.location.href='/signin';")

        # ✅ Store session data
        user = login_response.user
        session["user_id"] = user.id
        session["display_name"] = user.user_metadata.get("display_name", "User")

        print("🟢 Step 3: User authenticated successfully:", user.email)

        # ✅ Fix: Use JavaScript to force full-page reload
        return Script("window.location.replace('/user');")

    except Exception as e:
        print("❌ Exception in signin_account:", e)
        return Script("window.location.href='/signin';")

@rt("/logout")
def logout(request, session):
    """Clears session and logs out user."""
    try:
        print("🔴 Logging out user:", session.get("user_id"))

        # ✅ Ensure session keys are removed
        session.pop("user_id", None)
        session.pop("display_name", None)

        print("🟢 Successfully logged out!")
        return RedirectResponse('/signin', status_code=303)

    except Exception as e:
        print("❌ Error in logout:", e)
        return Response("Internal Server Error", status_code=500)


@rt("/api/check-password")
def get_check_password(password: str):
    return check_password(password)

@rt("/api/check-confirm-password")
def get_check_confirm_password(password: str, confirm_password: str):
    return check_confirm_password(password, confirm_password)

# ✅ Handle Email Verification Redirect
@rt("/api/handle-verify")
def handle_email_verification():
    return RedirectResponse('/user', status_code=303)


# book room
# ✅ Route to Handle Room Booking
@rt("/api/book-room", methods="post")
async def post_book_room(request: Request):
    try:
        booking_data = await request.json()  # ✅ Get JSON data from request
        result = await book_room(booking_data)  # ✅ Call book_room function
        return result  # ✅ Return success or error message
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    serve()
