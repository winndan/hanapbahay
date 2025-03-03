from fasthtml.common import *
from monsterui.all import *
from db_connect import supabase, supabase_url

supa_url = "https://yfswjewyxnrrifsvvewq.supabase.co"

# ✅ Fetch Rooms from Supabase
def fetch_rooms():
    response = supabase.table("rooms").select(
        "id, room_number, room_type, description, max_guests, status, price_per_night, image_id"
    ).execute()
    print(f"Fetched Rooms: {response.data}")  # ✅ Debugging
    return response.data if response and response.data else []

# ✅ Fetch User's Bookings
def fetch_bookings(user_email):
    response = supabase.table("bookings").select("*").filter("guest_email", "eq", user_email).execute()
    print(f"Fetched Bookings for {user_email}: {response.data}")  # ✅ Debugging
    return response.data if response and response.data else []

# ✅ Status Badge Colors
def booking_status_badge(status):
    status_colors = {
        "Pending": AlertT.warning,
        "Confirmed": AlertT.success,
        "Cancelled": AlertT.error
    }
    return Alert(status, cls=status_colors.get(status, AlertT.info))

# ✅ Room Card Component
# ✅ Room Card Component
def RoomCard(room, display_name, email):
    modal_id = f"modal-{room['room_number']}"  
    SUPABASE_BUCKET_URL = f"{supa_url}/storage/v1/object/public/room-images/room_images"

    # Debugging prints
    print(f"Supabase URL: {supa_url}")
    print(f"Image ID: {room.get('image_id')}")
    
    # Ensure image_id is correctly assigned
    image_url = f"{SUPABASE_BUCKET_URL}/{room['image_id']}" if room.get("image_id") else "/default-room.jpg"
    
    print(f"Generated Image URL: {image_url}")  # Debugging URL

    return Div(
        Card(
            Img(src=image_url, cls="w-full h-64 object-cover rounded-t-lg"),
            DivFullySpaced(
                H4(f"Room {room['room_number']}"),
                P(Strong(f"₱{room['price_per_night']} per guest"), cls=TextT.sm)
            ), 
            Button("Details", cls=(ButtonT.primary, "w-full"), data_uk_toggle=f"#{modal_id}")
        ),
        RoomDetailsModal(room, modal_id, display_name, email, image_url)
    )


# ✅ Room Details Modal
def RoomDetailsModal(room, modal_id, display_name, email, image_url):
    return Div(
        Modal(
            ModalTitle(f"Room {room['room_number']} Details"),
            Img(src=image_url, cls="w-full h-64 object-cover rounded-lg"),
            P(f"Type: {room['room_type']}", cls=TextPresets.muted_sm),
            P(f"Description: {room['description']}", cls=TextPresets.muted_sm),
            P(f"Max Guests: {room['max_guests']}", cls=TextPresets.muted_sm),
            P(f"Status: {room['status']}", cls=TextPresets.muted_sm),
            P(f"Price: ₱{room['price_per_night']} per guest", cls=TextPresets.muted_sm),
            BookingForm(room, modal_id, display_name, email),
            id=modal_id
        ),
        data_uk_modal=""
    )

