from fasthtml.common import *
from monsterui.core import Theme
from monsterui.all import *

app, rt = fast_app(hdrs=Theme.slate.headers(daisy=True))

# ✅ Route to render buttons
@rt("/")
def home():
    return Div(cls="p-8 space-y-4")(
        H1("HTMX Dynamic Buttons", cls="text-2xl font-bold"),
        Button("Click to Load Message", 
            cls=ButtonT.primary, 
            hx_get="/message",       # ✅ Fetches data from `/message`
            hx_target="#output",     # ✅ Updates the `#output` div
            hx_swap="innerHTML"      # ✅ Only replaces the content inside `#output`
        ),
        Div(id="output", cls="mt-4 p-4 border rounded")  # ✅ This will be dynamically updated
    )

# ✅ Route to return dynamic content when the button is clicked
@rt("/message")
def message():
    return Div(cls="text-green-600 font-semibold")(
        "Hello! This content was loaded dynamically using HTMX. 🚀"
    )

serve()
