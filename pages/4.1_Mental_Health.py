"""
pages/4.1_Mental_Health.py - Mental Health Assessment for Heal-Together
Demonstrates Python syllabus concepts:
- Day 1: Variables and data types
- Day 2: Arithmetic, comparison, and logical operators
- Day 3: if, if-else, and if-elif conditions
- Day 4: for loops over question collection
- Day 6: Lists
- Day 7: Tuples
- Day 9-10: Dictionaries
- Day 11: Functions and return statements
- Day 17-22: OOP (MentalHealthAssessment class instance, polymorphism)
- Day 26: Streamlit forms and session state
- Day 27: Data validation
- Day 29: Project integration
"""

import streamlit as st
import auth
import database as db
from assessments import MentalHealthAssessment

# Configure Page
st.set_page_config(
    page_title="Mental Health Assessment",
    page_icon="🧠",
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
    font-size: 16px;
    font-weight: 600;
    border: none;
}
.stButton > button:hover {
    background-color: #4E9447;
    color: white;
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

user_id = auth.get_current_user_id()
user_name = auth.get_current_user_name()

# Instantiate OOP Assessment Object (Day 17-22: Classes, Objects, Polymorphism)
assessment_model = MentalHealthAssessment()

# ============================================================
# PAGE TITLE
# ============================================================
st.title("🧠 Mental Health Assessment")
st.write(f"Welcome, **{user_name}** 💙")
st.write("Take a quiet moment to reflect on how your mind and heart have been feeling.")
st.info('❤️ *"Your feelings are valid, your story matters, and this moment is yours to understand yourself."*')
st.divider()

# Session State for Submission
if "mh_submitted" not in st.session_state:
    st.session_state["mh_submitted"] = False

# ============================================================
# STATE 1: QUESTIONNAIRE (Day 4: Loops & Day 6: Lists)
# ============================================================
if not st.session_state["mh_submitted"]:
    options = [
        "🤍 Not really",
        "🌱 A little",
        "🌿 Sometimes",
        "💙 Quite a lot",
        "🫂 Almost always"
    ]
    option_weights = {
        "🤍 Not really": 0,
        "🌱 A little": 1,
        "🌿 Sometimes": 2,
        "💙 Quite a lot": 3,
        "🫂 Almost always": 4
    }

    questions = [
        "1. How often have you felt down, sad, or emotionally low recently?",
        "2. How often have you had little interest or enjoyment in the things you normally like?",
        "3. How often have you felt worried, nervous, or unable to relax?",
        "4. How often have you found it difficult to manage your daily activities because of how you feel?",
        "5. How often have you felt hopeful and positive about the days ahead?"
    ]

    st.subheader("🌿 Please answer honestly")

    user_answers = []
    # Display questions using loop (Day 4: Loops)
    for idx, q_text in enumerate(questions):
        ans = st.radio(
            q_text,
            options,
            index=None,
            key=f"mh_q_{idx}"
        )
        user_answers.append(ans)

    st.divider()

    if st.button("Submit Assessment", use_container_width=True, key="mh_submit_btn"):
        if any(a is None for a in user_answers):
            st.warning("🤍 Please complete all five questions before submitting.")
        else:
            # Map selected options to numerical values
            raw_scores = [option_weights[a] for a in user_answers]

            # Calculate score using OOP Assessment Method (Day 21: Polymorphism)
            score = assessment_model.calculate_score(raw_scores)
            interpretation = assessment_model.get_interpretation(score)

            # Save result to SQLite database (Day 29)
            db.save_assessment_result(
                user_id=user_id,
                username=user_name,
                assessment_type=assessment_model.assessment_type,
                mental_health_score=score,
                total_score=score,
                interpretation=interpretation
            )

            st.session_state["mh_result"] = {
                "score": score,
                "interpretation": interpretation
            }
            st.session_state["mh_submitted"] = True
            st.rerun()

# ============================================================
# STATE 2: ASSESSMENT RESULT & THANK YOU -> WELLNESS HUB
# ============================================================
else:
    result = st.session_state.get("mh_result", {})
    score = result.get("score", 0)
    interpretation = result.get("interpretation", "")

    st.success("✅ Your Mental Health assessment result has been saved successfully.")

    st.subheader("📝 Assessment Result")
    st.write(f"### 💙 Emotional Reflection Score: {score} / {assessment_model.max_score}")
    st.write(f"**Interpretation:** {interpretation}")

    st.divider()

    # Supportive messages based on score range
    if score <= 4:
        st.success("🌞 You are taking good care of your heart.")
        st.info("""
### 💌 A Note for You
> *"May your heart find the peace, love, and warmth it has been searching for."* ❤️
""")
    elif score <= 8:
        st.info("💙 Your Heart Needs Kindness")
        st.info("""
### 💌 A Note for You
> *"Some days feel heavier than others. Be patient with yourself and remember that even the smallest step forward still matters."* 🌸
""")
    elif score <= 12:
        st.info("❤️ Be Kind to Your Heart")
        st.info("""
### 💌 A Note for You
> *"You are doing the best you can. Take today gently, and remember that even a tiny step forward is still progress."* 🌸
""")
    elif score <= 16:
        st.warning("❤️ You Don't Have to Carry It Alone")
        st.info("""
### 💌 A Note for You
> *"Some struggles become lighter when they are shared. Reach out, speak honestly, and let yourself be cared for too."* 🌸
""")
    else:
        st.error("🫂 Please Give Yourself More Support")
        st.info("""
### 💌 A Note for You
> *"You don't have to face difficult moments alone. Please consider reaching out to someone you trust. You deserve care and understanding."* 💙
""")

    # Non-diagnostic disclaimer from OOP model
    st.divider()
    st.caption(assessment_model.get_disclaimer())

    st.write("")
    # PROMINENT "THANK YOU" BUTTON -> GOES TO SUPPORT & REFLECTION (pages/5_choose.py)
    if st.button("💚 Thank You", use_container_width=True, key="mh_thank_you_btn"):
        st.session_state["mh_submitted"] = False
        st.switch_page("pages/5_choose.py")

    st.write("")
    st.subheader("✨ Your Wellness Journey — Quick Shortcuts")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Go to My Dashboard", use_container_width=True, key="mh_dash_btn"):
            st.switch_page("pages/User_Dashboard.py")
    with col2:
        if st.button("🧠 Mental Health Tools", use_container_width=True, key="mh_well_btn"):
            st.switch_page("pages/5.1_MentalHealth.py")
    with col3:
        if st.button("🤝 Loneliness & Connection", use_container_width=True, key="mh_conn_btn"):
            st.switch_page("pages/5.3_Loneliness.py")

    st.write("")
    if st.button("🔄 Retake This Assessment", key="mh_retake_btn"):
        st.session_state["mh_submitted"] = False
        st.rerun()