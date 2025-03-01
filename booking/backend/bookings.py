from fasthtml.common import *
from monsterui.all import *
from pydantic import BaseModel, Field, ValidationError
from uuid import uuid4
from db_connect import supabase
from datetime import date, datetime

# ✅ Pydantic Model for Booking Validation
class BookingData(BaseModel):
    room_id: str
    room_number: str
    guest_name: str = Field(..., min_length=1, max_length=100)
    guest_email: str = Field(..., pattern=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    guest_phone: str = Field(..., pattern=r"^\+?[0-9\- ]{10,15}$")
    check_in_date: date
    check_out_date: date
    number_of_guests: int = Field(..., gt=0)
    total_price: float = Field(..., gt=0)
    status: str = "Pending"  # ✅ Always starts as Pending
    payment_method: str = "eCash"  # ✅ Always eCash
    reference_number: str = Field(..., min_length=5, max_length=50)  # ✅ Required for eCash
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

async def book_room(req):
    try:
        form_data = await req.form()
        booking_data = dict(form_data)

        print("📝 Debug: Received Booking Data Before Processing:", booking_data)

        # ✅ Validate Required Fields
        required_fields = [
            "room_id", "room_number", "guest_name", "guest_email", "guest_phone",
            "check_in_date", "check_out_date", "number_of_guests", "reference_number"
        ]
        missing_fields = [field for field in required_fields if field not in booking_data or not booking_data[field]]

        if missing_fields:
            print("🚨 Error: Missing required fields:", missing_fields)
            return P(f"❌ Error: Missing required fields: {missing_fields}", cls=TextT.error, id="booking-status")

        # ✅ Convert Fields to Match Database Schema
        booking_data["number_of_guests"] = int(booking_data["number_of_guests"])
        check_in_date = date.fromisoformat(booking_data["check_in_date"])
        check_out_date = date.fromisoformat(booking_data["check_out_date"])

        # ✅ Validate Check-in & Check-out Dates
        if check_out_date <= check_in_date:
            print("❌ Error: Check-out date must be after check-in date!")
            return P("❌ Error: Check-out date must be after check-in date.", cls=TextT.error, id="booking-status")

        # ✅ Fetch `price_per_night` from Supabase
        room_response = supabase.table("rooms").select("price_per_night").eq("id", booking_data["room_id"]).execute()

        if not room_response.data:
            print("❌ Error: Room not found in database!")
            return P("❌ Error: Room not found!", cls=TextT.error, id="booking-status")

        price_per_night = float(room_response.data[0]["price_per_night"])  # ✅ Convert to FLOAT

        # ✅ Compute `total_price`
        booking_data["total_price"] = round(booking_data["number_of_guests"] * price_per_night, 2)

        booking_data["status"] = "Pending"  # ✅ Always "Pending"
        booking_data["payment_method"] = "eCash"  # ✅ Always "eCash"
        booking_data["created_at"] = datetime.now().isoformat()  # ✅ Ensure timestamp format
        booking_data["updated_at"] = datetime.now().isoformat()  # ✅ Ensure timestamp format

        print("📝 Debug: Processed Booking Data for Insert:", booking_data)

        # ✅ Insert into Supabase
        response = supabase.table("bookings").insert({
            "id": str(uuid4()),
            "room_id": booking_data["room_id"],
            "room_number": booking_data["room_number"],
            "guest_name": booking_data["guest_name"],
            "guest_email": booking_data["guest_email"],
            "guest_phone": booking_data["guest_phone"],
            "check_in_date": booking_data["check_in_date"],
            "check_out_date": booking_data["check_out_date"],
            "number_of_guests": booking_data["number_of_guests"],
            "total_price": booking_data["total_price"],  # ✅ Insert calculated total_price
            "status": booking_data["status"],
            "payment_method": booking_data["payment_method"],
            "reference_number": booking_data["reference_number"],
            "created_at": booking_data["created_at"],
            "updated_at": booking_data["updated_at"]
        }).execute()

        print("✅ Debug: Supabase Insert Response:", response)

        if response.data:
            print("✅ Booking Saved:", response.data)
            return P("✅ Booking Confirmed! Waiting for approval.", cls=TextT.success, id="booking-status")
        else:
            print("❌ Database Error: Booking not saved!")
            return P("❌ Booking Failed. Please try again.", cls=TextT.error, id="booking-status")

    except Exception as e:
        print("❌ Unexpected Error:", str(e))
        return P(f"❌ Error: {str(e)}", cls=TextT.error, id="booking-status")
