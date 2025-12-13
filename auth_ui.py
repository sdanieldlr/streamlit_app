
import streamlit as st
from dotenv import load_dotenv
from streamlit_oauth import OAuth2Component
import requests

from db import create_user, get_user, create_google_user, verify_user


load_dotenv()


REDIRECT_URI = st.secrets.get("redirect_uri", "https://similarly-listprice-arbor-paragraph.trycloudflare.com")


GOOGLE_SCOPE = (
    "https://www.googleapis.com/auth/userinfo.email "
    "https://www.googleapis.com/auth/userinfo.profile"
)


try:
    GOOGLE_CLIENT_ID = st.secrets["client_id"]
    GOOGLE_CLIENT_SECRET = st.secrets["client_secret"]
    google = OAuth2Component(
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
        token_endpoint="https://oauth2.googleapis.com/token",
    )
except KeyError:
    google = None  # OAuth disabled

def fetch_google_user_info(token_dict: dict) -> dict:
    """Fetch user info from Google using the access token."""
    if not isinstance(token_dict, dict):
        return {}

    access_token = token_dict.get("access_token")
    if not access_token:
        return {}

    try:
        resp = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=5,
        )
        if resp.ok:
            return resp.json()
    except Exception:
        pass

    return {}


def _handle_google_result(token: dict):
    user_info = fetch_google_user_info(token)

    email = user_info.get("email", "")
    name = user_info.get("name", "") or email

    if not email:
        st.error("Could not retrieve email from Google account.")
        return

    row = get_user(email)
    if not row:
        create_google_user(email, name)
        row = get_user(email)

    st.session_state["user"] = {
        "id": row[0],
        "email": row[1],
        "name": row[3] or row[1],
        "method": row[4] or "google",
    }

    st.session_state["google_token"] = token

    st.rerun()

def signup_view():
    st.subheader("Create account")

    email = st.text_input("Email", key="su_email")
    pwd = st.text_input("Password", type="password", key="su_pwd")
    confirm_pwd = st.text_input("Confirm Password", type="password", key="su_confirm_pwd")

    if st.button("Sign up", type="primary"):
        if not email or not pwd or not confirm_pwd:
            st.warning("Please fill in all fields.")
        elif pwd != confirm_pwd:
            st.error("Passwords do not match.")
        else:
            try:
                create_user(email, pwd)
                st.success("Account created. Go to Login tab to sign in.")
            except Exception as e:
                st.error(f"Could not create user: {e}")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("Or sign up with Google:")

    # Google OAuth sign-up
    if google is None:
        st.info("Google sign-in not configured. Add credentials to .streamlit/secrets.toml")
    elif "google_token" not in st.session_state:
        google_signup_result = google.authorize_button(
            "Sign up with Google",
            REDIRECT_URI,
            GOOGLE_SCOPE,
            key="google_signup",
        )

        if google_signup_result and "token" in google_signup_result:
            _handle_google_result(google_signup_result["token"])
    else:
        st.info("Already authenticated with Google.")

def login_view():
    st.subheader("Log in")

    email = st.text_input("Email", key="li_email")
    pwd = st.text_input("Password", type="password", key="li_pwd")

    if st.button("Login", type="primary"):
        if not email or not pwd:
            st.warning("Email and password required.")
        else:
            # Use verify_user for secure password checking
            user_id = verify_user(email, pwd)
            if user_id:
                row = get_user(email)
                st.session_state["user"] = {
                    "id": user_id,
                    "email": row[1],
                    "name": row[3] or row[1],
                    "method": row[4] or "manual",
                }
                st.success("Logged in.")
                st.rerun()
            else:
                st.error("Invalid credentials.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("Or sign in with Google:")

    # Google OAuth login
    if google is None:
        st.info("Google sign-in not configured. Add credentials to .streamlit/secrets.toml")
    elif "google_token" not in st.session_state:
        google_login_result = google.authorize_button(
            "Sign in with Google",
            REDIRECT_URI,
            GOOGLE_SCOPE,
            key="google_login",
        )

        if google_login_result and "token" in google_login_result:
            _handle_google_result(google_login_result["token"])
    else:
        st.info("Already authenticated with Google.")

def logout_button():
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Logout"):
            st.session_state.pop("user", None)
            st.session_state.pop("google_token", None)
            st.rerun()
    with col2:
        if st.button("Delete Account", type="secondary"):
            delete_account_view()


def delete_account_view():
    """Shows confirmation dialog for account deletion."""
    st.warning("⚠️ This action is permanent. All your notes will be deleted.")
    
    if st.button("Confirm: Delete my account", type="primary"):
        user = st.session_state.get("user")
        if user and isinstance(user, dict) and user.get("id"):
            from db import delete_user
            if delete_user(user["id"]):
                st.session_state.clear()
                st.success("Your account has been deleted.")
                st.rerun()
            else:
                st.error("Error deleting account. Please try again.")
        else:
            st.error("No active session.")
        st.rerun()