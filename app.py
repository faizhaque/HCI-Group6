import streamlit as st
import json
import os
from datetime import datetime
import hashlib


# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Load users
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}


def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)


# Load user-specific data
def load_data(username):
    filename = f'data_{username}.json'
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {'usage_logs': [], 'points': 0, 'streak': 0}


def save_data(data, username):
    filename = f'data_{username}.json'
    with open(filename, 'w') as f:
        json.dump(data, f)


# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'points' not in st.session_state:
    st.session_state.points = 0

# Login/Signup Page
if not st.session_state.logged_in:
    st.set_page_config(page_title="Social Media Tracker - Login", page_icon="", layout="centered")

    # Header
    st.markdown("<h1 style='text-align: center;'>🌊 Social Media Usage Tracker</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Track your social media usage and earn rewards!</p>",
                unsafe_allow_html=True)
    st.markdown("---")

    # Tabs for Login and Signup
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

    with tab1:
        st.subheader("Login to Your Account")
        login_username = st.text_input("Username", key="login_user")
        login_password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login", type="primary", use_container_width=True):
            users = load_users()

            if login_username in users:
                if users[login_username] == hash_password(login_password):
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    st.success(f"Welcome back, {login_username}!")
                    st.rerun()
                else:
                    st.error("Incorrect password!")
            else:
                st.error("Username not found!")

    with tab2:
        st.subheader("Create New Account")
        signup_username = st.text_input("Choose a Username", key="signup_user")
        signup_password = st.text_input("Choose a Password", type="password", key="signup_pass")
        signup_password_confirm = st.text_input("Confirm Password", type="password", key="signup_pass_confirm")

        if st.button("Sign Up", type="primary", use_container_width=True):
            users = load_users()

            if not signup_username:
                st.error("Please enter a username!")
            elif signup_username in users:
                st.error("Username already exists!")
            elif len(signup_password) < 4:
                st.error("Password must be at least 4 characters!")
            elif signup_password != signup_password_confirm:
                st.error("Passwords don't match!")
            else:
                # Create new user
                users[signup_username] = hash_password(signup_password)
                save_users(users)

                # Auto login
                st.session_state.logged_in = True
                st.session_state.username = signup_username
                st.success(f"Account created! Welcome, {signup_username}!")
                st.balloons()
                st.rerun()

else:
    # Main App (when logged in)
    st.set_page_config(page_title="Social Media Tracker", page_icon="🌊", layout="wide")

    # Sidebar with logout
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.username}")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.points = 0
            st.rerun()

    st.title("🌊 Social Media Usage Tracker")
    st.subheader(f"Welcome, {st.session_state.username}!")

    # Load user-specific data
    data = load_data(st.session_state.username)

    # Display stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Points", data.get('points', 0))
    with col2:
        st.metric("Current Streak", f"{data.get('streak', 0)} days")
    with col3:
        st.metric("Logs This Week", len(data.get('usage_logs', [])))

    st.info("👈 Use the sidebar to navigate between pages")