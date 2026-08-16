"""
pages/User_Dashboard.py - Personal User Dashboard for Heal-Together
Demonstrates Python syllabus concepts:
- Day 4: Loops for record processing
- Day 6: Lists
- Day 7: Tuples
- Day 9-10: Dictionaries for user info
- Day 11: Functions
- Day 12: Multiple returns where useful
- Day 14: Lambda functions for simple sorting/formatting
- Day 26: Streamlit session state
- Day 28: Streamlit display features (metrics, charts, cards)
- Day 29: Project integration
"""

import streamlit as st
import pandas as pd
import auth
import database as db

# PAGE CONFIGURATION
st.set_page_config(
    page_title="My Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom Styling - Calm, soothing, dark theme with green accents
st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
}
.stButton > button {
    background-color: #66B35A;
    color: white;
    border-radius: 10px;
    height: 46px;
    font-size: 15px;
    font-weight: 600;
    border: none;
}
.stButton > button:hover {
    background-color: #4E9447;
    color: white;
}
.clean-box {
    background-color: #161B22;
    border: 1px solid #30363D;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 16px;
}
.notification-banner {
    background-color: #161B22;
    border: 1px solid #66B35A;
    border-left: 5px solid #66B35A;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 16px;
}
.mood-tile {
    background-color: #161B22;
    border: 1px solid #30363D;
    border-left: 4px solid #66B35A;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
}
.progress-container {
    background-color: #21262D;
    border-radius: 8px;
    padding: 3px;
    margin: 6px 0;
}
.progress-bar-fill {
    background-color: #66B35A;
    height: 10px;
    border-radius: 6px;
}
blockquote {
    border-left: 3px solid #66B35A;
    padding-left: 15px;
    color: #8F8F8F;
}
</style>
""", unsafe_allow_html=True)

# Guard against unauthenticated access (Day 26)
auth.require_login()

user_id = auth.get_current_user_id()
user_name = auth.get_current_user_name()
user_email = st.session_state.get("username", "")

# Fetch user data strictly for this user (Data Isolation)
personal_info = db.get_personal_information(user_id=user_id)
assessment_history = db.get_assessment_results(user_id=user_id)
latest_assessment = db.get_latest_assessment(user_id=user_id)
mood_history = db.get_mood_entries(user_id=user_id, limit=10)
journal_entries = db.get_journal_entries(user_id=user_id)
wellness_acts = db.get_wellness_activities(user_id=user_id)
user_quotes = db.get_user_quotes(user_id=user_id)
alarms = db.get_alarm_reminders(user_id=user_id)
random_mantra = db.get_random_user_quote(user_id=user_id)

# ====================================================================
# TOP NOTIFICATION BANNER
# ====================================================================
if alarms:
    al = alarms[0]
    st.markdown(f"""
    <div class="notification-banner">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-weight:600; color:#66B35A; font-size:16px;">🔔 Active Reminder: {al['title']}</span>
            <span style="font-size:13px; color:#A0AEC0;">⏰ {al['reminder_time']}</span>
        </div>
        <div style="color:#CBD5E1; font-size:13px; margin-top:4px;">
            <em>Gentle pause scheduled for you.</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ====================================================================
# HEADER & SUMMARY
# ====================================================================
st.title("📊 My Personal Dashboard")
st.subheader(f"Welcome, {user_name} ❤️")

if random_mantra:
    st.write(f"> *\"✨ {random_mantra['quote_text']}\"* — **{random_mantra['author_name']}**")
else:
    st.write(
        "> *\"Here is your personal, private reflection space. "
        "Every small check-in is a quiet step toward taking care of yourself.\"* 🌿"
    )
st.divider()

# ====================================================================
# TOP STATS (Day 28: Metrics)
# ====================================================================
col_s1, col_s2, col_s3, col_s4 = st.columns(4)

with col_s1:
    st.metric("Assessments Taken", len(assessment_history))

with col_s2:
    st.metric("Mood Check-ins", len(mood_history))

with col_s3:
    st.metric("Private Journal Notes", len(journal_entries))

with col_s4:
    st.metric("Personal Mantras", len(user_quotes))

st.write("")

# ====================================================================
# VISUAL EMOTIONAL PROGRESS & MOOD TIMELINE
# ====================================================================
st.header("🌊 Emotional Harmony & Reflection Flow")

col_vis1, col_vis2 = st.columns(2)

with col_vis1:
    st.subheader("📈 Assessment Reflection Trend")
    if assessment_history:
        # Day 14: Lambda for simple transformation
        wave_data = [
            {
                "Session": f"Check-in {idx} ({a['assessment_date']})",
                "Reflection Score": a.get("total_score", 0)
            }
            for idx, a in enumerate(reversed(assessment_history), 1)
        ]
        df_wave = pd.DataFrame(wave_data)
        st.area_chart(df_wave, x="Session", y="Reflection Score", use_container_width=True)
        st.caption("🌊 Smooth reflection wave tracking your assessment scores over time.")
    else:
        st.info("No assessments completed yet. Take an assessment to see your reflection wave.")

