"""FrankenUI Auth Example built with MonsterUI (original design by ShadCN)"""

from fasthtml.common import *
from monsterui.all import *
from fasthtml.svg import *

def signup_page():
    Script(src="https://unpkg.com/htmx.org@2.0.4")

    left = Div(cls="col-span-1 hidden flex-col justify-between p-8 text-white lg:flex bg-cover bg-center bg-no-repeat",
               style="background-image: url('/assets/bg-auth.jpg');")(
        Div(cls=(TextT.bold))("Bukana Hotels"),
        Blockquote(cls="space-y-2")(
            P(cls=TextT.lg)('"Get all the details – from bed size to views – so you know exactly what you’re booking. No surprises, just satisfaction."'),
            Footer(cls=TextT.sm)("Book Now")))

    right = Div(cls="col-span-2 flex flex-col p-8 lg:col-span-1")(
        DivRAligned(Button("Back Home", cls=ButtonT.ghost, onclick="window.location.href='/';")),
        DivCentered(cls='flex-1')(
            Container(
                DivVStacked(
                    H3("Create an Account"),
                    Small("Enter your information below to create your account", cls=TextT.muted)
                ),
                # 🔹 Form with HTMX Integration (Includes Loading Indicator)
                Form(method="post", action="/api/signup",
                     hx_post="/api/signup",
                     hx_trigger="submit",
                     hx_target="#toast-container",
                     hx_indicator="#loading-indicator",
                     hx_on="htmx:after-request: this.reset();")(
                    
                    Input(name="display_name", placeholder="Display Name", type="text", required=True),                
                    Input(name="email", placeholder="name@example.com", type="email", required=True),
                    
                    Input(name="password", placeholder="Password", type="password", required=True, 
                          hx_get="/api/check-password", hx_target="#password-feedback", hx_trigger="keyup"),
                    Small(id="password-feedback"),

                    Input(name="confirm_password", placeholder="Confirm Password", type="password", required=True, 
                          hx_get="/api/check-confirm-password", hx_target="#confirm-password-feedback", 
                          hx_trigger="keyup", hx_include="[name='password']"),
                    Small(id="confirm-password-feedback"),

                    # 🔹 Loading Indicator (Hidden Initially)
                    Div(id="loading-indicator", cls="hidden text-center")(
                        Loading(cls=LoadingT.spinner, htmx_indicator=True)
                    ),

                    # 🔹 Submit Button
                    Button(
                        UkIcon('mail', cls='mr-2'),
                        "Sign Up with Email", 
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
                    "By clicking continue, you agree to our ",
                    A(cls=AT.muted, href="#terms")("Terms of Service"), " and ",
                    A(cls=AT.muted, href="#privacy")("Privacy Policy"), ".",
                    cls=(TextT.muted, "text-center"))),
                
                cls="space-y-6"
            )
        )
    )

    return Title("Auth Example"), Grid(left, right, cols=2, gap=0, cls='h-screen')
