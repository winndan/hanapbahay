from fasthtml.common import *
from monsterui.all import *
from fasthtml.svg import *

# 👉 Frontend: Login page UI
def signin_page():
    Script(src="https://unpkg.com/htmx.org@2.0.4")

    left = Div(cls="col-span-1 hidden flex-col justify-between p-8 text-white lg:flex bg-cover bg-center bg-no-repeat",
               style="background-image: url('/assets/bg-auth.jpg');")(
        Div(cls=(TextT.bold))("Bukana Hotels"),
        Blockquote(cls="space-y-2")(
            P(cls=TextT.lg)("""Login to access your personalized experience and manage your bookings effortlessly."""),
            Footer(cls=TextT.sm)("Sign in now")))

    right = Div(cls="col-span-2 flex flex-col p-8 lg:col-span-1")(
        DivRAligned(Button("Back Home", cls=ButtonT.ghost, onclick="window.location.href='/';")),
        DivCentered(cls='flex-1')(
            Container(
                DivVStacked(
                    H3("Sign In"),
                    Small("Enter your credentials below to access your account", cls=TextT.muted)
                ),
                # 🔹 Form with HTMX Integration (Includes Loading Indicator)
                Form(method="post", action="/api/signin",
                     hx_post="/api/signin",
                     hx_trigger="submit",
                     hx_target="#toast-container",
                     hx_indicator="#loading-indicator",
                     hx_on="htmx:after-request: this.reset();")(
                    
                    Input(name="email", placeholder="name@example.com", type="email", required=True),
                    
                    Input(name="password", placeholder="Password", type="password", required=True),
                    
                    # 🔹 Loading Indicator (Hidden Initially)
                    Div(id="loading-indicator", cls="hidden text-center")(
                        Loading(cls=LoadingT.spinner, htmx_indicator=True)
                    ),

                    # 🔹 Submit Button
                    Button(
                        UkIcon('log-in', cls='mr-2'),
                        "Sign In", 
                        cls=(ButtonT.primary, "w-full"), 
                        type="submit"
                    ),

                    DividerSplit(Small("Or continue with"), cls=TextT.muted),
                    
                    Button(UkIcon('google', cls='mr-2'), "Google", cls=(ButtonT.default, "w-full")),
                    
                    cls='space-y-6'
                ),
                # 🔹 Toast Notification Container (For Success/Error Messages)
                Div(id="toast-container", cls="absolute top-5 right-5"),
                
                DivVStacked(Small(
                    "By signing in, you agree to our ",
                    A(cls=AT.muted, href="#terms")("Terms of Service"), " and ",
                    A(cls=AT.muted, href="#privacy")("Privacy Policy"), ".",
                    cls=(TextT.muted, "text-center"))),
                
                cls="space-y-6"
            )
        )
    )

    return Title("Auth Example"), Grid(left, right, cols=2, gap=0, cls='h-screen')