with col_vis2:
    st.subheader("🌸 Daily Mood Journey")
    if mood_history:
        for m in mood_history[:5]:
            score_val = m["mood_score"] # 1 to 5
            pct_val = int((score_val / 5.0) * 100)
            note_text = f" — *\"{m['note']}\"*" if m.get("note") else ""

            st.markdown(f"""
            <div class="mood-tile">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:16px; font-weight:600; color:#F5F5F5;">{m['mood']}</span>
                    <span style="font-size:13px; color:#8F8F8F;">📅 {m['logged_date']}</span>
                </div>
                <div class="progress-container">
                    <div class="progress-bar-fill" style="width: {pct_val}%;"></div>
                </div>
                <div style="font-size:13px; color:#CBD5E1; margin-top:4px;">
                    Harmony Level: <strong>{score_val}/5</strong>{note_text}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No mood check-ins recorded yet. Track your mood in Mental Health to see your timeline.")

st.divider()

# ====================================================================
# PROFILE & LATEST RESULT & PERSONAL MANTRAS
# ====================================================================
col_prof, col_res = st.columns(2)

with col_prof:
    st.subheader("👤 My Profile")
    if personal_info:
        st.markdown(f"""
        <div class="clean-box">
            <p><strong>Name:</strong> {personal_info.get('full_name', user_name)}</p>
            <p><strong>Email:</strong> {user_email}</p>
            <p><strong>Age:</strong> {personal_info.get('age', 'N/A')} years</p>
            <p><strong>Gender:</strong> {personal_info.get('gender', 'N/A')}</p>
            <p><strong>Category:</strong> {personal_info.get('category', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("✏️ Edit Profile Info", key="dash_edit_btn"):
            st.switch_page("pages/3_form.py")
    else:
        st.info("Personal profile not completed yet.")
        if st.button("Fill Profile Form", key="dash_fill_btn"):
            st.switch_page("pages/3_form.py")

with col_res:
    st.subheader("🌿 Latest Assessment Summary")
    if latest_assessment:
        st.markdown(f"""
        <div class="clean-box" style="border-left: 4px solid #66B35A;">
            <h4 style="color: #66B35A; margin-top:0;">{latest_assessment.get('assessment_type')}</h4>
            <p style="font-size: 18px; font-weight: 600; margin: 6px 0;">Score: {latest_assessment.get('total_score', 'N/A')}</p>
            <p style="color: #CBD5E1; font-size: 14px;"><strong>Interpretation:</strong> {latest_assessment.get('interpretation', 'Completed')}</p>
            <p style="color: #8F8F8F; font-size: 12px;"><em>Date: {latest_assessment.get('assessment_date')} at {latest_assessment.get('assessment_time')}</em></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No assessments completed yet.")

if user_quotes:
    st.write("---")
    st.subheader("✨ My Personal Motivational Quotes & Affirmations")
    for q in user_quotes[:3]:
        st.markdown(f"""
        <div class="clean-box" style="border-left: 3px solid #66B35A; margin-bottom: 8px;">
            <p style="color:#F5F5F5; font-size:15px; margin:0;"><em>"{q['quote_text']}"</em></p>
            <p style="color:#8F8F8F; font-size:12px; margin-top:4px;">— {q['author_name']} ({q['category']})</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ====================================================================
# PAST ASSESSMENTS TABLE (Day 4: Loops & Day 28: Dataframe)
# ====================================================================
st.subheader("📋 My Assessment Records")

if assessment_history:
    df_history = pd.DataFrame(assessment_history)
    display_cols = [
        "assessment_type",
        "mental_health_score",
        "loneliness_score",
        "wellbeing_score",
        "total_score",
        "interpretation",
        "assessment_date",
        "assessment_time"
    ]
    available_cols = [c for c in display_cols if c in df_history.columns]
    df_show = df_history[available_cols].rename(columns={
        "assessment_type": "Assessment Type",
        "mental_health_score": "Mental Health",
        "loneliness_score": "Loneliness",
        "wellbeing_score": "Well-Being",
        "total_score": "Score",
        "interpretation": "Interpretation",
        "assessment_date": "Date",
        "assessment_time": "Time"
    })
    st.dataframe(df_show, hide_index=True, use_container_width=True)
else:
    st.info("No past assessment records.")

st.divider()

# ====================================================================
# QUICK SHORTCUTS
# ====================================================================
st.subheader("🚀 Quick Shortcuts")
col_q1, col_q2, col_q3 = st.columns(3)

with col_q1:
    if st.button("🧠 Open Mental Health", use_container_width=True, key="quick_mh_btn"):
        st.switch_page("pages/5.1_MentalHealth.py")

with col_q2:
    if st.button("🤝 Open Loneliness & Journal", use_container_width=True, key="quick_lon_btn"):
        st.switch_page("pages/5.3_Loneliness.py")

with col_q3:
    if st.button("🌿 Take an Assessment", use_container_width=True, key="quick_assess_btn"):
        st.switch_page("pages/4_Assessment.py")
