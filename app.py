"""
app.py - Main Entry Point for Heal-Together
Demonstrates Python & Streamlit syllabus concepts:
- Day 1: Variables and data types
- Day 2: Operators
- Day 3: Conditional statements (if, elif, else)
- Day 11: Functions and return statements
- Day 24: Streamlit project setup (st.Page, st.navigation)
- Day 26: Streamlit session state
- Day 29: Project integration
- Day 30: GitHub and Streamlit Cloud deployment
"""

import os
import streamlit as st
from database import create_database
from auth import is_logged_in, is_admin

# -----------------------------------------------------------------------------
# 1. DATABASE INITIALIZATION (Day 29: Project Integration)
# -----------------------------------------------------------------------------
create_database()

# -----------------------------------------------------------------------------
# 2. CROSS-PLATFORM PATH RESOLVER (Day 30: Linux / Streamlit Cloud Compatibility)
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(BASE_DIR, "pages")


def resolve_page_path(rel_path: str) -> str:
    """
    Resolves page file path safely across Windows and Linux (Streamlit Cloud).
    Handles exact match, relative match, and case-insensitive filename matches.
    """
    direct_path = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(direct_path):
        return rel_path

    # Case-insensitive resolution for Linux / GitHub deployments
    target_filename = os.path.basename(rel_path).lower()
    if os.path.exists(PAGES_DIR):
        for fname in os.listdir(PAGES_DIR):
            if fname.lower() == target_filename:
                return f"pages/{fname}"

    return rel_path


# -----------------------------------------------------------------------------
# 3. DEFINE ALL APPLICATION PAGES (Day 24: Streamlit Multi-Page Navigation)
# -----------------------------------------------------------------------------
home_page = st.Page(resolve_page_path("pages/Home.py"), title="Home", icon="🏠", default=True)
register_page = st.Page(resolve_page_path("pages/1_Register.py"), title="Register", icon="📝")
login_page = st.Page(resolve_page_path("pages/2_login.py"), title="Login", icon="🔑")
dashboard_page = st.Page(resolve_page_path("pages/User_Dashboard.py"), title="My Dashboard", icon="📊")
form_page = st.Page(resolve_page_path("pages/3_form.py"), title="Personal Information", icon="👤")
assessment_page = st.Page(resolve_page_path("pages/4_Assessment.py"), title="Assessment Hub", icon="🌿")
mh_page = st.Page(resolve_page_path("pages/4.1_Mental_Health.py"), title="Mental Health Check", icon="🧠")
lonely_page = st.Page(resolve_page_path("pages/4.2_Loneliness.py"), title="Loneliness Check", icon="🫂")
both_page = st.Page(resolve_page_path("pages/4.3_Both.py"), title="Combined Check", icon="💙")
not_sure_page = st.Page(resolve_page_path("pages/4.4_Not_Sure.py"), title="General Wellbeing", icon="🤔")
choose_page = st.Page(resolve_page_path("pages/5_choose.py"), title="Wellness Hub", icon="✨")
mental_health_wellness_page = st.Page(resolve_page_path("pages/5.1_MentalHealth.py"), title="Mental Wellness", icon="🧠")
loneliness_support_page = st.Page(resolve_page_path("pages/5.3_Loneliness.py"), title="Connection Support", icon="🤝")
admin_page = st.Page(resolve_page_path("pages/6_View_Data.py"), title="Admin Dashboard", icon="🛡️")
logout_page = st.Page(resolve_page_path("pages/Logout.py"), title="Logout", icon="🚪")

# -----------------------------------------------------------------------------
# 4. DYNAMIC ROLE-BASED NAVIGATION (Day 3: Conditions, Day 26: Session State)
# -----------------------------------------------------------------------------
if not is_logged_in():
    # Logged-out Guest Navigation
    pg = st.navigation(
        {
            "Get Started": [home_page, register_page, login_page]
        }
    )
elif is_admin():
    # Administrator Navigation
    pg = st.navigation(
        {
            "Administration": [admin_page],
            "Application": [home_page, dashboard_page, logout_page]
        }
    )
else:
    # Authenticated User Navigation
    pg = st.navigation(
        {
            "My Space": [home_page, dashboard_page, form_page],
            "Assessments": [assessment_page, mh_page, lonely_page, both_page, not_sure_page],
            "Support & Reflection": [choose_page, mental_health_wellness_page, loneliness_support_page],
            "Account": [logout_page]
        }
    )

# -----------------------------------------------------------------------------
# 5. REDIRECTION HANDLER (Day 26: Session State State Management)
# -----------------------------------------------------------------------------
if "redirect_target" in st.session_state and st.session_state["redirect_target"]:
    target = st.session_state.pop("redirect_target")
    try:
        resolved_target = resolve_page_path(target)
        st.switch_page(resolved_target)
    except Exception:
        pass

# -----------------------------------------------------------------------------
# 6. EXECUTE CURRENT PAGE
# -----------------------------------------------------------------------------
pg.run()