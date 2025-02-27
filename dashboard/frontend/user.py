from fasthtml.common import *
from monsterui.all import *
import uuid
import json
from db_connect import supabase
from booking.backend.bookings import book_room  # ✅ Import book_room

# ✅ Fetch Rooms from Supabase
def fetch_rooms():
    response = supabase.table("rooms").select("id, room_number, room_type, description, max_guests, status, price_per_night, image_id").execute()
    return response.data if response else []

# ✅ Generate Room Cards
def RoomCard(room):
    modal_id = f"modal-{room['room_number']}"  # Unique modal ID for each room
    
    # ✅ Supabase Storage Public URL (Modify with your bucket name)
    SUPABASE_BUCKET_URL = "https://your-project-id.supabase.co/storage/v1/object/public/room-images/"
    
    # ✅ Construct Image URL
    image_url = f"{SUPABASE_BUCKET_URL}{room['image_id']}" if room["image_id"] else "/default-room.jpg"

    return Div(
        Card(
            Img(src=image_url, cls="w-full h-64 object-cover rounded-t-lg"),  # ✅ Use correct image URL
            DivFullySpaced(H4(f"Room {room['room_number']}"), P(Strong(f"₱{room['price_per_night']} per night"), cls=TextT.sm)), 
            Button(
                "Details",
                cls=(ButtonT.primary, "w-full"),  # ✅ MonsterUI ButtonT.primary
                data_uk_toggle=f"#{modal_id}"  # ✅ Ensures button triggers modal
            )
        ),
        # 🔹 Room Details Modal
        Div(
            Modal(
                ModalTitle(f"Room {room['room_number']} Details"),
                Img(src=image_url, cls="w-full h-64 object-cover rounded-lg"),  # ✅ Display image inside modal
                P(f"Type: {room['room_type']}", cls=TextPresets.muted_sm),
                P(f"Description: {room['description']}", cls=TextPresets.muted_sm),
                P(f"Max Guests: {room['max_guests']}", cls=TextPresets.muted_sm),
                P(f"Status: {room['status']}", cls=TextPresets.muted_sm),
                P(f"Price: ₱{room['price_per_night']} per night", cls=TextPresets.muted_sm),

                Div(cls="flex justify-center space-x-4 mt-4")(
                    ModalCloseButton("Close", cls=ButtonT.secondary),  # ✅ MonsterUI ButtonT.secondary
                    Button("Book Now", cls=ButtonT.primary, onclick=f"bookRoom('{room['room_number']}')")  # ✅ MonsterUI ButtonT.primary
                ),
                id=modal_id
            ),
            data_uk_modal=""  # ✅ Ensures UIkit modal works
        )
    )


# ✅ User Dashboard
def user_page(display_name):
    rooms = fetch_rooms()

    return Container(
        NavBar(
            A("Welcome", href="#welcome-section"),
            A("Rooms", href="#rooms-section"),
            DivRAligned(Button(UkIcon('log-out', cls='mr-2'), "Logout", cls="btn btn-error px-4 py-2", onclick="window.location.href='/logout';")),
            brand=DivLAligned(H3("Bukana"), UkIcon('rocket', height=30, width=30)),
            sticky=True, uk_scrollspy_nav=True,
            scrollspy_cls=ScrollspyT.bold
        ),
        Container(
            DivCentered(H1(f"Welcome, {display_name}!"), Subtitle("Explore our rooms."), id="welcome-section"),
            Section(H2("Rooms"), Grid(*[RoomCard(room) for room in rooms], cols_lg=2), id="rooms-section"),
            cls=(ContainerT.xl, 'uk-container-expand')
        )
    )
