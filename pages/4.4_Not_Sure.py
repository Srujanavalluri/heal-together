"""
pages/4.4_Not_Sure.py - General Well-Being Check-In for Heal-Together
Demonstrates Python syllabus concepts:
- Day 1: Variables and input
- Day 2: Comparison and logical operators
- Day 3: if, if-elif, and nested conditions
- Day 4: Loops
- Day 5: Strings
- Day 6: Lists
- Day 7: Tuples
- Day 9-10: Dictionaries
- Day 11: Functions and return statements
- Day 17-22: OOP (GeneralWellbeingAssessment class instance, polymorphism)
- Day 24: Streamlit project navigation
- Day 26: Streamlit session state
- Day 27: Data validation
- Day 29: Project integration
"""

import streamlit as st
import auth
import database as db
from assessments import GeneralWellbeingAssessment

# Configure Page
st.set_page_config(
    page_title="General Well-Being Check-In",
    page_icon="🤔",
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

# Instantiate OOP Wellbeing Assessment Model (Day 17-22)
wellbeing_model = GeneralWellbeingAssessment()

# ============================================================
# PAGE TITLE
# ============================================================
st.title("🤔 General Well-Being Check-In")
st.write(f"Welcome, **{user_name}** 🌿")
st.write('🫂 *"Whatever you’re feeling is worth understanding. Take a quiet moment to listen to your heart and be honest with yourself."*')
st.info('🌙 *"You don’t have to figure everything out today. Take a breath, check in with yourself, and go gently."*')
st.divider()

if "ns_submitted" not in st.session_state:
    st.session_state["ns_submitted"] = False

# ============================================================
# STATE 1: QUESTIONNAIRE (Day 4: Loops & Day 6: Lists)
# ============================================================
if not st.session_state["ns_submitted"]:
    options = [
        "🤍 None / Rarely",
        "🌱 Mild / A little",
        "🌿 Moderate / Unsure",
        "💙 Noticeable / Often",
        "🫂 Strong / Almost always"
    ]
    option_weights = {
        "🤍 None / Rarely": 0,
        "🌱 Mild / A little": 1,
        "🌿 Moderate / Unsure": 2,
        "💙 Noticeable / Often": 3,
        "🫂 Strong / Almost always": 4
    }

    questions = [
        "1. How often have you felt emotionally overwhelmed recently?",
        "2. How often have you found it difficult to enjoy your usual activities?",
        "3. How often have you felt stressed by things happening in your daily life?",
        "4. How comfortable do you feel talking about your feelings with someone you trust?",
        "5. How connected do you feel to the people around you?",
        "6. How often do you wish you had someone to talk to or spend time with?",
        "7. How supported do you feel by the people around you?",
        "8. How difficult has it been to manage your usual daily activities recently?",
        "9. How often have you felt hopeful about the days ahead?",
        "10. How would you describe your overall emotional energy and social balance right now?"
    ]

    st.subheader("✨ There Are No Right or Wrong Feelings")

    user_answers = []
    for idx, q_text in enumerate(questions):
        ans = st.radio(q_text, options, index=None, key=f"ns_q_{idx}")
        user_answers.append(ans)

    st.divider()

    if st.button("Submit Check-In", use_container_width=True, key="ns_submit_btn"):
        if any(a is None for a in user_answers):
            st.warning("🫂 Your answers matter. Please complete all ten questions before submitting.")
        else:
            raw_scores = [option_weights[a] for a in user_answers]

            # Calculate score using OOP Assessment Method (Day 21: Polymorphism)
            score = wellbeing_model.calculate_score(raw_scores)
            interpretation = wellbeing_model.get_interpretation(score)

            # Determine Personalized Recommendation (Day 3: Conditions)
            if score <= 8:
                recommendation = "General Well-Being & Daily Self-Care"
            elif score <= 16:
                recommendation = "Mental Wellness & Mindful Breathing"
            elif score <= 24:
                recommendation = "Loneliness & Connection Support"
            else:
                recommendation = "Combined Support & Reflection"

            # Save into SQLite database (Day 29)
            db.save_assessment_result(
                user_id=user_id,
                username=user_name,
                assessment_type=wellbeing_model.assessment_type,
                wellbeing_score=score,
                total_score=score,
                interpretation=f"{interpretation} | Recommended Focus: {recommendation}"
            )

            st.session_state["ns_result"] = {
                "score": score,
                "interpretation": interpretation,
                "recommendation": recommendation
            }
            st.session_state["ns_submitted"] = True
            st.rerun()

# ============================================================
# STATE 2: RESULTS & THANK YOU -> WELLNESS HUB
# ============================================================
else:
    result = st.session_state.get("ns_result", {})
    score = result.get("score", 0)
    interpretation = result.get("interpretation", "")
    rec = result.get("recommendation", "General Wellness")

    st.success("✅ Your Well-being Check-In result has been saved successfully.")

    st.subheader("🌿 Your Well-Being Check-In Result")
    st.write(f"### 💙 Self-Reflection Score: {score} / {wellbeing_model.max_score}")
    st.write(f"**Interpretation:** {interpretation}")
    st.write(f"**Suggested Wellness Focus:** 🌟 `{rec}`")

    st.divider()

    if score <= 8:
        st.success("💙 You’re Finding Your Balance")
        st.info("""
### 💌 A Note for You
> *"Keep listening to yourself, celebrating the little joys, and making space for the people who matter."* 🤍
""")
    elif score <= 16:
        st.info("✨ Something in You Deserves Attention")
        st.info("""
### 💌 A Note for You
> *"You may not know exactly what you’re feeling yet—and that’s okay. Start by listening to yourself gently."* 🌱
""")
    elif score <= 24:
        st.info("🌙 Give Your Feelings Some Space")
        st.info("""
### 💌 A Note for You
> *"Whatever your heart is carrying, you don’t have to figure it out all at once. Take it one moment at a time."* ❤️
""")
    elif score <= 32:
        st.warning("🌙 You Don't Have to Carry It Alone")
        st.info("""
### 💌 A Note for You
> *"Some feelings become easier when they are shared. Let someone you trust walk beside you."* 🤍
""")
    else:
        st.error("🫂 Your Feelings Are Heavy Right Now")
        st.info("""
### 💌 A Note for You
> *"You have been carrying feelings that deserve to be seen, not hidden. Give yourself permission to slow down."* 💙
""")

    # Non-diagnostic disclaimer from OOP model
    st.divider()
    st.caption(wellbeing_model.get_disclaimer())

    st.write("")
    # PROMINENT THANK YOU BUTTON -> GOES TO SUPPORT & REFLECTION (pages/5_choose.py)
    if st.button("💚 Thank You", use_container_width=True, key="ns_thank_you_btn"):
        st.session_state["ns_submitted"] = False
        st.switch_page("pages/5_choose.py")

    st.write("")
    st.subheader("✨ Your Wellness Journey — Quick Shortcuts")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Go to My Dashboard", use_container_width=True, key="ns_dash_btn"):
            st.switch_page("pages/User_Dashboard.py")
    with col2:
        if st.button("🧠 Mental Health Tools", use_container_width=True, key="ns_well_btn"):
            st.switch_page("pages/5.1_MentalHealth.py")
    with col3:
        if st.button("🤝 Loneliness & Connection", use_container_width=True, key="ns_conn_btn"):
            st.switch_page("pages/5.3_Loneliness.py")

    st.write("")
    if st.button("🔄 Retake This Assessment", key="ns_retake_btn"):
        st.session_state["ns_submitted"] = False
        st.rerun()