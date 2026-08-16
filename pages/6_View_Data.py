"""
pages/6_View_Data.py - System Administration Dashboard for Heal-Together
Demonstrates Python syllabus concepts:
- Day 4: Loops
- Day 6: Lists
- Day 7: Tuples
- Day 9-10: Dictionaries
- Day 11: Functions
- Day 12: Multiple returns where useful
- Day 14: Lambda functions for filtering & sorting
- Day 28: Streamlit display features (metrics, tables, tabs)
- Day 29: Project integration
- Day 30: Deployment & administrative security
"""

import streamlit as st
import pandas as pd
import auth
import database as db

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="🛡️",
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
    height: 46px;
    font-size: 15px;
    font-weight: 600;
    border: none;
}
.stButton > button:hover {
    background-color: #4E9447;
    color: white;
}
.admin-metric-card {
    background-color: #161B22;
    border-radius: 8px;
    padding: 16px;
    border: 1px solid #30363D;
    border-top: 3px solid #66B35A;
}
</style>
""", unsafe_allow_html=True)

# STRICT ROLE-BASED ACCESS CONTROL GUARD (Day 29: Security)
auth.require_admin()

admin_name = auth.get_current_user_name()

# PAGE HEADER
st.title("🛡️ System Administration Dashboard")
st.write(f"Logged in as Administrator: **{admin_name}** | Confidential Analytics & Management Console")
st.divider()

# TABBED INTERFACE
tab_overview, tab_users, tab_assessments, tab_drilldown = st.tabs([
    "📊 Overview & Analytics",
    "👥 User Directory",
    "📋 Assessment Records",
    "🔍 User Inspection"
])


# ====================================================================
# TAB 1: OVERVIEW & ANALYTICS (Day 28: Metrics)
# ====================================================================
with tab_overview:
    st.subheader("System Overview Metrics")
    stats = db.get_admin_analytics()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Registered Users", stats["total_users"])
    with col2:
        st.metric("Total Assessments", stats["total_assessments"])
    with col3:
        st.metric("Mood Entries Logged", stats["total_moods"])
    with col4:
        st.metric("Private Journal Entries", stats["total_journals"])

    st.write("")
    st.subheader("Assessments Breakdown by Category")

    col_b1, col_b2, col_b3, col_b4 = st.columns(4)
    with col_b1:
        st.metric("🧠 Mental Health", stats["mental_health_count"])
    with col_b2:
        st.metric("🫂 Loneliness", stats["loneliness_count"])
    with col_b3:
        st.metric("💙 Combined (Both)", stats["both_count"])
    with col_b4:
        st.metric("🤔 General Wellbeing", stats["not_sure_count"])


# ====================================================================
# TAB 2: USER DIRECTORY
# ====================================================================
with tab_users:
    st.subheader("👥 Registered Users Directory")

    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search_query = st.text_input("🔍 Search by Name or Email", placeholder="Type user name or email...", key="admin_user_search")
    with col_filter:
        user_type_filter = st.selectbox(
            "Filter by User Type",
            ["All", "School Student", "College Student", "Employee", "Senior Citizen"],
            key="admin_user_type_filter"
        )

    users_list = db.get_all_users(search_query=search_query, user_type_filter=user_type_filter)

    if users_list:
        st.success(f"✅ {len(users_list)} registered user(s) found.")
        df_users = pd.DataFrame(users_list)
        df_users_display = df_users[[
            "id", "full_name", "email", "user_type", "age", "gender", "category", "created_at"
        ]].rename(columns={
            "id": "User ID",
            "full_name": "Full Name",
            "email": "Email Address",
            "user_type": "Registered Type",
            "age": "Age",
            "gender": "Gender",
            "category": "Profile Category",
            "created_at": "Registration Date"
        })
        st.dataframe(df_users_display, hide_index=True, use_container_width=True)
    else:
        st.info("No registered users match your criteria.")


# ====================================================================
# TAB 3: ASSESSMENT RECORDS
# ====================================================================
with tab_assessments:
    st.subheader("📋 Assessment Results Registry")

    col_at1, col_at2 = st.columns([1, 2])
    with col_at1:
        assess_filter = st.selectbox(
            "Filter by Assessment Type",
            ["All", "Mental Health", "Loneliness", "Both", "Not Sure"],
            key="admin_assess_type_filter"
        )

    all_assessments = db.get_assessment_results(assessment_type=assess_filter)

    if all_assessments:
        st.success(f"✅ {len(all_assessments)} assessment record(s) found.")
        df_assess = pd.DataFrame(all_assessments)
        df_assess_display = df_assess[[
            "id", "username", "email", "assessment_type",
            "mental_health_score", "loneliness_score", "wellbeing_score",
            "total_score", "interpretation", "assessment_date", "assessment_time"
        ]].rename(columns={
            "id": "Record ID",
            "username": "User Name",
            "email": "User Email",
            "assessment_type": "Assessment Type",
            "mental_health_score": "Mental Health",
            "loneliness_score": "Loneliness",
            "wellbeing_score": "Well-Being",
            "total_score": "Total Score",
            "interpretation": "Interpretation",
            "assessment_date": "Date",
            "assessment_time": "Time"
        })
        st.dataframe(df_assess_display, hide_index=True, use_container_width=True)

        # Download CSV option
        csv_data = df_assess_display.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download Assessment Records as CSV",
            data=csv_data,
            file_name="heal_together_assessment_records.csv",
            mime="text/csv"
        )
    else:
        st.info("No assessment records found.")


# ====================================================================
# TAB 4: USER INSPECTION & DRILLDOWN (Day 4: Loops & Day 9-10)
# ====================================================================
with tab_drilldown:
    st.subheader("🔍 Individual User Inspection")

    all_registered = db.get_all_users()
    if all_registered:
        user_choices = {f"{u['full_name']} ({u['email']}) — ID: {u['id']}": u['id'] for u in all_registered}
        selected_user_label = st.selectbox("Select a User to Inspect:", list(user_choices.keys()), key="drilldown_user_select")
        selected_user_id = user_choices[selected_user_label]

        details = db.get_user_drilldown_data(selected_user_id)

        if details and details["user"]:
            u_info = details["user"]
            p_info = details["personal_info"]
            a_list = details["assessments"]
            m_list = details["moods"]

            st.write("---")
            col_u1, col_u2 = st.columns(2)

            with col_u1:
                st.write("### 👤 User Account Details")
                st.write(f"• **User ID:** {u_info['id']}")
                st.write(f"• **Name:** {u_info['full_name']}")
                st.write(f"• **Email:** {u_info['email']}")
                st.write(f"• **Account Type:** {u_info['user_type']}")
                st.write(f"• **Registered At:** {u_info['created_at']}")

            with col_u2:
                st.write("### 📋 Personal Profile Form Data")
                if p_info:
                    st.write(f"• **Age:** {p_info.get('age', 'N/A')}")
                    st.write(f"• **Gender:** {p_info.get('gender', 'N/A')}")
                    st.write(f"• **Category:** {p_info.get('category', 'N/A')}")
                    st.write(f"• **Saved At:** {p_info.get('saved_at', 'N/A')}")
                else:
                    st.info("User has not submitted personal information form yet.")

            st.write("### 📊 Assessment History for this User")
            if a_list:
                df_u_assess = pd.DataFrame(a_list)[[
                    "assessment_type", "total_score", "interpretation", "assessment_date", "assessment_time"
                ]].rename(columns={
                    "assessment_type": "Assessment Type",
                    "total_score": "Score",
                    "interpretation": "Interpretation",
                    "assessment_date": "Date",
                    "assessment_time": "Time"
                })
                st.dataframe(df_u_assess, hide_index=True, use_container_width=True)
            else:
                st.info("No assessments completed by this user.")

            st.write("### 🌸 Recent Mood Activity")
            if m_list:
                for m in m_list:
                    n_str = f" (*{m['note']}*)" if m.get("note") else ""
                    st.write(f"• **{m['logged_date']} ({m['logged_time']}):** {m['mood']}{n_str}")
            else:
                st.info("No mood entries for this user.")
    else:
        st.info("No users registered yet.")