import os
from fasthtml.common import *
from monsterui.all import *
from db_connect import supabase
from homepage.homapageone import homepage
from auths.frontend.signup import signup_page
from auths.frontend.signin import signin_page
from dashboard.frontend.user import user_page
from auths.backend.signup import signup_account, check_password, check_confirm_password
from booking.frontend.bookings import bookings_page
import datetime
from datetime import datetime
import re




# ✅ Success Message Function
def ex_alerts2():
    return Alert("✅ Your booking has been confirmed!", cls=AlertT.success)

# ✅ Error Message Function
def ex_alerts3(message="Please enter a valid email."):
    return Alert(
        DivLAligned(
            UkIcon('triangle-alert'), 
            P(f"❌ {message}")
        ),
        cls=AlertT.error
    )

# ✅ Middleware to protect routes
def before(req, session):
    """Automatically check if the user is logged in before serving protected routes."""
    auth = req.scope['auth'] = session.get('user_id', None)
    if not auth:
        return RedirectResponse('/signin', status_code=303)  # Redirect if no user

skip_routes = [
    r'/',  # Home route
    r'/signin',
    r'/signup',
    r'/api/signin',
    r'/api/signup',
    r'/api/check-password',
    r'/api/check-confirm-password',
    r'/styles/.*',  # Allow all files under /styles/
    r'/assets/.*'   # Allow all files under /assets/
]

bware = Beforeware(
    before, 
    skip=skip_routes  # Pass the list directly
)


app, rt = fast_app(hdrs=Theme.slate.headers(daisy=True), live=True, before=bware)



# 🏠 Frontend Routes
@rt("/")
def home():
    return homepage()

@rt("/signup")
def get_signup_page():
    return signup_page()

@rt("/signin")
def get_signin_page():
    return signin_page()

@rt("/user")
def get_user_dashboard(auth, session):
    """Retrieve user session and display the user dashboard."""
    display_name = session.get("display_name", "User")
    user_email = session.get("email", "")
    return user_page(display_name, user_email)

# 🔒 Backend Authentication Routes
@rt("/api/signup", methods=["POST"])
async def api_signup(display_name: str, email: str, password: str, confirm_password: str, session):
    return await signup_account(display_name, email, password, confirm_password, session)

@rt("/api/signin")
def post_signin_account(email: str, password: str, session):
    """Handles user login and stores session information."""
    try:
        print("🔍 Step 1: Received login request for email:", email)

        if supabase is None:
            print("🚨 ERROR: Supabase client is not initialized!")
            return Script("window.location.href='/signin';")

        login_response = supabase.auth.sign_in_with_password({"email": email, "password": password})

        print("🔍 Step 2: Login Response:", login_response)

        if not login_response or not getattr(login_response, "user", None):
            print("🚨 ERROR: Invalid credentials!")
            return Script("window.location.href='/signin';")

        # ✅ Store session data
        user = login_response.user
        session["user_id"] = user.id
        session["display_name"] = user.user_metadata.get("display_name", "User")
        session["email"] = user.email  # ✅ Store the user's email

        print("🟢 Step 3: User authenticated successfully:", user.email)
        print("🟢 Stored in session:", session)  # ✅ Debugging session storage

        # ✅ Fix: Use JavaScript to force full-page reload
        return Script("window.location.replace('/user');")

    except Exception as e:
        print("❌ Exception in signin_account:", e)
        return Script("window.location.href='/signin';")

@rt("/logout")
def logout(request, session):
    """Clears session and logs out user."""
    try:
        print("🔴 Logging out user:", session.get("user_id"))

        # ✅ Ensure session keys are removed
        session.pop("user_id", None)
        session.pop("display_name", None)
        session.pop("email", None)  # Also clear email

        print("🟢 Successfully logged out!")
        return RedirectResponse('/signin', status_code=303)

    except Exception as e:
        print("❌ Error in logout:", e)
        return Response("Internal Server Error", status_code=500)

