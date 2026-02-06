# pages/4_📊_Progress_Dashboard.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import os

st.set_page_config(
    page_title="Progress Dashboard",
    page_icon="📊",
    layout="wide"
)

# Header
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem;">
    <h1 style="margin: 0;">📊 Progress Dashboard</h1>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Track your learning journey and insights</p>
</div>
""", unsafe_allow_html=True)

# Mock data for demonstration
# In real implementation, this would come from saved user data

def generate_mock_data():
    """Generate sample progress data"""
    dates = pd.date_range(end=datetime.now(), periods=14, freq='D')
    
    data = {
        'date': dates,
        'questions_answered': [12, 15, 8, 20, 18, 22, 16, 25, 19, 21, 17, 23, 20, 24],
        'accuracy': [65, 70, 68, 75, 72, 78, 76, 80, 82, 79, 81, 83, 85, 87],
        'time_spent': [25, 30, 20, 40, 35, 45, 38, 50, 42, 48, 40, 52, 45, 55]
    }
    
    return pd.DataFrame(data)

# Get data
df = generate_mock_data()

# Summary statistics
st.markdown("### 📈 Overall Performance")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_questions = df['questions_answered'].sum()
    st.metric(
        "Total Questions",
        f"{total_questions}",
        delta=f"+{df['questions_answered'].iloc[-1]} today"
    )

with col2:
    avg_accuracy = df['accuracy'].mean()
    accuracy_trend = df['accuracy'].iloc[-1] - df['accuracy'].iloc[-2]
    st.metric(
        "Average Accuracy",
        f"{avg_accuracy:.1f}%",
        delta=f"{accuracy_trend:+.1f}%"
    )

with col3:
    total_time = df['time_spent'].sum()
    st.metric(
        "Total Study Time",
        f"{total_time} mins",
        delta=f"+{df['time_spent'].iloc[-1]} mins today"
    )

with col4:
    streak = 14  # Mock data
    st.metric(
        "Current Streak",
        f"{streak} days",
        delta="🔥"
    )

st.markdown("---")

# Charts
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("### 📊 Daily Questions Answered")
    
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=df['date'],
        y=df['questions_answered'],
        marker_color='#667eea',
        text=df['questions_answered'],
        textposition='outside'
    ))
    
    fig1.update_layout(
        height=400,
        showlegend=False,
        xaxis_title="Date",
        yaxis_title="Questions",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    st.markdown("### 📈 Accuracy Trend")
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df['date'],
        y=df['accuracy'],
        mode='lines+markers',
        line=dict(color='#38ef7d', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(56, 239, 125, 0.2)'
    ))
    
    fig2.update_layout(
        height=400,
        showlegend=False,
        xaxis_title="Date",
        yaxis_title="Accuracy (%)",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Study time analysis
st.markdown("### ⏰ Study Time Analysis")

col_time1, col_time2 = st.columns(2)

with col_time1:
    # Time per day
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=df['date'],
        y=df['time_spent'],
        mode='lines+markers',
        line=dict(color='#f093fb', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(240, 147, 251, 0.2)'
    ))
    
    fig3.update_layout(
        title="Daily Study Time",
        height=350,
        showlegend=False,
        xaxis_title="Date",
        yaxis_title="Minutes"
    )
    
    st.plotly_chart(fig3, use_container_width=True)

with col_time2:
    # Weekly breakdown
    weekly_data = pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'Minutes': [45, 52, 38, 55, 42, 60, 48]
    })
    
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        x=weekly_data['Day'],
        y=weekly_data['Minutes'],
        marker_color=['#667eea', '#764ba2', '#667eea', '#764ba2', '#667eea', '#764ba2', '#667eea'],
        text=weekly_data['Minutes'],
        textposition='outside'
    ))
    
    fig4.update_layout(
        title="This Week's Activity",
        height=350,
        showlegend=False,
        xaxis_title="Day",
        yaxis_title="Minutes"
    )
    
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# Performance breakdown
st.markdown("### 🎯 Performance by Topic")

topics_data = pd.DataFrame({
    'Topic': ['Machine Learning', 'Data Structures', 'Algorithms', 'Databases', 'Networks'],
    'Questions': [45, 38, 52, 30, 25],
    'Accuracy': [85, 78, 82, 90, 75]
})

col_topic1, col_topic2 = st.columns(2)

with col_topic1:
    fig5 = px.bar(
        topics_data,
        x='Topic',
        y='Questions',
        color='Accuracy',
        color_continuous_scale='Viridis',
        text='Questions'
    )
    
    fig5.update_layout(
        title="Questions by Topic",
        height=350,
        showlegend=False
    )
    
    st.plotly_chart(fig5, use_container_width=True)

with col_topic2:
    fig6 = go.Figure(data=[go.Pie(
        labels=topics_data['Topic'],
        values=topics_data['Questions'],
        hole=.4,
        marker_colors=['#667eea', '#764ba2', '#38ef7d', '#f093fb', '#f5576c']
    )])
    
    fig6.update_layout(
        title="Topic Distribution",
        height=350
    )
    
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# Insights
st.markdown("### 💡 AI-Powered Insights")

insights_col1, insights_col2, insights_col3 = st.columns(3)

with insights_col1:
    st.success("""
    **🎯 Strength Area**
    
    You're doing excellent in **Databases** with 90% accuracy!
    Keep up the great work!
    """)

with insights_col2:
    st.warning("""
    **📚 Focus Area**
    
    **Networks** needs more practice (75% accuracy).
    Recommended: 30 more questions
    """)

with insights_col3:
    st.info("""
    **📈 Improvement**
    
    Your accuracy improved by **22%** in the last 2 weeks!
    Excellent progress!
    """)

st.markdown("---")

# Goals
st.markdown("### 🎯 Your Goals")

goal_col1, goal_col2 = st.columns(2)

with goal_col1:
    st.markdown("#### Weekly Goals")
    
    goals = {
        "Answer 100 questions": (78, 100),
        "Study 5 hours": (4.2, 5),
        "85% average accuracy": (83, 85)
    }
    
    for goal, (current, target) in goals.items():
        progress = current / target
        st.write(f"**{goal}**")
        st.progress(progress)
        st.write(f"{current}/{target} ({progress*100:.0f}%)")
        st.markdown("")

with goal_col2:
    st.markdown("#### Achievements")
    
    achievements = [
        "🏆 7-Day Streak",
        "🎯 100 Questions Milestone",
        "⭐ 80% Accuracy Average",
        "📚 5 Topics Covered",
        "🔥 Most Active Learner"
    ]
    
    for achievement in achievements:
        st.success(achievement)

# Export data
st.markdown("---")
st.markdown("### 📥 Export Your Data")

if st.button("📊 Download Progress Report (CSV)", type="primary"):
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"study_progress_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )