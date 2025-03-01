from fasthtml.common import *
from monsterui.all import *
from db_connect import supabase, supabase_url

supa_url = supabase_url

# ✅ Fetch User's Bookings
def fetch_bookings(user_email):
    print(f"Fetching bookings for email: {user_email}")  # ✅ Debugging output
    response = supabase.table("bookings").select("*").eq("guest_email", user_email).execute()
    
    print(f"Supabase response: {response}")  # ✅ Check if response is received
    print(f"Fetched Bookings Data: {response.data}")  # ✅ Debug the actual bookings data

    return response.data if response and response.data else []


# ✅ Status Badge Colors
def booking_status_badge(status):
    status_colors = {
        "Pending": AlertT.warning,
        "Confirmed": AlertT.success,
        "Cancelled": AlertT.error
    }
    return Alert(status, cls=status_colors.get(status, AlertT.info))

# ✅ My Bookings Page
def bookings_page(display_name, email):
    print(f"Rendering My Bookings page for: {display_name} ({email})")  # ✅ Debugging output
    bookings = fetch_bookings(email)

    print(f"Bookings Retrieved: {bookings}")  # ✅ Debugging output to check fetched data
    

    return Container(
        NavBar(
            A("Rooms", href="/user"),
            A("My Bookings", href="/bookings"),
            DivRAligned(Button(UkIcon('log-out', cls='mr-2'), "Logout", cls="btn btn-danger px-4 py-2", onclick="window.location.href='/logout';")),
            brand=DivLAligned(H3("Bukana"), UkIcon('rocket', height=30, width=30)),
            sticky=True, uk_scrollspy_nav=True,
            scrollspy_cls=ScrollspyT.bold
        ),
        Container(
            DivCentered(H1(f"My Bookings, {display_name}!"), Subtitle("Here are your confirmed bookings."), id="bookings-section"),
            Section(H2("My Bookings"),
                Grid(*[
                    Card(
                        H4(f"Room {b['room_number']}"),
                        P(f"{b['check_in_date']} to {b['check_out_date']}"),
                        P(f"Guests: {b['number_of_guests']}"),
                        P(f"Total Price: ₱{b['total_price']}"),
                        P(f"Payment Method: {b['payment_method']}"),
                        booking_status_badge(b["status"]),  # ✅ Shows correct status

                        # ✅ Ensure this div exists for HTMX response
                        Div(id=f"booking-status-{b['id']}"),  

                        # Show "Cancel Booking" only if status is Pending
                        Div(cls="flex justify-end mt-2")(
                            Button("Cancel Booking", cls=ButtonT.destructive,  
                                hx_post=f"/api/cancel-booking?booking_id={b['id']}", 
                                hx_target=f"#booking-status-{b['id']}",  
                                hx_swap="outerHTML"
                            ) if b["status"] == "Pending" else ""
                        )
                    ) for b in bookings
                ])
            ),
            cls=(ContainerT.xl, 'uk-container-expand')
        )
    )
