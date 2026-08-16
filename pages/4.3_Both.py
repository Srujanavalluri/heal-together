"""
pages/4.3_Both.py - Combined Assessment for Heal-Together
Demonstrates Python syllabus concepts:
- Day 2: Operators
- Day 3: Conditional statements
- Day 4: Loops
- Day 6: Lists
- Day 7: Tuples
- Day 9-10: Dictionaries
- Day 11: Functions
- Day 12: Multiple return values (mental_score, loneliness_score, total_score)
- Day 17-22: OOP (CombinedAssessment class instance, composition, polymorphism)
- Day 26: Streamlit forms and session state
- Day 27: Data validation
- Day 29: Project integration
"""

import streamlit as st
import auth
import database as db
from assessments import CombinedAssessment

# Configure Page
st.set_page_config(
    page_title="Mental Health & Loneliness Assessment",
    page_icon="💙",
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

# Instantiate OOP Combined Assessment Model (Day 17-22)
combined_model = CombinedAssessment()

# ============================================================
# PAGE TITLE
# ============================================================
st.title("💙 Combined Assessment")
st.write(f"Welcome, **{user_name}** ✨")
st.write('🤍 *"Give yourself a quiet moment to listen to your heart and understand what you have been carrying."*')
st.info('❤️ *"You don’t need all the answers right now. Be honest with yourself, take a breath, and remember that your feelings matter."*')
st.divider()

if "both_submitted" not in st.session_state:
    st.session_state["both_submitted"] = False

# ============================================================
# STATE 1: QUESTIONNAIRE (Day 4: Loops & Day 6: Lists)
# ============================================================
if not st.session_state["both_submitted"]:
    options = [
        "🤍 Not at all",
        "🌱 A little",
        "🌿 Sometimes",
        "💙 Quite often",
        "🫂 Very often"
    ]
    option_weights = {
        "🤍 Not at all": 0,
        "🌱 A little": 1,
        "🌿 Sometimes": 2,
        "💙 Quite often": 3,
        "🫂 Very often": 4
    }

    mh_questions = [
        "1. How often have you felt down, sad, or emotionally low recently?",
        "2. How often have you had little interest or enjoyment in the things you normally like?",
        "3. How often have you felt worried, nervous, or unable to relax?",
        "4. How often have you found it difficult to manage your daily activities because of how you feel?",
        "5. How often have you felt hopeful and positive about the days ahead?"
    ]

    lon_questions = [
        "6. How often do you feel that you lack companionship or a close confidant?",
        "7. How often do you feel left out or overlooked by the people around you?",
        "8. How often do you feel emotionally isolated from other people?",
        "9. How often do you feel that there is no one you can turn to when you need someone to talk to?",
        "10. How often do you feel disconnected even when you are around other people?"
    ]

    # MENTAL HEALTH SECTION
    st.header("🧠 Part 1: Emotional & Mental Well-Being")
    st.write("Please reflect on how your inner self has been feeling recently.")

    mh_answers = []
    for idx, q_text in enumerate(mh_questions):
        ans = st.radio(q_text, options, index=None, key=f"both_mh_q_{idx}")
        mh_answers.append(ans)

    st.divider()

    # LONELINESS SECTION
    st.header("🫂 Part 2: Loneliness & Social Connection")
    st.write("Now reflect on your relationships, companionship, and feelings of belonging.")

    lon_answers = []
    for idx, q_text in enumerate(lon_questions):
        ans = st.radio(q_text, options, index=None, key=f"both_lon_q_{idx}")
        lon_answers.append(ans)

    st.divider()

    if st.button("Submit Combined Assessment", use_container_width=True, key="both_submit_btn"):
        if any(a is None for a in mh_answers) or any(a is None for a in lon_answers):
            st.warning("🫂 Your answers help us understand your feelings better. Please complete all ten questions.")
        else:
            all_raw = [option_weights[a] for a in mh_answers + lon_answers]

            # Calculate scores using OOP Combined Method (Day 12: Multiple Returns & Day 21: Polymorphism)
            mental_score, loneliness_score, total_score = combined_model.calculate_score(all_raw)
            interpretation = combined_model.get_interpretation(total_score)

            # Save result to database (Day 29)
            db.save_assessment_result(
                user_id=user_id,
                username=user_name,
                assessment_type=combined_model.assessment_type,
                mental_health_score=mental_score,
                loneliness_score=loneliness_score,
                total_score=total_score,
                interpretation=interpretation
            )

            st.session_state["both_result"] = {
                "mental_score": mental_score,
                "loneliness_score": loneliness_score,
                "total_score": total_score,
                "interpretation": interpretation
            }
            st.session_state["both_submitted"] = True
            st.rerun()

# ============================================================
# STATE 2: RESULTS & THANK YOU -> WELLNESS HUB
# ============================================================
else:
    result = st.session_state.get("both_result", {})
    mental_score = result.get("mental_score", 0)
    loneliness_score = result.get("loneliness_score", 0)
    total_score = result.get("total_score", 0)
    interpretation = result.get("interpretation", "")

    st.success("✅ Your Combined Assessment result has been saved successfully.")

    st.subheader("📊 Assessment Summary")
    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        st.metric("Mental Health Score", f"{mental_score} / 20")
    with col_res2:
        st.metric("Loneliness Score", f"{loneliness_score} / 20")
    with col_res3:
        st.metric("Total Combined Score", f"{total_score} / {combined_model.max_score}")

    st.write(f"**Interpretation:** {interpretation}")
    st.divider()

    st.subheader("🧠 Mental Health Reflection")
    if mental_score <= 4:
        st.success("🌞 You're maintaining a healthy inner balance.")
    elif mental_score <= 8:
        st.info("🫂 Take Care of Your Heart: Be gentle with yourself today.")
    elif mental_score <= 12:
        st.info("🌧️ It’s Okay to Feel Heavy: Give your mind quiet space to rest.")
    elif mental_score <= 16:
        st.warning("🌙 Your Mind Needs a Pause: You don't have to be strong every single moment.")
    else:
        st.error("❤️ Please Reach Out: Consider talking to a trusted friend or mentor.")

    st.subheader("🫂 Loneliness Reflection")
    if loneliness_score <= 4:
        st.success("🫂 Your Heart Feels Connected and Supported.")
    elif loneliness_score <= 8:
        st.info("🌱 You Deserve Connection: One genuine conversation can make a big difference.")
    elif loneliness_score <= 12:
        st.info("🌙 You Don't Have to Stay Quiet: Let someone know how you feel.")
    elif loneliness_score <= 16:
        st.warning("🫂 You Deserve a Safe Connection: Give yourself permission to reach out.")
    else:
        st.error("🌙 You Don't Have to Carry the Silence Alone: Let a trusted person into your world.")

    # Non-diagnostic disclaimer from OOP model
    st.divider()
    st.caption(combined_model.get_disclaimer())

    st.write("")
    # PROMINENT THANK YOU BUTTON -> GOES TO SUPPORT & REFLECTION (pages/5_choose.py)
    if st.button("💚 Thank You", use_container_width=True, key="both_thank_you_btn"):
        st.session_state["both_submitted"] = False
        st.switch_page("pages/5_choose.py")

    st.write("")
    st.subheader("✨ Your Wellness Journey — Quick Shortcuts")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Go to My Dashboard", use_container_width=True, key="both_dash_btn"):
            st.switch_page("pages/User_Dashboard.py")
    with col2:
        if st.button("🧠 Mental Health Tools", use_container_width=True, key="both_well_btn"):
            st.switch_page("pages/5.1_MentalHealth.py")
    with col3:
        if st.button("🤝 Loneliness & Connection", use_container_width=True, key="both_conn_btn"):
            st.switch_page("pages/5.3_Loneliness.py")

    st.write("")
    if st.button("🔄 Retake This Assessment", key="both_retake_btn"):
        st.session_state["both_submitted"] = False
        st.rerun()