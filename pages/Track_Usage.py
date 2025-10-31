import streamlit as st
from datetime import date
import json

# Custom CSS
st.markdown("""
<style>
/* Main background */
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

/* User card in sidebar */
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

/* Title styling */
h1 {
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Input containers */
.input-card {
    background: white;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}

/* Button styling */
.stButton>button {
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.3s ease;
    padding: 0.75rem 1.5rem;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}

/* Log entry card */
.log-entry {
    background: rgba(255,255,255,0.95);
    padding: 1rem 1.5rem;
    border-radius: 10px;
    margin-bottom: 0.75rem;
    border-left: 4px solid #667eea;
    transition: all 0.2s ease;
}

.log-entry:hover {
    transform: translateX(5px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

/* Info box */
.stAlert {
    border-radius: 10px;
    border-left: 4px solid #667eea;
}

/* Hide branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


def load_data(username):
    try:
        filename = f'data_{username}.json'
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return {'usage_logs': [], 'points': 0, 'streak': 0}


def save_data(data, username):
    filename = f'data_{username}.json'
    with open(filename, 'w') as f:
        json.dump(data, f)


# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first!")
    st.stop()

# Beautiful Sidebar
with st.sidebar:
    # User profile card
    st.markdown(f"""
    <div class="user-card">
        <div class="user-avatar">👤</div>
        <div class="user-name">{st.session_state.username}</div>
        <div class="user-role">Member</div>
    </div>
    """, unsafe_allow_html=True)


    # Logout button
    if st.button("🚪 Logout", use_container_width=True, type="secondary"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.points = 0
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.write("© 2025 HCI Group 6")

# Main content
st.markdown("# 📱 Track Your Usage")
st.markdown("### Log your daily social media activity")
st.markdown("<br>", unsafe_allow_html=True)

# Load user data
data = load_data(st.session_state.username)

# Display current points in a beautiful card
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"""
    <div style="background: white; padding: 2rem; border-radius: 15px; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
        <div style="font-size: 2rem;">💎</div>
        <div style="font-size: 2.5rem; font-weight: 700; color: #667eea; margin: 0.5rem 0;">{data.get('points', 0)}</div>
        <div style="color: #718096; font-weight: 600;">Your Points</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Input form in a card
st.markdown('<div class="input-card">', unsafe_allow_html=True)

# Select app with emoji
app_options = {
    "📷 Instagram": "Instagram",
    "🎵 TikTok": "TikTok",
    "🐦 Twitter/X": "Twitter/X",
    "👥 Facebook": "Facebook",
    "👻 Snapchat": "Snapchat",
    "📺 YouTube": "YouTube",
    "🤖 Reddit": "Reddit"
}

selected = st.selectbox("📱 Choose Platform", list(app_options.keys()))
app = app_options[selected]

st.markdown("<br>", unsafe_allow_html=True)

# Time and goal inputs
col1, col2 = st.columns(2)
with col1:
    time_spent = st.number_input("⏱️ Minutes Spent Today", min_value=0, max_value=1440, value=30, step=5)
with col2:
    daily_goal = st.number_input("🎯 Your Daily Goal", min_value=0, max_value=1440, value=60, step=5)

st.markdown("<br>", unsafe_allow_html=True)

# Progress bar
if daily_goal > 0:
    progress = min(time_spent / daily_goal, 1.0)
    st.progress(progress)
    if time_spent <= daily_goal:
        st.markdown(
            f"<p style='text-align: center; color: #48bb78; font-weight: 600;'>✅ You're {daily_goal - time_spent} minutes under your goal!</p>",
            unsafe_allow_html=True)
    else:
        st.markdown(
            f"<p style='text-align: center; color: #f56565; font-weight: 600;'>⚠️ You're {time_spent - daily_goal} minutes over your goal</p>",
            unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Log button
if st.button("✨ Log Usage", type="primary", use_container_width=True):
    # Calculate points
    if time_spent <= daily_goal:
        points_earned = 10
        st.success(f"🎉 Amazing! You stayed under your goal. **+{points_earned} points**")
        st.balloons()
    else:
        points_earned = 5
        st.warning(f"📝 You went over your goal, but tracking is progress! **+{points_earned} points**")

    # Save log
    data['usage_logs'].append({
        'date': str(date.today()),
        'app': app,
        'time_spent': time_spent,
        'goal': daily_goal
    })

    # Update points and streak
    data['points'] = data.get('points', 0) + points_earned
    data['streak'] = data.get('streak', 0) + 1

    # Save to file
    save_data(data, st.session_state.username)

    # Update session state
    st.session_state.points = data['points']

    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Recent logs section
st.markdown("### 📅 Recent Activity")
if data['usage_logs']:
    for log in reversed(data['usage_logs'][-5:]):
        goal_met = "✅" if log['time_spent'] <= log['goal'] else "⚠️"
        st.markdown(f"""
        <div class="log-entry">
            <strong>{goal_met} {log['date']}</strong> • {log['app']} • {log['time_spent']} min (Goal: {log['goal']} min)
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("📝 No logs yet. Start tracking your usage above!")

st.markdown("<br>", unsafe_allow_html=True)

# Motivational tips
tips = [
    "💡 Set realistic goals to stay motivated!",
    "🎯 Consistency is key - log daily for best results!",
    "🏆 Small improvements add up over time!",
    "⏰ Try using a timer to track your usage more accurately!",
    "🌟 Celebrate your wins, no matter how small!"
]

import random

st.info(random.choice(tips))