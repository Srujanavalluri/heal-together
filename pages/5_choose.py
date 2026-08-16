"""
pages/5_choose.py - Wellness Hub (Support & Reflection) for Heal-Together
Demonstrates Python syllabus concepts:
- Day 4: Loops
- Day 6: Lists
- Day 7: Tuples
- Day 9-10: Dictionaries
- Day 11: Functions
- Day 24: Streamlit project navigation
- Day 28: Streamlit display features
- Day 29: Project integration
"""

import streamlit as st
import auth

# Configure Page
st.set_page_config(
    page_title="Support & Reflection",
    page_icon="✨",
    layout="wide"
)

# Custom Styling - Calm, soothing theme with green accents
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
    font-size: 16px;
    font-weight: 600;
    border: none;
}
.stButton > button:hover {
    background-color: #4E9447;
    color: white;
}
.hub-card {
    background-color: #161B22;
    border: 1px solid #30363D;
    border-radius: 12px;
    padding: 24px;
    border-top: 4px solid #66B35A;
    margin-bottom: 16px;
    height: 100%;
}
blockquote {
    border-left: 3px solid #66B35A;
    padding-left: 15px;
    color: #CBD5E1;
}
</style>
""", unsafe_allow_html=True)

# Guard against unauthenticated access
auth.require_login()

user_name = auth.get_current_user_name()

# ============================================================
# PAGE HEADER
# ============================================================
st.title("✨ Support & Reflection")
st.write(f"Welcome, **{user_name}** 💚")
st.write("""
> *"Healing begins with gentle self-compassion. Choose a support area below to practice mindful routines,
> write your thoughts, or take small connection steps."* 🌿🌸
""")
st.divider()

# ============================================================
# TWO MAIN WELLNESS COLUMNS (Mental Health vs Loneliness)
# ============================================================
col_mh, col_lon = st.columns(2)

with col_mh:
    st.markdown("""
    <div class="hub-card">
        <h2 style="color: #66B35A; margin-top:0;">🧠 Mental Health</h2>
        <p style="color: #F5F5F5; font-size: 15px;">
            <strong>Nurture your mind, breath, and inner energy:</strong>
        </p>
        <ul style="color: #CBD5E1; font-size: 14px; line-height: 1.8;">
            <li>🌸 <strong>Daily Mood Check-in:</strong> Visual emotional progress tracking.</li>
            <li>😴 <strong>Sleep Routine Planner:</strong> Establish peaceful bedtime habits.</li>
            <li>🚶 <strong>Outdoor Walk Tracker:</strong> Clear heavy thoughts with fresh air.</li>
            <li>🌿 <strong>4-4-4 Box Breathing:</strong> Calm heart rate and release stress.</li>
            <li>⏰ <strong>Gentle Mindful Reminders:</strong> Hydration & stretch notifications.</li>
            <li>✨ <strong>Personal Quotes & Mantras:</strong> Custom affirmations in your backend vault.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    if st.button("🧠 Enter Mental Wellness Space", use_container_width=True, key="btn_go_mh"):
        st.switch_page("pages/5.1_MentalHealth.py")

with col_lon:
    st.markdown("""
    <div class="hub-card">
        <h2 style="color: #66B35A; margin-top:0;">🤝 Loneliness & Connection</h2>
        <p style="color: #F5F5F5; font-size: 15px;">
            <strong>Find warmth, understanding, and personal reflections:</strong>
        </p>
        <ul style="color: #CBD5E1; font-size: 14px; line-height: 1.8;">
            <li>📖 <strong>Private Daily Journal:</strong> 100% private, editable reflection vault.</li>
            <li>✨ <strong>Comforting Words & Smile Stories:</strong> Uplifting short stories.</li>
            <li>🤝 <strong>One Small Connection Step:</strong> Simple daily micro-goals.</li>
            <li>💌 <strong>Personal Affirmations:</strong> Write and save your own self-care quotes.</li>
            <li>🔒 <strong>Private & Secure:</strong> Only you can view, edit, or delete your entries.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    if st.button("🤝 Enter Loneliness & Connection Space", use_container_width=True, key="btn_go_lon"):
        st.switch_page("pages/5.3_Loneliness.py")

st.divider()

# Quick Navigation to Dashboard
col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
with col_d2:
    if st.button("📊 Go to My Personal Dashboard", use_container_width=True, key="choose_dash_btn"):
        st.switch_page("pages/User_Dashboard.py")