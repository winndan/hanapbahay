from fasthtml.common import *
from homepage.homepage import homepage
from monsterui.all import *
from auths.frontend.signup import signup_page
from auths.frontend.signin import signin_page
from dashboard.user import user_page
from auths.backend.signup import signup_account, check_password, check_confirm_password
from auths.backend.signin import login_account
from testi import tests

app, rt = fast_app(hdrs=Theme.slate.headers(daisy=True), live=True)

@rt("/")
async def home():
    return homepage()

@rt("/signup")
async def get_signup_page():
    return signup_page()

@rt("/dashboard/user")
async def user_dashboard():
    return user_page()

@rt("/api/signup", methods="post")
async def post_signup_page(display_name: str, email: str, password: str, confirm_password: str):
    return await signup_account(display_name, email, password, confirm_password)

# 👉 Route for logging in the account
@rt("/api/signin", methods="post")
async def post_signin_page(email: str, password: str):
    return await login_account(email, password)


@rt("/api/check-password")
async def get_check_password(password: str):
    return await check_password(password)

@rt("/api/check-confirm-password")
async def get_check_confirm_password(password: str, confirm_password: str):
    return await check_confirm_password(password, confirm_password)

@rt("/signin")
async def get_signin_form():
    return signin_page()

# 👉 Route to handle email verification redirect
@rt("/api/handle-verify", methods="get")
async def handle_email_verification():
    return Script("window.location.href = '/dashboard/user';")


@rt("/test")
def test_page():
    return tests()

@rt("/debug")
def debug_page():
    return Div(cls="p-8 text-center bg-gray-100 h-screen")(
        H1("Debug Page"),
        P("If you see this, FastHTML is working!")
    )

if __name__ == "__main__":
    serve()
