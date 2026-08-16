"""
pages/Logout.py - Logout Handler for Heal-Together
Demonstrates Python syllabus concepts:
- Day 1: Variables
- Day 3: Conditional statements
- Day 11: Functions
- Day 26: Streamlit session state
- Day 29: Project integration
"""

import streamlit as st
import auth

# Configure Page
st.set_page_config(
    page_title="Logout",
    page_icon="🚪",
    layout="centered"
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
.logout-box {
    background-color: #161B22;
    border: 1px solid #30363D;
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    border-top: 4px solid #66B35A;
}
</style>
""", unsafe_allow_html=True)

# PAGE HEADER & CONFIRMATION
st.markdown("""
<div class="logout-box">
    <h2 style="color: #66B35A; margin-top:0;">🚪 Confirm Logout</h2>
    <p style="color: #CBD5E1; font-size: 16px;">
        Are you sure you want to log out of your Heal-Together account?
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")

col1, col2 = st.columns(2)

with col1:
    if st.button("🚪 Yes, Log Me Out", use_container_width=True, key="logout_confirm_btn"):
        # Day 26: Clear Session State & Logout
        auth.logout_user()
        st.session_state["redirect_target"] = "pages/2_login.py"
        st.success("You have been logged out successfully.")
        st.rerun()

with col2:
    if st.button("🏠 Stay & Return Home", use_container_width=True, key="logout_cancel_btn"):
        st.switch_page("pages/Home.py")
