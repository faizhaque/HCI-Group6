import streamlit as st
import json
from datetime import datetime, date

def load_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except:
        return {'usage_logs': [], 'points': 0, 'streak': 0}

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)

st.title("📱 Track Your Usage")

# Select app
app = st.selectbox("Social Media App", 
    ["Instagram", "TikTok", "Twitter/X", "Facebook", "Snapchat"])

# Time spent
time_spent = st.number_input("Minutes spent today", min_value=0, max_value=1440, value=30)

# Goal
daily_goal = st.number_input("Your daily goal (minutes)", min_value=0, value=60)

# Log entry
if st.button("Log Usage", type="primary"):
    data = load_data()
    
    # Calculate points (reward for staying under goal)
    if time_spent <= daily_goal:
        points_earned = 10
        st.success(f"✅ Great job! You stayed under your goal. +{points_earned} points!")
    else:
        points_earned = 5
        st.warning(f"You went over your goal, but tracking is progress! +{points_earned} points")
    
    # Save log
    log_entry = {
        'date': str(date.today()),
        'app': app,
        'time_spent': time_spent,
        'goal': daily_goal,
        'points': points_earned
    }
    
    data['usage_logs'].append(log_entry)
    data['points'] = data.get('points', 0) + points_earned
    
    # Update streak
    data['streak'] = data.get('streak', 0) + 1
    
    save_data(data)
    st.balloons()

# Show recent logs
st.subheader("Recent Logs")
data = load_data()
if data['usage_logs']:
    for log in data['usage_logs'][-5:]:
        st.write(f"**{log['date']}** - {log['app']}: {log['time_spent']} min (Goal: {log['goal']} min)")
else:
    st.info("No logs yet. Start tracking!")