from fasthtml.common import *
from monsterui.all import *
from db_connect import supabase
from dashboard.frontend.user import user_page

async def get_user_dashboard(req):
    """Retrieve user session and display the user dashboard."""
    
    print("Request Headers:", req.headers)  # Log headers
    print("Request Cookies:", req.cookies)  # Log cookies

    auth_header = req.headers.get("Authorization")
    token = None

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split("Bearer ")[1].strip()
    else:
        token = req.cookies.get("auth_token")  # Fallback to cookies

    if not token:
        print("🚨 No token found in request! Redirecting to signin.")
        return Redirect("/signin")

    try:
        # ✅ Fix: Remove `await`, as `supabase.auth.get_user(token)` is not async
        response = supabase.auth.get_user(token)

        if not response or not response.user:
            print("🚨 Invalid token! Redirecting to signin.")
            return Redirect("/signin")

        user_data = response.user
        display_name = user_data.user_metadata.get("display_name", "User")

        return user_page(display_name)  # ✅ Ensure display_name is passed

    except Exception as e:
        print("❌ Error fetching user data from Supabase:", e)
        return Redirect("/signin")
