import streamlit as st
from datetime import date

st.title("Track Your Usage")

# Initialize session state
if 'usage_logs' not in st.session_state:
    st.session_state.usage_logs = []
if 'points' not in st.session_state:
    st.session_state.points = 0

# Select app
app = st.selectbox("Social Media App", 
    ["Instagram", "TikTok", "Twitter/X", "Facebook", "Snapchat"])

# Time spent
time_spent = st.text_input("Minutes spent today", value="30")

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
    st.session_state.usage_logs.append({
        'date': str(date.today()),
        'app': app,
        'time_spent': time_spent,
        'goal': daily_goal
    })
    st.session_state.points += points_earned
    st.balloons()

# Show recent logs
st.subheader("Recent Logs")
if st.session_state.usage_logs:
    for log in st.session_state.usage_logs[-5:]:
        st.write(f"**{log['date']}** - {log['app']}: {log['time_spent']} min (Goal: {log['goal']} min)")
else:
    st.info("No logs yet. Start tracking!")