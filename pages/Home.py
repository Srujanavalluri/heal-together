"""
pages/Home.py - Landing Page for Heal-Together
Demonstrates Python syllabus concepts:
- Day 1: Variables, strings, and data types
- Day 5: Strings and string methods
- Day 6: Lists
- Day 9-10: Dictionaries for feature organization
- Day 11: Functions
- Day 24: Streamlit project setup
- Day 28: Streamlit display features
- Day 29: Project integration
"""

import streamlit as st
import auth

# Configure Page
st.set_page_config(
    page_title="Heal-Together",
    page_icon="🌿",
    layout="wide"
)

# Custom Styling - Calm, dark theme with serene green accents
st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
}
.stButton > button {
    background-color: #66B35A;
    color: white;
    border-radius: 10px;
    height: 52px;
    font-size: 17px;
    font-weight: 600;
    border: none;
}
.stButton > button:hover {
    background-color: #4E9447;
    color: white;
}
.hero-card {
    background-color: #161B22;
    border: 1px solid #30363D;
    border-radius: 12px;
    padding: 26px;
    border-top: 4px solid #66B35A;
    margin-bottom: 20px;
}
.feature-tile {
    background-color: #161B22;
    border: 1px solid #30363D;
    border-radius: 10px;
    padding: 18px;
    height: 100%;
    margin-bottom: 12px;
}
blockquote {
    border-left: 3px solid #66B35A;
    padding-left: 15px;
    color: #CBD5E1;
}
</style>
""", unsafe_allow_html=True)

# Check login state
logged_in = auth.is_logged_in()
user_name = auth.get_current_user_name() if logged_in else "Friend"

# ====================================================================
# HERO SECTION (Top Starting Section)
# ====================================================================
st.markdown("""
<div class="hero-card">
    <h1 style="color: #66B35A; margin-bottom: 4px;">🌿 Heal-Together</h1>
    <h3 style="color: #F5F5F5; margin-top: 0;">Emotional Wellness & Social Connection Platform</h3>
    <p style="color: #A0AEC0; font-size: 16px; line-height: 1.6;">
        A calm, compassionate space designed to help individuals, students, and professionals
        reflect on their thoughts, navigate feelings of loneliness, and build gentle daily wellness habits.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
> *"Welcome, {user_name}. Whatever you are carrying today, remember that your feelings are valid,
> and you don't have to navigate everything alone. Take one gentle step forward."* ✨
""")

# ====================================================================
# PROMINENT "GET STARTED" ACTION BUTTONS AT THE VERY START
# ====================================================================
st.write("")
col_top1, col_top2, col_top3 = st.columns([1, 2, 1])

with col_top2:
    if not logged_in:
        col_gs1, col_gs2 = st.columns(2)
        with col_gs1:
            # 🚀 GET STARTED BUTTON AT THE VERY START
            if st.button("🚀 GET STARTED", use_container_width=True, key="top_get_started_btn"):
                st.switch_page("pages/1_Register.py")
        with col_gs2:
            if st.button("🔑 LOGIN", use_container_width=True, key="top_login_btn"):
                st.switch_page("pages/2_login.py")
    else:
        col_gs1, col_gs2 = st.columns(2)
        with col_gs1:
            if st.button("📊 MY DASHBOARD", use_container_width=True, key="top_dash_btn"):
                st.switch_page("pages/User_Dashboard.py")
        with col_gs2:
            if st.button("🌿 TAKE ASSESSMENT", use_container_width=True, key="top_assess_btn"):
                st.switch_page("pages/4_Assessment.py")

st.divider()

# ====================================================================
# FEATURES CATALOG (Day 9-10: Dictionaries & Day 6: Lists)
# ====================================================================
st.subheader("✨ What You Can Do in Heal-Together")

features = [
    {
        "icon": "🧠",
        "title": "Mental Health Check",
        "desc": "A gentle 5-question reflection tool to gauge emotional balance and mental energy."
    },
    {
        "icon": "🫂",
        "title": "Loneliness Check",
        "desc": "Reflect on feelings of connection, belonging, and social support in a safe environment."
    },
    {
        "icon": "💙",
        "title": "Combined Assessment",
        "desc": "A comprehensive self-awareness check combining emotional wellness and social connectivity."
    },
    {
        "icon": "🤔",
        "title": "General Wellbeing",
        "desc": "An intuitive guide for users seeking gentle direction when they are unsure what they feel."
    },
    {
        "icon": "📊",
        "title": "Personal Dashboard",
        "desc": "Visual wave trends, daily mood journey, and your complete assessment reflection history."
    },
    {
        "icon": "📖",
        "title": "Private Daily Journal",
        "desc": "A 100% private, secure reflection vault for your personal thoughts, with easy edit/delete."
    }
]

# Display features in responsive 3-column grid (Day 4: Loops & Day 6: Lists)
col_a, col_b, col_c = st.columns(3)
columns = [col_a, col_b, col_c]

for idx, feat in enumerate(features):
    target_col = columns[idx % 3]
    with target_col:
        st.markdown(f"""
        <div class="feature-tile">
            <h3 style="color: #66B35A; margin: 0;">{feat['icon']} {feat['title']}</h3>
            <p style="color: #CBD5E1; font-size: 14px; margin-top: 8px; line-height: 1.5;">
                {feat['desc']}
            </p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ====================================================================
# BOTTOM CALL TO ACTION (Day 3: Conditions & Day 24: Navigation)
# ====================================================================
col_cta1, col_cta2, col_cta3 = st.columns([1, 2, 1])

with col_cta2:
    if not logged_in:
        st.write("### Ready to begin your gentle journey?")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🚀 Register & Begin", use_container_width=True, key="home_register_btn"):
                st.switch_page("pages/1_Register.py")
        with col_btn2:
            if st.button("🔑 Log In to Account", use_container_width=True, key="home_login_btn"):
                st.switch_page("pages/2_login.py")
    else:
        st.write("### Continue where you left off:")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("📊 Go to My Dashboard", use_container_width=True, key="home_dash_btn"):
                st.switch_page("pages/User_Dashboard.py")
        with col_btn2:
            if st.button("🌿 Take an Assessment", use_container_width=True, key="home_assess_btn"):
                st.switch_page("pages/4_Assessment.py")