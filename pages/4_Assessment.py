"""
pages/4_Assessment.py - Assessment Selection Hub for Heal-Together
Demonstrates Python syllabus concepts:
- Day 3: Conditional statements
- Day 4: Loops (for loop over collection)
- Day 6: Lists
- Day 7: Tuples
- Day 9-10: Dictionaries for assessment metadata
- Day 11: Functions
- Day 24: Streamlit project navigation
- Day 28: Streamlit display features
- Day 29: Project integration
"""

import streamlit as st
import auth

# Configure Page
st.set_page_config(
    page_title="Assessment Hub",
    page_icon="🌿",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
}
.stButton > button {
    background-color: #66B35A;
    color: white;
    border-radius: 10px;
    height: 48px;
    font-size: 15px;
    font-weight: 600;
    border: none;
}
.stButton > button:hover {
    background-color: #4E9447;
    color: white;
}
.assess-card {
    background-color: #161B22;
    border: 1px solid #30363D;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    border-top: 3px solid #66B35A;
}
blockquote {
    border-left: 3px solid #66B35A;
    padding-left: 15px;
    color: #8F8F8F;
}
</style>
""", unsafe_allow_html=True)

# Guard against unauthenticated access
auth.require_login()

user_name = auth.get_current_user_name()

# ============================================================
# PAGE HEADER
# ============================================================
st.title("🌿 Assessment Hub")
st.write(f"Welcome, **{user_name}** 💙")
st.write("""
> *"Self-reflection is the first step toward inner peace and emotional balance.
> Select an assessment below to begin your check-in."* 🌸
""")
st.divider()

# ============================================================
# ASSESSMENT OPTIONS DATA STRUCTURE (Day 9-10: Dictionaries & Day 6: Lists)
# ============================================================
assessment_options = [
    {
        "icon": "🧠",
        "title": "Mental Health Check",
        "page": "pages/4.1_Mental_Health.py",
        "description": "Reflect on your mood, emotional energy, daily interest, and inner peace.",
        "duration": "5 Questions (~2 mins)",
        "button_text": "Start Mental Health Check"
    },
    {
        "icon": "🫂",
        "title": "Loneliness Check",
        "page": "pages/4.2_Loneliness.py",
        "description": "Understand your feelings of connection, companionship, and social belonging.",
        "duration": "5 Questions (~2 mins)",
        "button_text": "Start Loneliness Check"
    },
    {
        "icon": "💙",
        "title": "Combined Check (Both)",
        "page": "pages/4.3_Both.py",
        "description": "A comprehensive reflection combining both emotional wellbeing and social connectivity.",
        "duration": "10 Questions (~4 mins)",
        "button_text": "Start Combined Check"
    },
    {
        "icon": "🤔",
        "title": "General Wellbeing / Not Sure",
        "page": "pages/4.4_Not_Sure.py",
        "description": "Not sure which to choose? Answer a few guided questions to discover what you need.",
        "duration": "10 Questions (~3 mins)",
        "button_text": "Start Wellbeing Check"
    }
]

# Display assessment cards in a 2x2 grid (Day 4: Loops)
col_left, col_right = st.columns(2)
columns = [col_left, col_right]

for idx, opt in enumerate(assessment_options):
    target_col = columns[idx % 2]
    with target_col:
        st.markdown(f"""
        <div class="assess-card">
            <h3 style="color: #66B35A; margin-top: 0;">{opt['icon']} {opt['title']}</h3>
            <p style="color: #CBD5E1; font-size: 14px; line-height: 1.6;">{opt['description']}</p>
            <p style="color: #8F8F8F; font-size: 12px; margin-bottom: 14px;">⏱️ <em>{opt['duration']}</em></p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(opt["button_text"], use_container_width=True, key=f"start_opt_{idx}"):
            st.switch_page(opt["page"])

st.divider()

# ============================================================
# NON-DIAGNOSTIC DISCLAIMER
# ============================================================
st.caption(
    '🌿 *"Important Note: Heal-Together assessments are designed solely for self-awareness and personal reflection. '
    'They do not provide medical diagnoses or replace professional mental healthcare."*'
)