# pages/3_📝_Practice_Quiz.py
import streamlit as st
import sys
from pathlib import Path
import time

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from modules.answer_evaluator import AnswerEvaluator

# Page config
st.set_page_config(
    page_title="Practice Quiz",
    page_icon="📝",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    /* Quiz container */
    .quiz-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    /* Question card */
    .question-card {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        border-left: 5px solid #667eea;
    }
    
    .question-number {
        color: #667eea;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .question-text {
        font-size: 1.4rem;
        font-weight: 600;
        color: #333;
        line-height: 1.6;
    }
    
    /* Option cards */
    .option-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        margin: 0.8rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .option-card:hover {
        border-color: #667eea;
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
    }
    
    .option-selected {
        border-color: #667eea;
        background: #667eea10;
    }
    
    .option-correct {
        border-color: #38ef7d;
        background: #38ef7d15;
    }
    
    .option-incorrect {
        border-color: #f5576c;
        background: #f5576c15;
    }
    
    /* Progress bar */
    .custom-progress {
        background: #e0e0e0;
        height: 8px;
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .custom-progress-bar {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        transition: width 0.5s ease;
    }
    
    /* Score card */
    .score-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
    }
    
    .score-number {
        font-size: 4rem;
        font-weight: 800;
        margin: 1rem 0;
    }
    
    .score-label {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Timer */
    .timer {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        font-size: 1.2rem;
        font-weight: 700;
        text-align: center;
    }
    
    /* Feedback boxes */
    .feedback-correct {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        animation: slideIn 0.5s ease;
    }
    
    .feedback-incorrect {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        animation: slideIn 0.5s ease;
    }
    
    .feedback-partial {
        background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
        color: #333;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Navigation buttons */
    .nav-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 10px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .nav-button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Streak indicator */
    .streak-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Initialize evaluator
@st.cache_resource
def load_evaluator():
    return AnswerEvaluator()

# Initialize session state
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'correct_streak' not in st.session_state:
    st.session_state.correct_streak = 0
if 'max_streak' not in st.session_state:
    st.session_state.max_streak = 0

# Header
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem;">
    <h1 style="margin: 0;">📝 Practice Quiz</h1>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Test your knowledge and get instant feedback</p>
</div>
""", unsafe_allow_html=True)

# Check if questions exist
if 'generated_questions' not in st.session_state or not st.session_state.generated_questions:
    st.warning("⚠️ No questions available! Generate questions first.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 3rem;">
            <div style="font-size: 5rem; margin-bottom: 1rem;">📚</div>
            <h3>No Questions Yet</h3>
            <p style="color: #666;">Generate some questions first to start practicing!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎯 Go to Question Generator", use_container_width=True, type="primary"):
            st.switch_page("pages/2_🎯_Generate_Questions.py")
    
    st.stop()

# Load data
questions = st.session_state.generated_questions
q_type = st.session_state.question_type
evaluator = load_evaluator()

# Quiz not started - Show start screen
if not st.session_state.quiz_started:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: white; 
                    border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🎯</div>
            <h2>Ready to Start?</h2>
            <p style="color: #666; margin: 1rem 0;">You have <strong>{}</strong> questions waiting</p>
        </div>
        """.format(len(questions)), unsafe_allow_html=True)
        
        st.markdown("")
        
        # Quiz info
        info_col1, info_col2 = st.columns(2)
        
        with info_col1:
            st.info(f"""
            **📊 Quiz Details**
            - Questions: {len(questions)}
            - Type: {q_type.upper()}
            - Time: Untimed
            """)
        
        with info_col2:
            st.success("""
            **💡 Tips**
            - Read carefully
            - Take your time
            - Review feedback
            """)
        
        st.markdown("")
        
        if st.button("🚀 Start Quiz", use_container_width=True, type="primary"):
            st.session_state.quiz_started = True
            st.session_state.start_time = time.time()
            st.session_state.current_question_index = 0
            st.session_state.user_answers = {}
            st.session_state.quiz_completed = False
            st.session_state.correct_streak = 0
            st.session_state.max_streak = 0
            st.rerun()

# Quiz in progress
elif not st.session_state.quiz_completed:
    current_idx = st.session_state.current_question_index
    current_q = questions[current_idx]
    total_questions = len(questions)
    
    # Sidebar - Progress tracker
    with st.sidebar:
        st.markdown("### 📊 Quiz Progress")
        
        # Progress bar
        progress = (current_idx + 1) / total_questions
        st.progress(progress)
        st.markdown(f"**Question {current_idx + 1} of {total_questions}**")
        
        st.markdown("---")
        
        # Stats
        answered = len(st.session_state.user_answers)
        st.metric("Answered", f"{answered}/{total_questions}")
        
        if st.session_state.correct_streak > 0:
            st.markdown(f"""
            <div class="streak-badge">
                🔥 {st.session_state.correct_streak} Streak!
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Timer
        if st.session_state.start_time:
            elapsed = int(time.time() - st.session_state.start_time)
            mins = elapsed // 60
            secs = elapsed % 60
            st.markdown(f"""
            <div class="timer">
                ⏱️ {mins:02d}:{secs:02d}
            </div>
            """, unsafe_allow_html=True)
    
    # Question display
    st.markdown(f"""
    <div class="question-card">
        <div class="question-number">Question {current_idx + 1} of {total_questions}</div>
        <div class="question-text">{current_q.get('question' if q_type == 'mcq' else 'statement' if q_type == 'tf' else 'question', 'N/A')}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer input based on type
    user_answer = None
    
    if q_type == "mcq":
        options = current_q.get('options', {})
        
        st.markdown("### Select your answer:")
        
        for opt_key, opt_text in options.items():
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                if st.button(opt_key, key=f"opt_{opt_key}", use_container_width=True):
                    user_answer = opt_key
            with col2:
                st.markdown(f"**{opt_text}**")
        
        # Store answer
        if user_answer:
            st.session_state.user_answers[current_idx] = user_answer
    
    elif q_type == "tf":
        st.markdown("### Is this statement True or False?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ True", use_container_width=True, type="primary"):
                user_answer = True
                st.session_state.user_answers[current_idx] = user_answer
        
        with col2:
            if st.button("❌ False", use_container_width=True):
                user_answer = False
                st.session_state.user_answers[current_idx] = user_answer
    
    else:  # Short answer
        st.markdown("### Write your answer:")
        
        # Show key points hint
        with st.expander("💡 Key Points to Consider"):
            key_points = current_q.get('key_points', [])
            for point in key_points:
                st.markdown(f"- {point}")
        
        user_answer = st.text_area(
            "Your answer (2-3 sentences):",
            height=150,
            key=f"sa_{current_idx}",
            placeholder="Write a clear, detailed answer..."
        )
        
        if st.button("Submit Answer", type="primary"):
            if user_answer and user_answer.strip():
                st.session_state.user_answers[current_idx] = user_answer
            else:
                st.error("Please write an answer before submitting.")
    
    # Show feedback if answered
    if current_idx in st.session_state.user_answers:
        st.markdown("---")
        
        # Evaluate answer
        user_ans = st.session_state.user_answers[current_idx]
        
        if q_type == "mcq":
            correct_ans = current_q.get('correct_answer')
            result = evaluator.evaluate_mcq(user_ans, correct_ans)
            
            if result['is_correct']:
                st.markdown(f"""
                <div class="feedback-correct">
                    <h3>✅ Correct!</h3>
                    <p>{result['feedback']}</p>
                    {f"<p><strong>Explanation:</strong> {current_q.get('explanation', '')}</p>" if 'explanation' in current_q else ""}
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
                st.session_state.correct_streak += 1
                st.session_state.max_streak = max(st.session_state.max_streak, st.session_state.correct_streak)
            else:
                st.markdown(f"""
                <div class="feedback-incorrect">
                    <h3>❌ Incorrect</h3>
                    <p>The correct answer is: <strong>{correct_ans}</strong></p>
                    {f"<p><strong>Explanation:</strong> {current_q.get('explanation', '')}</p>" if 'explanation' in current_q else ""}
                </div>
                """, unsafe_allow_html=True)
                st.session_state.correct_streak = 0
        
        elif q_type == "tf":
            correct_ans = current_q.get('answer')
            result = evaluator.evaluate_true_false(user_ans, correct_ans)
            
            if result['is_correct']:
                st.markdown(f"""
                <div class="feedback-correct">
                    <h3>✅ Correct!</h3>
                    <p>{current_q.get('explanation', 'Well done!')}</p>
                </div>
                """, unsafe_allow_html=True)
                st.balloons()
                st.session_state.correct_streak += 1
                st.session_state.max_streak = max(st.session_state.max_streak, st.session_state.correct_streak)
            else:
                st.markdown(f"""
                <div class="feedback-incorrect">
                    <h3>❌ Incorrect</h3>
                    <p>The correct answer is: <strong>{'True' if correct_ans else 'False'}</strong></p>
                    <p><strong>Explanation:</strong> {current_q.get('explanation', '')}</p>
                </div>
                """, unsafe_allow_html=True)
                st.session_state.correct_streak = 0
        
        else:  # Short answer
            correct_ans = current_q.get('sample_answer')
            key_points = current_q.get('key_points', [])
            result = evaluator.evaluate_short_answer(user_ans, correct_ans, key_points)
            
            score = result['score']
            
            if score >= 75:
                st.markdown(f"""
                <div class="feedback-correct">
                    <h3>✅ Excellent Answer!</h3>
                    <p><strong>Score: {score:.1f}%</strong></p>
                    <p>{result['feedback']}</p>
                </div>
                """, unsafe_allow_html=True)
                if score >= 90:
                    st.balloons()
            elif score >= 60:
                st.markdown(f"""
                <div class="feedback-partial">
                    <h3>✓ Good Effort</h3>
                    <p><strong>Score: {score:.1f}%</strong></p>
                    <p>{result['feedback']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="feedback-incorrect">
                    <h3>⚠️ Needs Improvement</h3>
                    <p><strong>Score: {score:.1f}%</strong></p>
                    <p>{result['feedback']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Show breakdown
            with st.expander("📊 Score Breakdown"):
                breakdown = result.get('breakdown', {})
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Semantic", f"{breakdown.get('semantic_similarity', 0):.0f}%")
                with col_b:
                    st.metric("Keywords", f"{breakdown.get('keyword_match', 0):.0f}%")
                with col_c:
                    st.metric("Length", f"{breakdown.get('length_appropriateness', 0):.0f}%")
            
            # Show sample answer
            with st.expander("📝 Sample Answer"):
                st.write(correct_ans)
    
    # Navigation
    st.markdown("---")
    nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])
    
    with nav_col1:
        if current_idx > 0:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.current_question_index -= 1
                st.rerun()
    
    with nav_col2:
        if current_idx in st.session_state.user_answers:
            st.success("✓ Answered")
    
    with nav_col3:
        if current_idx < total_questions - 1:
            if st.button("Next ➡️", use_container_width=True, type="primary"):
                st.session_state.current_question_index += 1
                st.rerun()
        else:
            if st.button("🏁 Finish Quiz", use_container_width=True, type="primary"):
                if len(st.session_state.user_answers) < total_questions:
                    st.warning(f"⚠️ You've answered {len(st.session_state.user_answers)}/{total_questions} questions. Finish anyway?")
                    if st.button("Yes, Finish Now"):
                        st.session_state.quiz_completed = True
                        st.rerun()
                else:
                    st.session_state.quiz_completed = True
                    st.rerun()

# Quiz completed - Show results
else:
    # Calculate final stats
    total_questions = len(questions)
    answered = len(st.session_state.user_answers)
    
    scores = []
    correct_count = 0
    
    for idx, q in enumerate(questions):
        if idx in st.session_state.user_answers:
            user_ans = st.session_state.user_answers[idx]
            
            if q_type == "mcq":
                result = evaluator.evaluate_mcq(user_ans, q.get('correct_answer'))
            elif q_type == "tf":
                result = evaluator.evaluate_true_false(user_ans, q.get('answer'))
            else:
                result = evaluator.evaluate_short_answer(
                    user_ans, q.get('sample_answer'), q.get('key_points', [])
                )
            
            scores.append(result['score'])
            if result['is_correct']:
                correct_count += 1
    
    avg_score = sum(scores) / len(scores) if scores else 0
    
    # Calculate time taken
    time_taken = int(time.time() - st.session_state.start_time) if st.session_state.start_time else 0
    mins = time_taken // 60
    secs = time_taken % 60
    
    # Results page
    st.markdown("""
    <div class="score-card">
        <h2 style="margin: 0;">🎉 Quiz Complete!</h2>
        <div class="score-number">{:.1f}%</div>
        <div class="score-label">Average Score</div>
    </div>
    """.format(avg_score), unsafe_allow_html=True)
    
    # Performance grade
    if avg_score >= 90:
        grade = "A"
        message = "Outstanding! You've mastered this material! 🏆"
        st.balloons()
    elif avg_score >= 75:
        grade = "B"
        message = "Great job! You have a solid understanding! 👏"
    elif avg_score >= 60:
        grade = "C"
        message = "Good effort! Review the feedback to improve. 📚"
    elif avg_score >= 50:
        grade = "D"
        message = "You're getting there. More practice needed. 💪"
    else:
        grade = "F"
        message = "Don't give up! Review the material and try again. 🔄"
    
    st.markdown(f"### Grade: {grade}")
    st.info(message)
    
    st.markdown("---")
    
    # Detailed stats
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric("Questions", f"{answered}/{total_questions}")
    
    with stat_col2:
        st.metric("Correct", f"{correct_count}/{answered}")
    
    with stat_col3:
        st.metric("Time Taken", f"{mins}:{secs:02d}")
    
    with stat_col4:
        st.metric("Max Streak", f"{st.session_state.max_streak} 🔥")
    
    st.markdown("---")
    
    # Review answers
    st.markdown("### 📋 Review Your Answers")
    
    for idx, q in enumerate(questions):
        if idx in st.session_state.user_answers:
            with st.expander(f"Question {idx + 1} - {scores[idx]:.0f}%"):
                # Show question
                if q_type == "mcq":
                    st.markdown(f"**Q:** {q.get('question')}")
                    st.markdown(f"**Your Answer:** {st.session_state.user_answers[idx]}")
                    st.markdown(f"**Correct Answer:** {q.get('correct_answer')}")
                    
                    result = evaluator.evaluate_mcq(
                        st.session_state.user_answers[idx], 
                        q.get('correct_answer')
                    )
                    
                    if result['is_correct']:
                        st.success("✅ Correct!")
                    else:
                        st.error("❌ Incorrect")
                    
                    if 'explanation' in q:
                        st.info(f"💡 {q['explanation']}")
                
                elif q_type == "tf":
                    st.markdown(f"**Statement:** {q.get('statement')}")
                    st.markdown(f"**Your Answer:** {'True' if st.session_state.user_answers[idx] else 'False'}")
                    st.markdown(f"**Correct Answer:** {'True' if q.get('answer') else 'False'}")
                    
                    result = evaluator.evaluate_true_false(
                        st.session_state.user_answers[idx],
                        q.get('answer')
                    )
                    
                    if result['is_correct']:
                        st.success("✅ Correct!")
                    else:
                        st.error("❌ Incorrect")
                    
                    st.info(f"💡 {q.get('explanation', '')}")
                
                else:  # Short answer
                    st.markdown(f"**Q:** {q.get('question')}")
                    st.markdown("**Your Answer:**")
                    st.write(st.session_state.user_answers[idx])
                    st.markdown("**Sample Answer:**")
                    st.write(q.get('sample_answer'))
                    
                    result = evaluator.evaluate_short_answer(
                        st.session_state.user_answers[idx],
                        q.get('sample_answer'),
                        q.get('key_points', [])
                    )
                    
                    st.write(f"**Score:** {result['score']:.1f}%")
                    st.write(f"**Feedback:** {result['feedback']}")
    
    st.markdown("---")
    
    # Action buttons
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("🔄 Retake Quiz", use_container_width=True):
            st.session_state.quiz_started = False
            st.session_state.current_question_index = 0
            st.session_state.user_answers = {}
            st.session_state.quiz_completed = False
            st.session_state.start_time = None
            st.session_state.correct_streak = 0
            st.rerun()
    
    with action_col2:
        if st.button("🎯 New Questions", use_container_width=True):
            st.switch_page("pages/2_🎯_Generate_Questions.py")
    
    with action_col3:
        if st.button("📊 View Dashboard", use_container_width=True):
            st.switch_page("pages/4_📊_Progress_Dashboard.py")