import streamlit as st
import json
import os
from datetime import datetime

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user= "Demo User"
if 'points' not in st.session_state:
    st.session_state.points =0

# Load data
def load_data():
    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            return json.load(f)
    return {'usage_logs': [], 'points': 0, 'streak': 0}

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)

st.set_page_config(page_title="Social Media Tracker", page_icon="🌊", layout="wide")

st.title("Social Media Usage Tracker")
st.subheader(f"Welcome, {st.session_state.user}!")

data = load_data()

# Display stats
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Points", data.get('points', 0))
with col2:
    st.metric("Current Streak", f"{data.get('streak', 0)} days")
with col3:
    st.metric("Logs This Week", len(data.get('usage_logs', [])))

st.info("Use the sidebar to navigate between pages")