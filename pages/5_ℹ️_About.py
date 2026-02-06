# pages/5_ℹ️_About.py
import streamlit as st

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)

# Header
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem; text-align: center;">
    <h1 style="margin: 0;">ℹ️ About AI Study Assistant</h1>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.2rem;">Your intelligent learning companion</p>
</div>
""", unsafe_allow_html=True)

# Project overview
st.markdown("## 🎓 Project Overview")

st.write("""
The **AI Study Assistant** is an intelligent learning platform designed to revolutionize the way students study.
By leveraging cutting-edge artificial intelligence and natural language processing, we make personalized learning
accessible to everyone.
""")

st.markdown("---")

# Features
st.markdown("## ✨ Key Features")

feature_col1, feature_col2 = st.columns(2)

with feature_col1:
    st.markdown("""
    ### 📚 Smart Flashcards
    - Upload PDF or text study materials
    - Automatically split into reviewable flashcards
    - Track which concepts you've mastered
    - Spaced repetition for better retention
    
    ### 🎯 AI Question Generator
    - Generate unlimited practice questions
    - Multiple question types (MCQ, T/F, Short Answer)
    - Powered by advanced language models
    - Questions tailored to your content
    """)

with feature_col2:
    st.markdown("""
    ### 📝 Intelligent Answer Evaluation
    - Instant feedback on your answers
    - Multi-dimensional scoring system
    - Semantic similarity analysis
    - Detailed explanations and improvements
    
    ### 📊 Progress Tracking
    - Visualize your learning journey
    - Identify strengths and weaknesses
    - Set and track goals
    - Performance analytics
    """)

st.markdown("---")

# Technology stack
st.markdown("## 🛠️ Technology Stack")

tech_col1, tech_col2, tech_col3 = st.columns(3)

with tech_col1:
    st.info("""
    **Frontend**
    - Streamlit
    - Plotly
    - Custom CSS/HTML
    """)

with tech_col2:
    st.success("""
    **AI/ML**
    - LangChain
    - Groq LLM API
    - Sentence Transformers
    - Scikit-learn
    """)

with tech_col3:
    st.warning("""
    **Backend**
    - Python 3.10+
    - PyPDF2
    - Pandas
    - NumPy
    """)

st.markdown("---")

# How it works
st.markdown("## 🔍 How It Works")

st.markdown("""
### Question Generation Process

1. **Content Analysis**: Your study material is analyzed by our AI model
2. **Question Creation**: The LLM generates relevant questions based on key concepts
3. **Quality Assurance**: Questions are formatted and validated
4. **Delivery**: You receive high-quality practice questions instantly

### Answer Evaluation System

Our evaluation uses three complementary methods:

1. **Semantic Similarity (50%)**: Compares meaning using AI embeddings
2. **Keyword Matching (35%)**: Checks if key concepts are mentioned
3. **Length Appropriateness (15%)**: Ensures answer completeness

Final Score = Weighted average of all three methods
""")

st.markdown("---")

# Team
st.markdown("## 👥 Development Team")

team_col1, team_col2 = st.columns(2)

with team_col1:
    st.markdown("""
    ### Module 1: Flashcard Manager
    **Developer**: [Partner's Name]
    
    **Responsibilities**:
    - File upload and text extraction
    - Flashcard generation algorithm
    - User interface design
    - Progress tracking
    """)

with team_col2:
    st.markdown("""
    ### Module 2: AI Question Engine
    **Developer**: [Your Name]
    
    **Responsibilities**:
    - LLM integration
    - Question generation algorithms
    - Answer evaluation system
    - NLP-based scoring
    """)

st.markdown("---")

# Future enhancements
st.markdown("## 🚀 Future Enhancements")

enhancement_col1, enhancement_col2 = st.columns(2)

with enhancement_col1:
    st.markdown("""
    ### Planned Features
    - 📱 Mobile app version
    - 🤝 Collaborative study groups
    - 🎮 Gamification elements
    - 🗣️ Voice-based practice
    - 🌐 Multi-language support
    """)

with enhancement_col2:
    st.markdown("""
    ### Technical Improvements
    - 💾 Cloud data synchronization
    - 🔐 User authentication
    - 📈 Advanced analytics
    - 🤖 Adaptive difficulty
    - 🎯 Personalized recommendations
    """)

st.markdown("---")

# Technical details
with st.expander("🔬 Technical Implementation Details"):
    st.markdown("""
    ### Architecture
    
    **Multi-Page Streamlit Application**
    - Modular design with separate pages for each feature
    - Shared session state for data persistence
    - Custom CSS for modern UI/UX
    
    **AI Integration**
    - Groq API for fast LLM inference
    - LangChain for prompt engineering
    - Sentence Transformers for semantic analysis
    
    **Data Processing**
    - PyPDF2 for PDF text extraction
    - Pandas for data manipulation
    - Plotly for interactive visualizations
    
    **Evaluation Algorithm**
```python
    final_score = (
        semantic_similarity * 0.50 +
        keyword_match * 0.35 +
        length_score * 0.15
    )
```
    """)

# Contact
st.markdown("---")
st.markdown("## 📞 Contact & Support")

contact_col1, contact_col2, contact_col3 = st.columns(3)

with contact_col1:
    st.info("""
    **📧 Email**
    
    support@studyassistant.com
    """)

with contact_col2:
    st.success("""
    **💬 Discord**
    
    StudyAI Community
    """)

with contact_col3:
    st.warning("""
    **🐙 GitHub**
    
    github.com/studyassistant
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>AI Study Assistant</strong> | Final Year Project 2026</p>
    <p>© 2026 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)