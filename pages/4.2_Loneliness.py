"""
pages/4.2_Loneliness.py - Loneliness Assessment for Heal-Together
Demonstrates Python syllabus concepts:
- Day 2: Arithmetic, comparison, and logical operators
- Day 3: Conditional statements
- Day 4: Loops over question lists
- Day 6: Lists
- Day 7: Tuples
- Day 9-10: Dictionaries
- Day 11: Functions and return values
- Day 17-22: OOP (LonelinessAssessment class instance, polymorphism)
- Day 26: Streamlit forms and session state
- Day 27: Data validation
- Day 29: Project integration
"""

import streamlit as st
import auth
import database as db
from assessments import LonelinessAssessment

# Configure Page
st.set_page_config(
    page_title="Loneliness Assessment",
    page_icon="🫂",
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

# Instantiate OOP Assessment Object (Day 17-22)
loneliness_model = LonelinessAssessment()

# ============================================================
# PAGE TITLE
# ============================================================
st.title("🫂 Loneliness Assessment")
st.write(f"Welcome, **{user_name}** 🤍")
st.write('🌿 *"Take a moment to listen to your heart and notice how connected and supported you feel."*')
st.info('🌸 *"Loneliness is a feeling, not your identity. You are worthy of genuine connection and care."*')
st.divider()

if "lon_submitted" not in st.session_state:
    st.session_state["lon_submitted"] = False

# ============================================================
# STATE 1: QUESTIONNAIRE (Day 4: Loops & Day 6: Lists)
# ============================================================
if not st.session_state["lon_submitted"]:
    options = [
        "💚 Connected / Rarely",
        "🌱 A little / Sometimes",
        "🌿 Moderately / Often",
        "💙 Quite often",
        "🫂 Almost always"
    ]
    option_weights = {
        "💚 Connected / Rarely": 0,
        "🌱 A little / Sometimes": 1,
        "🌿 Moderately / Often": 2,
        "💙 Quite often": 3,
        "🫂 Almost always": 4
    }

    questions = [
        "1. Do you wish you had someone who truly understood your thoughts and feelings?",
        "2. Do you sometimes feel lonely, even when you are around other people?",
        "3. Do you feel emotionally distant from the people in your daily life?",
        "4. When your heart feels heavy, do you have someone trustworthy you can talk to?",
        "5. Do you feel a genuine sense of belonging with your friends, family, or community?"
    ]

    st.subheader("💙 Answer honestly — there are no wrong feelings")

    user_answers = []
    for idx, q_text in enumerate(questions):
        ans = st.radio(
            q_text,
            options,
            index=None,
            key=f"lon_q_{idx}"
        )
        user_answers.append(ans)

    st.divider()

    if st.button("Submit Assessment", use_container_width=True, key="lon_submit_btn"):
        if any(a is None for a in user_answers):
            st.warning("💙 Take your time — please answer all five questions before submitting.")
        else:
            raw_scores = [option_weights[a] for a in user_answers]

            # Calculate score using OOP Assessment Method (Day 21: Polymorphism)
            score = loneliness_model.calculate_score(raw_scores)
            interpretation = loneliness_model.get_interpretation(score)

            # Save into SQLite database (Day 29)
            db.save_assessment_result(
                user_id=user_id,
                username=user_name,
                assessment_type=loneliness_model.assessment_type,
                loneliness_score=score,
                total_score=score,
                interpretation=interpretation
            )

            st.session_state["lon_result"] = {
                "score": score,
                "interpretation": interpretation
            }
            st.session_state["lon_submitted"] = True
            st.rerun()

# ============================================================
# STATE 2: RESULTS & THANK YOU -> WELLNESS HUB
# ============================================================
else:
    result = st.session_state.get("lon_result", {})
    score = result.get("score", 0)
    interpretation = result.get("interpretation", "")

    st.success("✅ Your Loneliness assessment result has been saved successfully.")

    st.subheader("🫂 Loneliness Assessment Result")
    st.write(f"### 💙 Connection Score: {score} / {loneliness_model.max_score}")
    st.write(f"**Interpretation:** {interpretation}")

    st.divider()

    if score <= 4:
        st.success("🌿 You Feel Connected")
        st.info("""
### 💌 A Note for You
> *"May you always have someone to laugh with, someone to talk to, and someone who reminds you that you belong."* 🤍
""")
    elif score <= 8:
        st.info("🌱 Your Heart May Need More Connection")
        st.info("""
### 💌 A Note for You
> *"You don't need a crowd to feel connected. Sometimes one honest conversation with the right person can make the heart feel lighter."* 🤍
""")
    elif score <= 12:
        st.info("🫂 Your Heart Deserves to Be Heard")
        st.info("""
### 💌 A Note for You
> *"Feeling lonely can be heavy, but you don't have to carry it quietly. Let someone you trust know how your heart is feeling."* ❤️
""")
    elif score <= 16:
        st.warning("💙 Your Heart May Be Feeling Heavy")
        st.info("""
### 💌 A Note for You
> *"Even when you feel forgotten or distant, your presence still matters. There is nothing wrong with wanting someone beside you."* 🫂
""")
    else:
        st.error("🌙 You Don't Have to Face This Alone")
        st.info("""
### 💌 A Note for You
> *"You were never meant to carry every feeling by yourself. When the silence feels heavy, let a trusted person be there with you."* 🤍
""")

    # Non-diagnostic disclaimer from OOP model
    st.divider()
    st.caption(loneliness_model.get_disclaimer())

    st.write("")
    # PROMINENT THANK YOU BUTTON -> GOES TO SUPPORT & REFLECTION (pages/5_choose.py)
    if st.button("💚 Thank You", use_container_width=True, key="lon_thank_you_btn"):
        st.session_state["lon_submitted"] = False
        st.switch_page("pages/5_choose.py")

    st.write("")
    st.subheader("✨ Your Wellness Journey — Quick Shortcuts")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Go to My Dashboard", use_container_width=True, key="lon_dash_btn"):
            st.switch_page("pages/User_Dashboard.py")
    with col2:
        if st.button("🤝 Loneliness & Connection", use_container_width=True, key="lon_conn_btn"):
            st.switch_page("pages/5.3_Loneliness.py")
    with col3:
        if st.button("🧠 Mental Health Tools", use_container_width=True, key="lon_well_btn"):
            st.switch_page("pages/5.1_MentalHealth.py")

    st.write("")
    if st.button("🔄 Retake This Assessment", key="lon_retake_btn"):
        st.session_state["lon_submitted"] = False
        st.rerun()