from fasthtml.common import *  # ✅ Already imported
from monsterui.all import *
from db_connect import supabase

async def signin_account(email: str, password: str):
    try:
        print("🔍 Step 1: Received login request for email:", email)

        # ✅ Ensure Supabase client exists
        if supabase is None:
            print("🚨 ERROR: Supabase client is not initialized!")
            return ex_alerts3("Internal error: Database not connected!")

        # ✅ Attempt login
        login_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        print("🔍 Step 2: Login Response:", login_response)

        # ✅ Check if Supabase returned any response
        if login_response is None:
            print("🚨 ERROR: Supabase returned None for login!")
            return ex_alerts3("Supabase error: No response from authentication.")

        # ✅ Ensure response contains a user
        user = getattr(login_response, "user", None)
        if user is None:
            print("🚨 ERROR: Supabase login response is missing user data!")
            return ex_alerts3("Invalid email or password!")

        print("🟢 Step 3: User authenticated successfully:", user.email)

        # ✅ Check if the user has confirmed their email
        if not getattr(user, "confirmed_at", None):
            print("🚨 ERROR: Email not confirmed!")
            return ex_alerts3("Please confirm your email before logging in.")

        # ✅ Extract session and access token
        session = getattr(login_response, "session", None)
        if session is None:
            print("🚨 ERROR: No session returned from Supabase!")
            return ex_alerts3("Error: No session found!")

        access_token = getattr(session, "access_token", None)
        if not access_token:
            print("🚨 ERROR: No access token returned!")
            return ex_alerts3("Error: Access token not found!")

        print("🟢 Step 4: Access token retrieved.")

        # ✅ Show success Toast & redirect after 2 seconds
        response = Response(
            Div(
                ex_alerts2("✅ Login successful! Redirecting..."),
                Script(f"""
                    setTimeout(function() {{
                        document.cookie = 'auth_token={access_token}; path=/; Secure;';
                        window.location.href='/user';
                    }}, 2000);
                """)
            ),
            status_code=200
        )

        print("🟢 Step 5: Response sent successfully.")
        return response

    except Exception as e:
        print("❌ Exception in signin_account:", e)
        return ex_alerts3(f"Error: {str(e)}")
