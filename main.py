#this is main.py
from fasthtml.common import *
from homepage.homepage import homepage
from monsterui.all import *
from auths.signup import signups
from testi import tests

app, rt = fast_app(hdrs=Theme.slate.headers(daisy=True))




@rt("/")
def home():
    return homepage()  # ✅ Calls the function once, without recursion

@rt("/signup")
def signup_page():
    return signups()  # ✅ Calls the function once, without recursion

@rt("/test")
def test_page():
    return tests()  # ✅ Calls the function once, without recursion


@rt("/debug")
def debug_page():
    return Div(cls="p-8 text-center bg-gray-100 h-screen")(
        H1("Debug Page"),
        P("If you see this, FastHTML is working!")
    )


if __name__ == "__main__":
    serve()


