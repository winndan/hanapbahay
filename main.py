from fasthtml.common import *
from homepage.homepage import homepage
from monsterui.all import *
from auths.frontend.signup import signup_page
from auths.frontend.signin import signin_page
from dashboard.frontend.user import user_page
from auths.backend.signup import signup_account, check_password, check_confirm_password
from auths.backend.signin import signin_account
from dashboard.frontend.admin import dashboard
from testi import tests

app, rt = fast_app(hdrs=Theme.slate.headers(daisy=True), live=True)


# Frontend
@rt("/")
async def home():
    return homepage()

@rt("/signup")
async def get_signup_page():
    return signup_page()

@rt("/user")
async def get_user_dashboard():
    return user_page()


@rt("/signin")
async def get_signin_page():
    return signin_page()

@rt("/admin")
async def get_admin_page():
    return dashboard()



# Backend

@rt("/api/signup", methods="post")
async def post_signup_account(display_name: str, email: str, password: str, confirm_password: str):
    return await signup_account(display_name, email, password, confirm_password)

# 👉 Route for logging in the account
@rt("/api/signin", methods="post")
async def post_signin_account(email: str, password: str):
    return await signin_account(email, password)


@rt("/api/check-password")
async def get_check_password(password: str):
    return await check_password(password)

@rt("/api/check-confirm-password")
async def get_check_confirm_password(password: str, confirm_password: str):
    return await check_confirm_password(password, confirm_password)

# 👉 Route to handle email verification redirect
@rt("/api/handle-verify", methods="get")
async def handle_email_verification():
    return Script("window.location.href = '/dashboard/user';")


if __name__ == "__main__":
    serve()
