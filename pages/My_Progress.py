import streamlit as st
import json
import plotly.express as px
import pandas as pd

def load_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except:
        return {'usage_logs': [], 'points': 0, 'streak': 0}

st.title("📊 My Progress")

data = load_data()

if not data['usage_logs']:
    st.warning("No data yet. Start logging your usage!")
else:
    # Convert to DataFrame
    df = pd.DataFrame(data['usage_logs'])
    
    # Chart: Time spent by app
    fig = px.bar(df, x='app', y='time_spent', 
                 title="Time Spent by App",
                 color='app')
    st.plotly_chart(fig, use_container_width=True)
    
    # Chart: Daily usage over time
    daily_df = df.groupby('date')['time_spent'].sum().reset_index()
    fig2 = px.line(daily_df, x='date', y='time_spent',
                   title="Daily Usage Trend",
                   markers=True)
    st.plotly_chart(fig2, use_container_width=True)
    
    # Stats
    st.subheader("Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Minutes Tracked", df['time_spent'].sum())
        st.metric("Average Daily Usage", f"{df['time_spent'].mean():.1f} min")
    with col2:
        st.metric("Most Used App", df['app'].mode()[0])
        st.metric("Days Tracked", df['date'].nunique())