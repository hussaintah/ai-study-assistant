# app.py - Main Landing Page
import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_extras.colored_header import colored_header

# Page configuration
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern look
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary: #667eea;
        --secondary: #764ba2;
        --accent: #f093fb;
    }
    
    /* Hero section */
    .hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .hero h1 {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .hero p {
        font-size: 1.3rem;
        opacity: 0.95;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
        border-left: 4px solid var(--primary);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #666;
        line-height: 1.6;
    }
    
    /* Stats section */
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <h1>🎓 AI Study Assistant</h1>
    <p>Transform the way you study with AI-powered learning tools</p>
</div>
""", unsafe_allow_html=True)

# Introduction
st.markdown("### 👋 Welcome to Your Personal Study Companion")
st.write("""
Our AI-powered platform helps you learn more effectively by generating personalized practice questions,
providing instant feedback, and tracking your progress—all powered by cutting-edge artificial intelligence.
""")

st.markdown("---")

# Feature Cards
st.markdown("### ✨ Powerful Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📚</div>
        <div class="feature-title">Smart Flashcards</div>
        <div class="feature-desc">
            Upload your notes and create interactive flashcards automatically. 
            Track which concepts you've mastered and which need more review.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">AI Question Generator</div>
        <div class="feature-desc">
            Generate unlimited practice questions from your study material. 
            MCQs, True/False, and short answer questions powered by AI.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Progress Tracking</div>
        <div class="feature-desc">
            Visualize your learning journey with detailed analytics. 
            See improvement over time and identify areas for focus.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# How It Works Section
st.markdown("### 🚀 How It Works")

step_col1, step_col2, step_col3, step_col4 = st.columns(4)

with step_col1:
    st.markdown("#### 1️⃣ Upload")
    st.write("Upload your study materials (PDFs, text files)")

with step_col2:
    st.markdown("#### 2️⃣ Generate")
    st.write("AI creates personalized questions and flashcards")

with step_col3:
    st.markdown("#### 3️⃣ Practice")
    st.write("Answer questions and review flashcards")

with step_col4:
    st.markdown("#### 4️⃣ Improve")
    st.write("Track progress and master your subjects")

st.markdown("---")

# Stats Section
st.markdown("### 📈 Platform Stats")

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">1000+</div>
        <div class="stat-label">Questions Generated</div>
    </div>
    """, unsafe_allow_html=True)

with stat_col2:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">500+</div>
        <div class="stat-label">Flashcards Created</div>
    </div>
    """, unsafe_allow_html=True)

with stat_col3:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">95%</div>
        <div class="stat-label">Accuracy Rate</div>
    </div>
    """, unsafe_allow_html=True)

with stat_col4:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-number">24/7</div>
        <div class="stat-label">Always Available</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Call to Action
st.markdown("### 🎯 Ready to Start Learning?")

cta_col1, cta_col2, cta_col3 = st.columns([1, 2, 1])

with cta_col2:
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <p style="font-size: 1.2rem; color: #666; margin-bottom: 1.5rem;">
            Choose a feature from the sidebar to get started!
        </p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar Content
with st.sidebar:
    st.markdown("## 🎓 Navigation")
    st.info("👈 Select a page above to get started!")
    
    st.markdown("---")
    
    st.markdown("## 💡 Quick Tips")
    st.markdown("""
    - Start with **Flashcards** for passive review
    - Use **Generate Questions** for active practice
    - Check **Progress Dashboard** to track learning
    - Practice regularly for best results
    """)
    
    st.markdown("---")
    
    st.markdown("## 📞 Support")
    st.markdown("""
    Having issues? Contact:
    - 📧 Email: support@studyassistant.com
    - 💬 Discord: StudyAI Community
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>Built with ❤️ using Streamlit and AI | © 2026 AI Study Assistant</p>
</div>
""", unsafe_allow_html=True)