import streamlit as st
from datetime import datetime
import json


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
    st.warning("Please login first!")
    st.stop()

# Sidebar with user info and logout
with st.sidebar:
    st.markdown(f"### {st.session_state.username}")
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.points = 0
        st.switch_page("app.py")

st.title("Rewards Shop")

# Load user data
data = load_data(st.session_state.username)
points = data.get('points', 0)

# Initialize redeemed list if not exists
if 'redeemed' not in data:
    data['redeemed'] = []

st.markdown(f"## Your Points: **{points}** 💎")
st.markdown("---")

# Rewards list
rewards = [
    {"name": "☕ $5 Starbucks Gift Card", "points": 100},
    {"name": "🎵 $10 Spotify Gift Card", "points": 150},
    {"name": "📚 eBook of Your Choice", "points": 120},
    {"name": "🎬 Movie Ticket", "points": 130},
    {"name": "🎮 $15 Steam Gift Card", "points": 200},
    {"name": "🎧 1 Month Premium App", "points": 180},
    {"name": "🍕 $20 Food Delivery", "points": 250},
    {"name": "🎯 Custom Reward", "points": 300},
]

# Display rewards in a nice layout
for reward in rewards:
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        st.write(f"**{reward['name']}**")
    with col2:
        st.write(f"💎 {reward['points']} pts")
    with col3:
        can_afford = points >= reward['points']
        button_label = "Redeem" if can_afford else "🔒 Locked"

        if st.button(button_label, key=reward['name'], disabled=not can_afford,
                     type="primary" if can_afford else "secondary"):
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

            st.success(f"Redeemed: {reward['name']}!")
            st.balloons()
            st.rerun()

st.markdown("---")

# Redemption history
st.subheader("🏆 Your Redeemed Rewards")
if data['redeemed']:
    for item in reversed(data['redeemed'][-5:]):
        st.write(f" {item['item']} - {item['date']} ({item['points']} points)")
else:
    st.info("No rewards redeemed yet. Keep earning points!")

# Motivational message
st.markdown("---")
st.info(" **Tip:** Log your usage daily to earn more points and unlock rewards!")