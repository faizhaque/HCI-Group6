import streamlit as st
from datetime import date
import json


def load_data(username):
    try:
        filename = f'data_{username}.json'
        with open(filename,'r') as f:
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
        st.session_state.logged_in =False
        st.session_state.username= None
        st.session_state.points = 0
        st.switch_page("app.py")

st.title("Track Your Usage")

# Load user data
data = load_data(st.session_state.username)

# Display current points
st.markdown(f"## Your Points: **{data.get('points', 0)}**")
st.markdown("---")

# Select app
app = st.selectbox("Social Media App", 
    ["Instagram", "TikTok", "Twitter/X", "Facebook", "Snapchat"])

# Time spent
time_spent = st.text_input("Minutes spent today",value="30")

# Goal
daily_goal = st.text_input("Your daily goal (minutes)", value="60")

# Log entry
if st.button("Log Usage", type="primary"):
    time_spent = int(time_spent)
    daily_goal = int(daily_goal)
    
    # Calculate points
    if time_spent <= daily_goal:
        points_earned = 10
        st.success(f"Great job! You stayed under your goal. +{points_earned} points!")
    else:
        points_earned = 5
        st.warning(f"You went over your goal, but tracking is progress! +{points_earned} points")
    
    # Save log
    data['usage_logs'].append({
        'date': str(date.today()),
        'app': app,
        'time_spent':time_spent,
        'goal':daily_goal
    })
    
    # Update points
    data['points'] = data.get('points', 0) + points_earned
    
    # Save to file
    save_data(data, st.session_state.username)
    
    # Update session state
    st.session_state.points = data['points']
    
    st.balloons()
    st.rerun()

# Show recent logs
st.subheader("Recent Logs")
if data['usage_logs']:
    for log in reversed(data['usage_logs'][-5:]):
        st.write(f"**{log['date']}** - {log['app']}: {log['time_spent']} min (Goal: {log['goal']} min)")
else:
    st.info("No logs yet. Start tracking!")