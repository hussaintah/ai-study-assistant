# pages/2_🎯_Generate_Questions.py
import streamlit as st
import sys
from pathlib import Path
import os
from dotenv import load_dotenv
import json

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="Generate Questions",
    page_icon="🎯",
    layout="wide"
)

# Load environment
load_dotenv()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
    
    .question-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0;">🎯 AI Question Generator</h1>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Transform your study material into practice questions</p>
</div>
""", unsafe_allow_html=True)

# Check API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("⚠️ GROQ_API_KEY not found in .env file!")
    st.info("Please add your Groq API key to the .env file")
    st.code('GROQ_API_KEY=your_key_here', language='bash')
    st.stop()

# Load generator
try:
    from modules.question_generator import QuestionGenerator
    
    @st.cache_resource
    def load_generator():
        return QuestionGenerator()
    
    generator = load_generator()
    st.success("✅ AI Model loaded successfully!")
    
except Exception as e:
    st.error(f"❌ Error loading AI model: {e}")
    with st.expander("🔍 Error Details"):
        st.code(str(e))
    st.stop()

# Sidebar settings
with st.sidebar:
    st.markdown("### ⚙️ Question Settings")
    
    question_type = st.selectbox(
        "Question Type",
        ["Multiple Choice", "True/False", "Short Answer"],
        help="Choose the type of questions to generate"
    )
    
    num_questions = st.slider(
        "Number of Questions",
        min_value=1,
        max_value=10,
        value=5,
        help="How many questions to generate"
    )
    
    st.markdown("---")
    
    st.markdown("### 💡 Tips")
    st.info("""
    - Use at least 200 words of content
    - Clear, well-written content = better questions
    - Review generated questions before use
    - Try different question types
    """)

# Main content area
st.markdown("### 📄 Study Material Input")

# Text input
study_content = st.text_area(
    "Paste your study material here:",
    height=300,
    placeholder="""Enter at least 200 characters of study material...

Example:
Photosynthesis is the process by which green plants use sunlight to synthesize nutrients from carbon dioxide and water. It involves the green pigment chlorophyll and generates oxygen as a byproduct. The process occurs in two main stages: the light-dependent reactions and the light-independent reactions (Calvin cycle)...
""",
    help="The more detailed your content, the better the questions"
)

# Show statistics
if study_content:
    word_count = len(study_content.split())
    char_count = len(study_content)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Words", word_count)
    
    with col2:
        st.metric("Characters", char_count)
    
    with col3:
        if word_count < 50:
            st.metric("Status", "Too Short", delta="Need more")
        elif word_count < 150:
            st.metric("Status", "Adequate", delta="OK")
        else:
            st.metric("Status", "Great!", delta="✓")

st.markdown("---")

# Generate button
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    generate_clicked = st.button(
        "🚀 Generate Questions",
        type="primary",
        use_container_width=True
    )

# Generate questions
if generate_clicked:
    if not study_content or len(study_content.strip()) < 50:
        st.error("❌ Please enter at least 50 characters of study material")
    else:
        # Progress indicator
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🤖 AI is analyzing your content...")
        progress_bar.progress(25)
        
        try:
            # Generate based on type
            if question_type == "Multiple Choice":
                status_text.text("🎯 Creating multiple choice questions...")
                progress_bar.progress(50)
                questions = generator.generate_mcq(study_content, num_questions)
                q_type = "mcq"
                
            elif question_type == "True/False":
                status_text.text("✓ Creating true/false questions...")
                progress_bar.progress(50)
                questions = generator.generate_true_false(study_content, num_questions)
                q_type = "tf"
                
            else:  # Short Answer
                status_text.text("✍️ Creating short answer questions...")
                progress_bar.progress(50)
                questions = generator.generate_short_answer(study_content, num_questions)
                q_type = "sa"
            
            progress_bar.progress(75)
            status_text.text("✨ Finalizing questions...")
            
            if questions and len(questions) > 0:
                progress_bar.progress(100)
                status_text.empty()
                progress_bar.empty()
                
                # Success message
                st.success(f"🎉 Successfully generated {len(questions)} questions!")
                st.balloons()
                
                # Store in session state
                st.session_state['generated_questions'] = questions
                st.session_state['question_type'] = q_type
                st.session_state['study_content'] = study_content
                
                # Display questions
                st.markdown("---")
                st.markdown("### 📝 Generated Questions")
                
                for i, q in enumerate(questions, 1):
                    with st.expander(f"Question {i}", expanded=(i==1)):
                        if question_type == "Multiple Choice":
                            st.markdown(f"**{q.get('question', 'N/A')}**")
                            st.markdown("")
                            
                            options = q.get('options', {})
                            for opt, text in options.items():
                                st.markdown(f"**{opt}.)** {text}")
                            
                            st.markdown("")
                            st.success(f"✅ **Correct Answer:** {q.get('correct_answer')}")
                            
                            if 'explanation' in q:
                                st.info(f"💡 **Explanation:** {q['explanation']}")
                        
                        elif question_type == "True/False":
                            st.markdown(f"**{q.get('statement', 'N/A')}**")
                            st.markdown("")
                            
                            answer = q.get('answer', False)
                            st.success(f"✅ **Answer:** {'True' if answer else 'False'}")
                            
                            if 'explanation' in q:
                                st.info(f"💡 **Explanation:** {q['explanation']}")
                        
                        else:  # Short Answer
                            st.markdown(f"**{q.get('question', 'N/A')}**")
                            st.markdown("")
                            
                            st.markdown("**📖 Sample Answer:**")
                            st.write(q.get('sample_answer', 'N/A'))
                            
                            if 'key_points' in q:
                                st.markdown("**🔑 Key Points to Include:**")
                                for point in q['key_points']:
                                    st.markdown(f"- {point}")
                
                # Action buttons
                st.markdown("---")
                
                btn_col1, btn_col2, btn_col3 = st.columns(3)
                
                with btn_col1:
                    st.download_button(
                        label="📥 Download JSON",
                        data=json.dumps(questions, indent=2),
                        file_name="study_questions.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                with btn_col2:
                    st.download_button(
                        label="📄 Download Text",
                        data="\n\n".join([f"Q{i}: {q.get('question', q.get('statement', 'N/A'))}" for i, q in enumerate(questions, 1)]),
                        file_name="study_questions.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with btn_col3:
                    if st.button("📝 Practice These Questions", use_container_width=True):
                        st.switch_page("pages/3_📝_Practice_Quiz.py")
            
            else:
                progress_bar.empty()
                status_text.empty()
                st.error("❌ Failed to generate questions. Please try different content or try again.")
                
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Error: {str(e)}")
            with st.expander("🔍 Error Details"):
                st.code(str(e))

# Show if questions already exist
if 'generated_questions' in st.session_state and st.session_state.get('generated_questions'):
    st.markdown("---")
    st.info(f"💾 You have {len(st.session_state['generated_questions'])} questions saved from previous generation")
    
    col_action1, col_action2 = st.columns(2)
    
    with col_action1:
        if st.button("📝 Practice Saved Questions", use_container_width=True):
            st.switch_page("pages/3_📝_Practice_Quiz.py")
    
    with col_action2:
        if st.button("🔄 Clear Saved Questions", use_container_width=True):
            del st.session_state['generated_questions']
            st.rerun()