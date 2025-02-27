from fasthtml.common import *  # ✅ Already imported
from monsterui.all import *
from db_connect import supabase

async def signin_account(email: str, password: str):
    try:
        print("🔍 Step 1: Received login request for email:", email)

        # ✅ Ensure Supabase client exists
        if supabase is None:
            print("🚨 ERROR: Supabase client is not initialized!")
            return Div(Alert("❌ Internal error: Database not connected!", cls=AlertT.error))

        # ✅ Attempt login
        login_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        print("🔍 Step 2: Login Response:", login_response)

        # ✅ Check if Supabase returned any response
        if login_response is None:
            print("🚨 ERROR: Supabase returned None for login!")
            return Div(Alert("❌ Supabase error: No response from authentication.", cls=AlertT.error))

        # ✅ Ensure response contains a user
        user = getattr(login_response, "user", None)
        if user is None:
            print("🚨 ERROR: Supabase login response is missing user data!")
            return Div(Alert("❌ Invalid email or password!", cls=AlertT.error))

        print("🟢 Step 3: User authenticated successfully:", user.email)

        # ✅ Extract session and access token
        session = getattr(login_response, "session", None)
        if session is None:
            print("🚨 ERROR: No session returned from Supabase!")
            return Div(Alert("❌ Error: No session found!", cls=AlertT.error))

        access_token = getattr(session, "access_token", None)
        if not access_token:
            print("🚨 ERROR: No access token returned!")
            return Div(Alert("❌ Error: Access token not found!", cls=AlertT.error))

        print("🟢 Step 4: Access token retrieved.")

        # ✅ Show success Alert & redirect after 2 seconds
        response = Response(
            Div(
                Alert("✅ Login successful! Redirecting...", cls=AlertT.success),
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
        return Div(Alert(f"❌ Error: {str(e)}", cls=AlertT.error))
