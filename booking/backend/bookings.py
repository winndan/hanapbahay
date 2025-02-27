from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from db_connect import supabase
import uuid

# ✅ Define Pydantic Model for Bookings (Fixed `pattern` instead of `regex`)
class Booking(BaseModel):
    room_id: uuid.UUID
    room_number: str = Field(..., min_length=1, max_length=50)
    guest_name: str = Field(..., min_length=1, max_length=100)
    guest_email: EmailStr
    guest_phone: str = Field(..., pattern=r'^\+?[0-9\- ]{10,15}$')  # ✅ Fixed pattern
    check_in_date: date
    check_out_date: date
    number_of_guests: int = Field(..., gt=0)
    total_price: float = Field(..., gt=0)
    status: str = Field(..., pattern="^(Pending|Confirmed|Cancelled|Completed)$")  # ✅ Fixed pattern
    payment_method: str = Field(..., pattern="^(Cash|eCash)$")  # ✅ Fixed pattern
    reference_number: str | None = None  # Only required if payment_method is eCash
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# ✅ Create Booking Function
async def book_room(booking_data: dict):
    try:
        # Validate input data with Pydantic
        booking = Booking(**booking_data)

        # ✅ Ensure reference_number is provided for eCash payments
        if booking.payment_method == "eCash" and not booking.reference_number:
            return {"error": "Reference number is required for eCash payments."}

        # ✅ Insert booking data into Supabase
        response = supabase.table("bookings").insert(booking.model_dump()).execute()  # ✅ Use `.model_dump()`

        if response.get("error"):
            return {"error": f"Database error: {response['error']}"}

        return {"success": "Room booked successfully!"}

    except Exception as e:
        return {"error": str(e)}
