import streamlit as st
import json
import plotly.express as px
import pandas as pd


def load_data(username):
    try:
        filename = f'data_{username}.json'
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return {'usage_logs': [], 'points': 0, 'streak': 0}


# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first!")
    st.stop()

# Sidebar with user info and logout
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.username}")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.points = 0
        st.switch_page("app.py")

st.title("📊 My Progress")

data = load_data(st.session_state.username)

if not data['usage_logs']:
    st.warning("No data yet. Start logging your usage!")
else:
    # Convert to DataFrame
    df = pd.DataFrame(data['usage_logs'])

    # Chart: Time spent by app
    fig = px.bar(df, x='app', y='time_spent',
                 title="Time Spent by App",
                 color='app',
                 labels={'time_spent': 'Minutes', 'app': 'Social Media App'})
    st.plotly_chart(fig, use_container_width=True)

    # Chart: Daily usage over time
    daily_df = df.groupby('date')['time_spent'].sum().reset_index()
    fig2 = px.line(daily_df, x='date', y='time_spent',
                   title="Daily Usage Trend",
                   markers=True,
                   labels={'time_spent': 'Total Minutes', 'date': 'Date'})
    st.plotly_chart(fig2, use_container_width=True)

    # Stats
    st.subheader("📈 Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Minutes Tracked", df['time_spent'].sum())
        st.metric("Average Daily Usage", f"{df['time_spent'].mean():.1f} min")
    with col2:
        st.metric("Most Used App", df['app'].mode()[0])
        st.metric("Days Tracked", df['date'].nunique())