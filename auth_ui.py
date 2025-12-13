import streamlit as st
from dotenv import load_dotenv
from streamlit_oauth import OAuth2Component
import requests

from db import create_user, get_user, create_google_user


load_dotenv()


REDIRECT_URI = "https://similarly-listprice-arbor-paragraph.trycloudflare.com"


GOOGLE_SCOPE = (
    "https://www.googleapis.com/auth/userinfo.email "
    "https://www.googleapis.com/auth/userinfo.profile"
)


GOOGLE_CLIENT_ID = "985077610080-u3ml16p73ia6kg7q4mempcntqcfbo2eh.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"

google = OAuth2Component(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
    token_endpoint="https://oauth2.googleapis.com/token",
)

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

    if st.button("Sign up", type="primary"):
        if not email or not pwd:
            st.warning("Email and password required.")
        else:
            try:
                create_user(email, pwd)
                st.success("Account created. Go to Login tab to sign in.")
            except Exception as e:
                st.error(f"Could not create user: {e}")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("Or sign up with Google:")

    # Only handle Google sign up when we don't already have a token
    if "google_token" not in st.session_state:
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
            row = get_user(email)
            if row and row[2] == pwd:
                st.session_state["user"] = {
                    "id": row[0],
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

    if "google_token" not in st.session_state:
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
    if st.button("Logout"):
        st.session_state.pop("user", None)
        st.session_state.pop("google_token", None)
        st.rerun()