# ✅ Booking Form with Disabled Confirm Button
def BookingForm(room, modal_id, display_name, email):
    return Div(id=f"booking-form-{modal_id}")(
        Form(
            Fieldset(
                *[Input(name=field, type="hidden", value=value) for field, value in {
                    "guest_name": display_name, 
                    "guest_email": email, 
                    "payment_method": "eCash",
                    "room_id": room["id"], 
                    "room_number": room["room_number"], 
                    "price_per_night": room["price_per_night"],
                    "modal_id": modal_id  # Add this line to include modal_id in form data
                }.items()],
                Label("Phone", Input(name="guest_phone", type="tel", pattern="\+?[0-9\- ]{10,15}", required=True)),
                Label("Check-in Date", 
                     Input(name="check_in_date", 
                           type="date", 
                           required=True,
                           hx_trigger="change",
                           hx_post="/api/calculate-total",
                           hx_target=f"#total-price-{modal_id}",
                           hx_include=f"#booking-form-{modal_id} form")),
                Label("Check-out Date", 
                     Input(name="check_out_date", 
                           type="date", 
                           required=True,
                           hx_trigger="change",
                           hx_post="/api/calculate-total",
                           hx_target=f"#total-price-{modal_id}",
                           hx_include=f"#booking-form-{modal_id} form")),
                Label("Number of Guests", 
                    Input(name="number_of_guests", 
                          type="number", 
                          min="1", 
                          max=str(room["max_guests"]),
                          value="1",
                          required=True, 
                          hx_post="/api/calculate-total", 
                          hx_target=f"#total-price-{modal_id}",
                          hx_swap="outerHTML",
                          hx_include=f"#booking-form-{modal_id} form"
                    )
                ),
                
                # ✅ Total Price (Auto-calculated)
                P("Total Price: ", Strong("₱0.00", id=f"total-price-{modal_id}"), cls=TextT.success),

                # ✅ Reference Number with OnInput event to Enable Confirm Button
                Label("Reference Number",
                    Input(name="reference_number", 
                          type="text", 
                          required=True, 
                          id=f"ref-num-{modal_id}",
                          oninput=f"enableBookingButton('{modal_id}')")
                ),
            ),
            BookingFormActions(modal_id)
        ),
        Div(id=f"booking-success-{modal_id}")  # ✅ Where the success message will appear
    )

# ✅ Booking Form Actions with Disabled Confirm Button
def BookingFormActions(modal_id):
    return Div(cls="flex justify-center space-x-4 mt-4")(
        ModalCloseButton("Close", cls=ButtonT.secondary),
        Button("Confirm Booking", 
               cls=ButtonT.primary, 
               type="submit",
               hx_post="/api/book-room",
               hx_target=f"#booking-success-{modal_id}",  
               hx_swap="innerHTML",
               hx_include=f"#booking-form-{modal_id} form",  # Include all form data
               id=f"book-now-{modal_id}",
               disabled=True)  # ✅ Initially Disabled
    )

# ✅ JavaScript to Enable/Disable Button
def enable_booking_button_script():
    return Script("""
        function enableBookingButton(modalId) {
            const refInput = document.getElementById(`ref-num-${modalId}`);
            const bookBtn = document.getElementById(`book-now-${modalId}`);
            if (refInput && bookBtn) {
                bookBtn.disabled = !refInput.value.trim();  // Enable only if not empty
            }
        }
    """)

# ✅ Booking Card
def BookingCard(booking):
    booking_id = f"booking-status-{booking['id']}"  
    return Card(
        H4(f"Room {booking['room_number']}"),
        P(f"Check-in: {booking['check_in_date']}"),
        P(f"Check-out: {booking['check_out_date']}"),
        P(f"Guests: {booking['number_of_guests']}"),
        P(f"Total Price: ₱{booking['total_price']}"),
        P(f"Payment Method: {booking['payment_method']}"),
        booking_status_badge(booking["status"]),
        Div(id=booking_id),  
        Div(cls="flex justify-end mt-2")(
            Button("Cancel Booking", cls=ButtonT.destructive,  
                   hx_post=f"/api/cancel-booking?booking_id={booking['id']}", 
                   hx_target=f"#{booking_id}",  
                   hx_swap="outerHTML") if booking["status"] == "Pending" else ""
        )
    )

# ✅ User Dashboard
def user_page(display_name, email):
    rooms = fetch_rooms()
    return Container(
        enable_booking_button_script(),  # ✅ Include JavaScript function
        NavBar(
            A("Welcome", href="#welcome-section"),
            A("Rooms", href="#rooms-section"),
            A("My Bookings", href="/bookings"),  
            DivRAligned(Button(UkIcon('log-out', cls='mr-2'), "Logout", cls="btn btn-danger px-4 py-2", onclick="window.location.href='/logout';")),
            brand=DivLAligned(H3("Bukana"), UkIcon('rocket', height=30, width=30)),
            sticky=True, uk_scrollspy_nav=True, scrollspy_cls=ScrollspyT.bold
        ),
        Container(
            DivCentered(H1(f"Welcome, {display_name}!"), Subtitle("Explore our rooms."), id="welcome-section"),
            Section(H2("Rooms"), Grid(*[RoomCard(room, display_name, email) for room in rooms], cols_lg=2), id="rooms-section"),
            cls=(ContainerT.xl, 'uk-container-expand')
        )
    )
