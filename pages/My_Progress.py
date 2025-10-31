import streamlit as st
import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

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

/* Metric cards */
.metric-card {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    text-align: center;
    transition: all 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: #667eea;
    margin: 0.5rem 0;
}

.metric-label {
    color: #718096;
    font-weight: 600;
    font-size: 1rem;
}

/* Chart container */
.chart-container {
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
st.markdown("# 📊 My Progress")
st.markdown("### Visualize your social media habits")
st.markdown("<br>", unsafe_allow_html=True)

data = load_data(st.session_state.username)

if not data['usage_logs']:
    # Empty state
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background: white; padding: 3rem; border-radius: 15px; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
            <h2 style="color: #667eea;">No Data Yet!</h2>
            <p style="color: #718096;">Start logging your usage to see your progress and insights here.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 Navigate to **Track_Usage** page using the selector above to start logging!")
else:
    # Convert to DataFrame
    df = pd.DataFrame(data['usage_logs'])

    # Key Statistics Cards
    st.markdown("### 📈 Key Statistics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem;">⏱️</div>
            <div class="metric-value">{df['time_spent'].sum()}</div>
            <div class="metric-label">Total Minutes</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem;">📱</div>
            <div class="metric-value">{df['date'].nunique()}</div>
            <div class="metric-label">Days Tracked</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem;">📊</div>
            <div class="metric-value">{df['time_spent'].mean():.0f}</div>
            <div class="metric-label">Avg Minutes/Day</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        most_used = df['app'].mode()[0] if not df['app'].mode().empty else "N/A"
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem;">⭐</div>
            <div class="metric-value" style="font-size: 1.5rem;">{most_used}</div>
            <div class="metric-label">Most Used App</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Charts in beautiful containers
    st.markdown("### 📊 Usage Analysis")

    # Chart 1: Time spent by app (Bar chart with custom colors)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    app_totals = df.groupby('app')['time_spent'].sum().sort_values(ascending=False)

    fig1 = go.Figure(go.Bar(
        x=app_totals.index,
        y=app_totals.values,
        marker=dict(
            color=['#0ea5e9', '#06b6d4', '#14b8a6', '#10b981', '#84cc16', '#eab308', '#f59e0b'],
            line=dict(color='#0284c7', width=2)
        ),
        text=[f"{val} min" for val in app_totals.values],
        textposition='outside',
    ))

    fig1.update_layout(
        title=dict(text="Time Spent by Platform", font=dict(size=18, color='#1e293b')),
        xaxis_title="Social Media Platform",
        yaxis_title="Total Minutes",
        height=450,
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=13, color='#334155'),
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis=dict(
            gridcolor='#cbd5e1',
            gridwidth=1,
            showgrid=True
        ),
        yaxis=dict(
            gridcolor='#cbd5e1',
            gridwidth=1,
            showgrid=True
        )
    )

    st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

    # Chart 2: Daily usage trend (Line chart)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    daily_df = df.groupby('date')['time_spent'].sum().reset_index()

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=daily_df['date'],
        y=daily_df['time_spent'],
        mode='lines+markers',
        name='Daily Usage',
        line=dict(color='#0ea5e9', width=4),
        marker=dict(size=10, color='#0284c7', line=dict(color='white', width=2)),
        fill='tozeroy',
        fillcolor='rgba(14, 165, 233, 0.2)'
    ))

    fig2.update_layout(
        title=dict(text="Daily Usage Trend", font=dict(size=18, color='#1e293b')),
        xaxis_title="Date",
        yaxis_title="Total Minutes",
        height=450,
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=13, color='#334155'),
        margin=dict(l=20, r=20, t=60, b=20),
        hovermode='x unified',
        xaxis=dict(
            gridcolor='#94a3b8',
            gridwidth=1.5,
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            gridcolor='#94a3b8',
            gridwidth=1.5,
            showgrid=True,
            zeroline=True,
            zerolinecolor='#64748b',
            zerolinewidth=2
        )
    )

    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

    # Chart 3: Goal Achievement (Pie chart)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    df['goal_met'] = df['time_spent'] <= df['goal']
    goal_stats = df['goal_met'].value_counts()

    fig3 = go.Figure(go.Pie(
        labels=['Goal Met ✅', 'Over Goal ⚠️'],
        values=[goal_stats.get(True, 0), goal_stats.get(False, 0)],
        hole=0.4,
        marker=dict(colors=['#48bb78', '#f56565']),
        textinfo='label+percent',
        textfont=dict(size=14)
    ))

    fig3.update_layout(
        title="Goal Achievement Rate",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        margin=dict(l=20, r=20, t=40, b=20)
    )

    st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Insights section
    st.markdown("###  Insights & Tips")

    total_minutes = df['time_spent'].sum()
    avg_daily = df['time_spent'].mean()
    goals_met = (df['time_spent'] <= df['goal']).sum()
    total_logs = len(df)

    col1, col2 = st.columns(2)

    with col1:
        if avg_daily < 60:
            st.success(f" **Great job!** Your average daily usage of {avg_daily:.0f} minutes is under 1 hour!")
        elif avg_daily < 120:
            st.info(f" Your average daily usage is {avg_daily:.0f} minutes. Consider reducing it slightly!")
        else:
            st.warning(f" Your average daily usage is {avg_daily:.0f} minutes. Try setting lower goals!")

    with col2:
        success_rate = (goals_met / total_logs * 100) if total_logs > 0 else 0
        if success_rate >= 70:
            st.success(f" **Excellent!** You've met your goals {success_rate:.0f}% of the time!")
        elif success_rate >= 50:
            st.info(f" You've met your goals {success_rate:.0f}% of the time. Keep improving!")
        else:
            st.warning(f" You've met your goals {success_rate:.0f}% of the time. Try setting more realistic goals!")

st.markdown("<br><br>", unsafe_allow_html=True)