import streamlit as st
import json
import os
from datetime import datetime
import hashlib


# Custom CSS for beautiful styling
def load_css():
    st.markdown("""
    <style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
    }

    /* Sidebar styling - LIGHTER VERSION */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4a5568 0%, #2d3748 100%) !important;
    }

    /* Make ALL sidebar text white and visible */
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }

    [data-testid="stSidebar"] p {
        color: white !important;
    }

    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white !important;
    }

    /* Custom metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }

    [data-testid="stMetricLabel"] {
        font-size: 1rem;
        font-weight: 500;
        color: #4a5568;
    }

    /* Button styling */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        font-weight: 600;
    }

    /* Info box styling */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }

    /* Title styling */
    h1 {
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Sidebar user card */
    .user-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .user-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: white;
        margin: 0 auto 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    .user-name {
        color: white;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .user-role {
        color: rgba(255,255,255,0.9);
        font-size: 0.9rem;
    }

    /* Stat cards */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Emoji styling */
    .big-emoji {
        font-size: 3rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)


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
    st.set_page_config(page_title="Social Media Tracker - Login", page_icon="🌊", layout="centered")
    load_css()

    # Beautiful header with emoji
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='big-emoji'>🌊</div>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>Social Media Tracker</h1>", unsafe_allow_html=True)
        st.markdown(
            "<p style='text-align: center; color: #718096; font-size: 1.1rem;'>Track your usage, earn rewards, stay balanced</p>",
            unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs for Login and Signup
    tab1, tab2 = st.tabs(["🔐 Login", "✨ Sign Up"])

    with tab1:
        st.markdown("### Welcome Back!")
        st.markdown("<br>", unsafe_allow_html=True)

        login_username = st.text_input("Username", key="login_user", placeholder="Enter your username")
        login_password = st.text_input("Password", type="password", key="login_pass", placeholder="Enter your password")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚀 Login", type="primary", use_container_width=True):
            users = load_users()

            if login_username in users:
                if users[login_username] == hash_password(login_password):
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    st.success(f"✅ Welcome back, {login_username}!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Incorrect password!")
            else:
                st.error("❌ Username not found!")

    with tab2:
        st.markdown("### Create Your Account")
        st.markdown("<br>", unsafe_allow_html=True)

        signup_username = st.text_input("Choose a Username", key="signup_user", placeholder="Pick a unique username")
        signup_password = st.text_input("Choose a Password", type="password", key="signup_pass",
                                        placeholder="At least 4 characters")
        signup_password_confirm = st.text_input("Confirm Password", type="password", key="signup_pass_confirm",
                                                placeholder="Re-enter your password")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🎉 Create Account", type="primary", use_container_width=True):
            users = load_users()

            if not signup_username:
                st.error("❌ Please enter a username!")
            elif signup_username in users:
                st.error("❌ Username already exists!")
            elif len(signup_password) < 4:
                st.error("❌ Password must be at least 4 characters!")
            elif signup_password != signup_password_confirm:
                st.error("❌ Passwords don't match!")
            else:
                # Create new user
                users[signup_username] = hash_password(signup_password)
                save_users(users)

                # Auto login
                st.session_state.logged_in = True
                st.session_state.username = signup_username
                st.success(f"🎊 Account created! Welcome, {signup_username}!")
                st.balloons()
                st.rerun()

else:
    # Main App (when logged in)
    st.set_page_config(page_title="Social Media Tracker", page_icon="🌊", layout="wide")
    load_css()

    # Beautiful Sidebar
    with st.sidebar:
        # User profile card
        st.markdown(f"""
        <div class="user-card">
            <div class="user-avatar">🐱‍🐉</div>
            <div class="user-name">{st.session_state.username}</div>
            <div class="user-role">Member</div>
        </div>
        """, unsafe_allow_html=True)


        # Logout button with icon
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.points = 0
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.write("© 2025 HCI Group 6")

    # Main content
    st.markdown("# 🌊 Dashboard")
    st.markdown(f"### Welcome back, **{st.session_state.username}**! 👋")
    st.markdown("<br>", unsafe_allow_html=True)

    # Load user-specific data
    data = load_data(st.session_state.username)

    # Display stats in beautiful cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 2.5rem; text-align: center; margin-bottom: 0.5rem;">💎</div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: 700; color: #667eea;">{}</div>
                <div style="color: #718096; font-weight: 600;">Total Points</div>
            </div>
        </div>
        """.format(data.get('points', 0)), unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 2.5rem; text-align: center; margin-bottom: 0.5rem;">🔥</div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: 700; color: #f56565;">{}</div>
                <div style="color: #718096; font-weight: 600;">Day Streak</div>
            </div>
        </div>
        """.format(data.get('streak', 0)), unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 2.5rem; text-align: center; margin-bottom: 0.5rem;">📝</div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: 700; color: #48bb78;">{}</div>
                <div style="color: #718096; font-weight: 600;">Total Logs</div>
            </div>
        </div>
        """.format(len(data.get('usage_logs', []))), unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Tips section
    st.info("💡 **Pro Tip:** Log your usage daily to maintain your streak and earn bonus points!")

    # Recent activity
    if data.get('usage_logs', []):
        st.markdown("### 📅 Recent Activity")
        recent_logs = data['usage_logs'][-3:]
        for log in reversed(recent_logs):
            st.markdown(f"**{log['date']}** • {log['app']} • {log['time_spent']} minutes")

    st.markdown("<br><br>", unsafe_allow_html=True)