# ✅ Book Room Endpoint (Fixed version - single implementation)
@rt("/api/book-room", methods=["POST"])
async def handle_booking(req):
    try:
        form_data = await req.form()
        print(f"🔍 Received booking form data: {dict(form_data)}")  # Debug log
        
        guest_name = form_data.get("guest_name")
        guest_email = form_data.get("guest_email")
        guest_phone = form_data.get("guest_phone")
        room_id = form_data.get("room_id")
        room_number = form_data.get("room_number")
        check_in_date = form_data.get("check_in_date")
        check_out_date = form_data.get("check_out_date")
        number_of_guests = form_data.get("number_of_guests")
        reference_number = form_data.get("reference_number")
        modal_id = form_data.get("modal_id", room_id)  # Fallback to room_id if modal_id not provided

        # ✅ Ensure all fields are present
        if not all([guest_name, guest_email, guest_phone, room_id, room_number, check_in_date, check_out_date, number_of_guests, reference_number]):
            print("❌ Missing required fields")
            return ex_alerts3("All fields are required.")

        # ✅ Convert data types
        number_of_guests = int(number_of_guests)

        # ✅ Validate check-in & check-out dates
        try:
            check_in_date_obj = datetime.strptime(check_in_date, "%Y-%m-%d")
            check_out_date_obj = datetime.strptime(check_out_date, "%Y-%m-%d")
            if check_out_date_obj <= check_in_date_obj:
                return ex_alerts3("Check-out date must be after check-in date.")
        except ValueError:
            return ex_alerts3("Invalid date format.")

        # ✅ Calculate number of nights
        nights = (check_out_date_obj - check_in_date_obj).days

        # ✅ Fetch `price_per_night` from Supabase
        room_response = supabase.table("rooms").select("price_per_night").eq("id", room_id).execute()
        if not room_response.data:
            print(f"❌ Room not found: {room_id}")
            return ex_alerts3("Room not found.")

        price_per_night = float(room_response.data[0]["price_per_night"])
        total_price = round(number_of_guests * price_per_night * nights, 2)

        # ✅ Save booking to Supabase
        booking_data = {
            "guest_name": guest_name,
            "guest_email": guest_email,
            "guest_phone": guest_phone,
            "room_id": room_id,
            "room_number": room_number,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "number_of_guests": number_of_guests,
            "total_price": total_price,
            "status": "Confirmed",
            "payment_method": "eCash",
            "reference_number": reference_number
        }

        print(f"✅ Attempting to save booking: {booking_data}")
        response = supabase.table("bookings").insert(booking_data).execute()
        print(f"✅ Supabase response: {response}")

        # ✅ Ensure no error in booking
        if hasattr(response, "error") and response.error:
            print(f"❌ Booking error: {response.error}")
            return ex_alerts3(f"Booking failed: {response.error}")

        # ✅ Return success message and close modal
        return Div(
            Script(f"UIkit.modal('#modal-{room_number}').hide();"),  # ✅ Closes modal
            ex_alerts2(),  # ✅ Success message
            Script(f"""
                setTimeout(() => {{
                    if (document.querySelector("#booking-form-modal-{room_number}")) {{
                        document.querySelector("#booking-form-modal-{room_number} form").reset();
                        const totalPriceElem = document.querySelector("#total-price-modal-{room_number}");
                        if (totalPriceElem) totalPriceElem.innerHTML = "₱0.00";
                        const bookNowBtn = document.querySelector("#book-now-modal-{room_number}");
                        if (bookNowBtn) bookNowBtn.setAttribute("disabled", "true");
                    }}
                }}, 300);
            """)  # ✅ Clears form fields, resets total price & disables button
        )
    
    except Exception as e:
        print(f"❌ Exception in handle_booking: {str(e)}")
        return ex_alerts3(f"An error occurred: {str(e)}")
    
# ✅ Calculate Total Price (HTMX Triggered)
@rt("/api/calculate-total", methods=["POST"])
async def calculate_total(req):
    try:
        form_data = await req.form()
        print(f"🔍 Calculate total form data: {dict(form_data)}")  # Debug log
        
        room_id = form_data.get("room_id")
        number_of_guests = form_data.get("number_of_guests", "1")
        check_in_date = form_data.get("check_in_date")
        check_out_date = form_data.get("check_out_date")
        
        if not all([room_id, number_of_guests]):
            return Strong("₱0.00", id="total-price")

        number_of_guests = int(number_of_guests)
        
        # Calculate nights if dates are provided
        nights = 1
        if check_in_date and check_out_date:
            try:
                check_in_date_obj = datetime.strptime(check_in_date, "%Y-%m-%d")
                check_out_date_obj = datetime.strptime(check_out_date, "%Y-%m-%d")
                if check_out_date_obj > check_in_date_obj:
                    nights = (check_out_date_obj - check_in_date_obj).days
            except ValueError:
                pass
        
        # ✅ Fetch price_per_night from Supabase
        room_response = supabase.table("rooms").select("price_per_night").eq("id", room_id).execute()
        if not room_response.data:
            return ex_alerts3("Room not found.")

        price_per_night = float(room_response.data[0]["price_per_night"])
        total_price = round(number_of_guests * price_per_night * nights, 2)

        return Strong(f"₱{total_price}", id="total-price")

    except Exception as e:
        print(f"❌ Exception in calculate_total: {str(e)}")
        return Strong("₱0.00", id="total-price")

@rt("/api/check-password")
def get_check_password(password: str):
    return check_password(password)

@rt("/api/check-confirm-password")
def get_check_confirm_password(password: str, confirm_password: str):
    return check_confirm_password(password, confirm_password)

# ✅ Handle Email Verification Redirect
@rt("/api/handle-verify")
def handle_email_verification():
    return RedirectResponse('/user', status_code=303)

# ✅ Validate Reference Number (HTMX Triggered)
@rt("/api/validate-reference", methods=["POST"])
async def validate_reference(req):
    form_data = await req.form()
    reference_number = form_data.get("reference_number", "").strip()
    modal_id = form_data.get("modal_id", "")

    if not reference_number:
        return Button("Confirm Booking", cls=ButtonT.primary, type="submit", disabled=True, id=f"book-now-{modal_id}")

    return Button("Confirm Booking", cls=ButtonT.primary, type="submit", hx_post="/api/book-room", hx_target="#booking-status", hx_swap="outerHTML", id=f"book-now-{modal_id}")

@rt("/bookings")
def get_bookings_page(auth, session):
    display_name = session.get("display_name", "User")
    user_email = session.get("email", "")  # ✅ Retrieve email from session

    print(f"📌 Loading My Bookings for: {display_name} ({user_email})")  # ✅ Debugging output

    return bookings_page(display_name, user_email)

# ✅ Cancel Booking Endpoint
@rt("/api/cancel-booking", methods=["POST"])
async def cancel_booking(booking_id: str):
    try:
        # Update booking status to "Cancelled" in Supabase
        response = supabase.table("bookings").update({"status": "Cancelled"}).eq("id", booking_id).execute()
        
        if hasattr(response, "error") and response.error:
            return ex_alerts3("Cancellation failed. Please try again.")
            
        return Alert("Booking cancelled successfully", cls=AlertT.success)
    except Exception as e:
        print(f"❌ Error cancelling booking: {str(e)}")
        return ex_alerts3("An error occurred while cancelling your booking.")

if __name__ == "__main__":
    serve()