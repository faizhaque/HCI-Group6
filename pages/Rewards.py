import streamlit as st
from datetime import datetime

st.title("🎁 Rewards Shop")

# Initialize session state
if 'points' not in st.session_state:
    st.session_state.points= 0
if 'redeemed' not in st.session_state:
    st.session_state.redeemed =[]

points = st.session_state.points

st.markdown(f"## Your Points: **{points}**")
st.markdown("---")

# Simple rewards list
rewards = [
    {"name": "☕ $5 Starbucks Gift Card", "points": 100},
    {"name": "🎵 $10 Spotify Gift Card", "points": 150},
    {"name": "📚 eBook of Your Choice", "points": 120},
    {"name": "🎬 Movie Ticket", "points": 130},
    {"name": "🎮 $15 Steam Gift Card", "points": 200},
    {"name": "🎧 1 Month Premium App", "points": 180},
]

# Display rewards
for reward in rewards:
    col1, col2, col3 =st.columns([3, 1, 1])
    
    with col1:
        st.write(f"**{reward['name']}**")
    with col2:
        st.write(f"{reward['points']} pts")
    with col3:
        can_afford = points >= reward['points']
        if st.button("Redeem", key=reward['name'], disabled=not can_afford):
            st.session_state.points-= reward['points']
            
            st.session_state.redeemed.append({
                'item': reward['name'],
                'points': reward['points'],
                'date': str(datetime.now().date())
            })
            
            st.success(f"Redeemed: {reward['name']}!")
            st.balloons()
            st.rerun()

st.markdown("---")

# Simple history
st.subheader("Your Redeemed Rewards")
if st.session_state.redeemed:
    for item in reversed(st.session_state.redeemed[-5:]):
        st.write(f"• {item['item']} - {item['date']}")
else:
    st.info("No rewards yet. Keep earning points!")