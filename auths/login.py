
"""FrankenUI Auth Example built with MonsterUI (original design by ShadCN)"""

from fasthtml.common import *
from monsterui.all import *
from fasthtml.svg import *


def login():
    Script(src="https://unpkg.com/htmx.org@2.0.4")
      
    left = Div(cls="col-span-1 hidden flex-col justify-between p-8 text-white lg:flex bg-cover bg-center bg-no-repeat",
               style="background-image: url('/assets/bg-auth.jpg');")(
        Div(cls=(TextT.bold))("Bukana Hotels"),
        Blockquote(cls="space-y-2")(
            P(cls=TextT.lg)('"Get all the details – from bed size to views – so you know exactly what you’re booking. No surprises, just satisfaction."'),
            Footer(cls=TextT.sm)("Book Now")))

    right = Div(cls="col-span-2 flex flex-col p-8 lg:col-span-1")(
        DivRAligned(Button("back home", cls=ButtonT.ghost,
       onclick="window.location.href='/';")),
        DivCentered(cls='flex-1')(
            Container(
                DivVStacked(
                    H3("Create an account"),
                    Small("Enter your information below to create your account", cls=TextT.muted)),
                Form(
    Input(placeholder="name@example.com", type="email"),
    Input(placeholder="Password", type="password"),
    
    Button(
    UkIcon('mail', cls='mr-2'),  # Email icon instead of spinner
    "Sign in with Email", 
    cls=(ButtonT.primary, "w-full"), 
    disabled=True
),
    
    DividerSplit(Small("Or continue with"), cls=TextT.muted),
    
    Button(UkIcon('google', cls='mr-2'), "Google", cls=(ButtonT.default, "w-full")),
    
    cls='space-y-6'
)
,
                DivVStacked(Small(
                        "By clicking continue, you agree to our ",
                        A(cls=AT.muted, href="#demo")("Terms of Service")," and ",
                        A(cls=AT.muted, href="#demo")("Privacy Policy"),".",
                        cls=(TextT.muted,"text-center"))),
                cls="space-y-6")))
    
    return Title("Auth Example"),Grid(left,right,cols=2, gap=0,cls='h-screen')



