# pages/1_📚_Flashcards.py
import streamlit as st
import PyPDF2

st.set_page_config(
    page_title="Flashcard Manager",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .flashcard {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        min-height: 250px;
        color: white;
        font-size: 18px;
        line-height: 1.6;
        margin: 20px 0;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .known-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    
    .review-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem;">
    <h1 style="margin: 0;">📚 Flashcard Manager</h1>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Upload your notes and create interactive flashcards</p>
</div>
""", unsafe_allow_html=True)

# Helper function
def create_flashcards(text, words_per_card=100):
    """Split text into flashcard chunks"""
    words = text.split()
    flashcards = []
    
    for i in range(0, len(words), words_per_card):
        chunk = ' '.join(words[i:i + words_per_card])
        if chunk.strip():
            flashcards.append(chunk)
    
    return flashcards

# Initialize session state
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = []
if 'current_card' not in st.session_state:
    st.session_state.current_card = 0
if 'known_cards' not in st.session_state:
    st.session_state.known_cards = []
if 'review_cards' not in st.session_state:
    st.session_state.review_cards = []

# Sidebar - Progress
with st.sidebar:
    st.markdown("### 📊 Progress")
    
    if st.session_state.flashcards:
        total = len(st.session_state.flashcards)
        known = len(st.session_state.known_cards)
        review = len(st.session_state.review_cards)
        unseen = total - known - review
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total", total)
            st.metric("Known", known)
        with col2:
            st.metric("Review", review)
            st.metric("Unseen", unseen)
        
        # Progress bar
        if total > 0:
            progress = known / total
            st.progress(progress)
            st.write(f"**{int(progress * 100)}%** Complete")
        
        st.markdown("---")
        
        if st.button("🔄 Reset Progress", use_container_width=True):
            st.session_state.known_cards = []
            st.session_state.review_cards = []
            st.rerun()
    else:
        st.info("Upload a file to see progress")

# Main content
tab1, tab2 = st.tabs(["📤 Upload & Create", "📇 Study Flashcards"])

with tab1:
    st.markdown("### Upload Your Study Material")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['pdf', 'txt'],
        help="Upload PDF or TXT files"
    )
    
    if uploaded_file is not None:
        # Extract text
        if uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        else:
            text = uploaded_file.read().decode('utf-8')
        
        st.success(f"✅ File uploaded! Extracted {len(text)} characters")
        
        with st.expander("📄 View Extracted Content"):
            st.text_area("Content", text[:1000] + "...", height=200, disabled=True)
        
        st.markdown("---")
        
        # Settings
        col1, col2 = st.columns([2, 1])
        
        with col1:
            words_per_card = st.slider(
                "Words per flashcard",
                min_value=50,
                max_value=200,
                value=100,
                step=10,
                help="Adjust the size of each flashcard"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🎴 Create Flashcards", type="primary", use_container_width=True):
                flashcards = create_flashcards(text, words_per_card)
                
                st.session_state.flashcards = flashcards
                st.session_state.current_card = 0
                st.session_state.known_cards = []
                st.session_state.review_cards = []
                
                st.success(f"✅ Created {len(flashcards)} flashcards!")
                st.balloons()
                st.info("👉 Go to the 'Study Flashcards' tab to review them")

with tab2:
    if not st.session_state.flashcards:
        st.info("👈 Upload a file and create flashcards first!")
    else:
        flashcards = st.session_state.flashcards
        current = st.session_state.current_card
        
        # Card status
        if current in st.session_state.known_cards:
            card_class = "flashcard known-card"
            status_text = "✅ You know this!"
            status_color = "success"
        elif current in st.session_state.review_cards:
            card_class = "flashcard review-card"
            status_text = "🔄 Needs review"
            status_color = "warning"
        else:
            card_class = "flashcard"
            status_text = "❓ Not reviewed yet"
            status_color = "info"
        
        # Status indicator
        if status_color == "success":
            st.success(status_text)
        elif status_color == "warning":
            st.warning(status_text)
        else:
            st.info(status_text)
        
        # Card counter
        st.markdown(f"### Flashcard {current + 1} of {len(flashcards)}")
        
        # Display flashcard
        st.markdown(f"""
        <div class="{card_class}">
            {flashcards[current]}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Marking buttons
        st.markdown("### How well do you know this?")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("✅ I Know This", use_container_width=True, type="primary"):
                if current not in st.session_state.known_cards:
                    st.session_state.known_cards.append(current)
                if current in st.session_state.review_cards:
                    st.session_state.review_cards.remove(current)
                st.rerun()
        
        with col_b:
            if st.button("🔄 Need Review", use_container_width=True):
                if current not in st.session_state.review_cards:
                    st.session_state.review_cards.append(current)
                if current in st.session_state.known_cards:
                    st.session_state.known_cards.remove(current)
                st.rerun()
        
        st.markdown("---")
        
        # Navigation
        nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])
        
        with nav_col1:
            if st.button("⬅️ Previous", disabled=(current == 0), use_container_width=True):
                st.session_state.current_card -= 1
                st.rerun()
        
        with nav_col2:
            st.markdown(f"<h3 style='text-align: center;'>{current + 1} / {len(flashcards)}</h3>", 
                       unsafe_allow_html=True)
        
        with nav_col3:
            if st.button("Next ➡️", disabled=(current == len(flashcards) - 1), use_container_width=True):
                st.session_state.current_card += 1
                st.rerun()