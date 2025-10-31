import streamlit as st
from datetime import datetime
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

/* User card */
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

/* Reward card */
.reward-card {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
    transition: all 0.3s ease;
    border: 2px solid transparent;
}

.reward-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    border-color: #667eea;
}

.reward-card.locked {
    opacity: 0.6;
    background: #f7fafc;
}

.reward-icon {
    font-size: 2.5rem;
    text-align: center;
    margin-bottom: 0.5rem;
}

.reward-name {
    font-size: 1.1rem;
    font-weight: 700;
    color: #2d3748;
    margin-bottom: 0.5rem;
}

.reward-points {
    font-size: 1.2rem;
    font-weight: 600;
    color: #667eea;
}

/* Points display */
.points-banner {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    color: white;
}

.points-value {
    font-size: 3rem;
    font-weight: 800;
    margin: 0.5rem 0;
}

/* History item */
.history-item {
    background: rgba(255,255,255,0.95);
    padding: 1rem 1.5rem;
    border-radius: 10px;
    margin-bottom: 0.75rem;
    border-left: 4px solid #48bb78;
    transition: all 0.2s ease;
}

.history-item:hover {
    transform: translateX(5px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
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

/* Logout button styling - BLACK */
.stButton>button[kind="secondary"] {
    background-color: #1e293b !important;
    color: white !important;
    border: none !important;
}

.stButton>button[kind="secondary"]:hover {
    background-color: #334155 !important;
    color: white !important;
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
st.markdown("# 🎁 Rewards Shop")
st.markdown("### Redeem your hard-earned points!")
st.markdown("<br>", unsafe_allow_html=True)

# Load user data
data = load_data(st.session_state.username)
points = data.get('points', 0)

# Initialize redeemed list if not exists
if 'redeemed' not in data:
    data['redeemed'] = []

# Beautiful points banner
st.markdown(f"""
<div class="points-banner">
    <div style="font-size: 2.5rem;">💎</div>
    <div class="points-value">{points}</div>
    <div style="font-size: 1.2rem; font-weight: 600;">Your Points</div>
    <div style="font-size: 0.9rem; opacity: 0.8; margin-top: 0.5rem;">Keep logging to earn more!</div>
</div>
""", unsafe_allow_html=True)

# Rewards list with beautiful cards
rewards = [
    {"name": "☕ Starbucks Gift Card", "points": 100, "value": "$5"},
    {"name": "🎵 Spotify Gift Card", "points": 150, "value": "$10"},
    {"name": "📚 eBook of Choice", "points": 120, "value": "Any"},
    {"name": "🎬 Movie Ticket", "points": 130, "value": "1 Ticket"},
    {"name": "🎮 Steam Gift Card", "points": 200, "value": "$15"},
    {"name": "🎧 Premium App", "points": 180, "value": "1 Month"},
    {"name": "🍕 Food Delivery", "points": 250, "value": "$20"},
    {"name": "🎯 Custom Reward", "points": 300, "value": "Special"},
]

st.markdown("### 🏆 Available Rewards")
st.markdown("<br>", unsafe_allow_html=True)

# Display rewards in a grid
col1, col2 = st.columns(2)

for idx, reward in enumerate(rewards):
    can_afford = points >= reward['points']

    with col1 if idx % 2 == 0 else col2:
        # Reward card
        card_class = "" if can_afford else "locked"

        st.markdown(f"""
        <div class="reward-card {card_class}">
            <div class="reward-icon">{reward['name'].split()[0]}</div>
            <div class="reward-name">{' '.join(reward['name'].split()[1:])}</div>
            <div style="color: #718096; margin-bottom: 0.5rem;">{reward['value']}</div>
            <div class="reward-points">💎 {reward['points']} pts</div>
        </div>
        """, unsafe_allow_html=True)

        # Redeem button
        button_label = "✨ Redeem" if can_afford else "🔒 Locked"
        button_type = "primary" if can_afford else "secondary"

        if st.button(button_label, key=f"btn_{reward['name']}", disabled=not can_afford,
                     type=button_type, use_container_width=True):
            # Deduct points
            data['points'] -= reward['points']

            # Add to redeemed history
            data['redeemed'].append({
                'item': reward['name'],
                'points': reward['points'],
                'date': str(datetime.now().date())
            })

            # Save data
            save_data(data, st.session_state.username)

            # Update session state
            st.session_state.points = data['points']

            st.success(f"🎉 Successfully redeemed: {reward['name']}!")
            st.balloons()
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Redemption history
st.markdown("### 📜 Redemption History")

if data['redeemed']:
    for item in reversed(data['redeemed'][-10:]):
        st.markdown(f"""
        <div class="history-item">
            <strong>✅ {item['item']}</strong><br>
            <span style="color: #718096; font-size: 0.9rem;">{item['date']} • {item['points']} points</span>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("📝 No rewards redeemed yet. Start earning points to unlock rewards!")

st.markdown("<br>", unsafe_allow_html=True)

# Motivational section
st.markdown("### 💡 How to Earn More Points")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 10px; text-align: center;">
        <div style="font-size: 2rem;">📱</div>
        <div style="font-weight: 600; color: #2d3748; margin-top: 0.5rem;">Log Daily</div>
        <div style="color: #718096; font-size: 0.9rem;">+5-10 pts</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 10px; text-align: center;">
        <div style="font-size: 2rem;">🎯</div>
        <div style="font-weight: 600; color: #2d3748; margin-top: 0.5rem;">Meet Goals</div>
        <div style="color: #718096; font-size: 0.9rem;">+10 pts</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 10px; text-align: center;">
        <div style="font-size: 2rem;">🔥</div>
        <div style="font-weight: 600; color: #2d3748; margin-top: 0.5rem;">Build Streaks</div>
        <div style="color: #718096; font-size: 0.9rem;">Bonus pts</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)