"""
pages/1_Register.py - User Registration Page for Heal-Together
Demonstrates Python syllabus concepts:
- Day 1: Variables, input and output
- Day 2: Comparison and logical operators
- Day 3: Conditional statements (if, if-else, if-elif)
- Day 5: Strings and string methods (.strip(), in operator)
- Day 9-10: Dictionaries
- Day 11: Functions and return statements
- Day 26: Streamlit forms and session state
- Day 27: Data validation
- Day 29: Project integration
"""

import streamlit as st
import auth

# Configure Page
st.set_page_config(
    page_title="Register",
    page_icon="📝",
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
    color: #8F8F8F;
}
</style>
""", unsafe_allow_html=True)

# If already logged in, offer quick jump to dashboard
if auth.is_logged_in():
    st.info("You are already logged in.")
    if st.button("Go to My Dashboard", key="reg_logged_in_dash"):
        st.switch_page("pages/User_Dashboard.py")
    st.stop()

# ====================================================================
# HEADER
# ====================================================================
st.title("📝 Create Your Account")
st.write("""
### Welcome to Heal-Together 💚
> *"Create your account and begin your journey toward hope, healing, and self-awareness."* 🌿❤️
""")
st.divider()

# Success state handling outside nested buttons (Day 26)
if st.session_state.get("registration_success"):
    reg_name = st.session_state.get("registered_name", "Friend")
    st.success(f"🎉 Registration Successful! Welcome, **{reg_name}**.")
    st.info("Your account is ready. Please log in with your credentials.")
    if st.button("🔑 Proceed to Login Now", use_container_width=True, key="proc_login_btn"):
        st.session_state["registration_success"] = False
        st.switch_page("pages/2_login.py")
    st.stop()

# ====================================================================
# REGISTRATION FORM (Day 26: Streamlit Forms & Day 27: Validation)
# ====================================================================
col1, col2 = st.columns([2, 1])

with col1:
    full_name = st.text_input("👤 Full Name", placeholder="Enter your full name", key="reg_name_in")
    email = st.text_input("📧 Email Address / Username", placeholder="e.g. name@example.com", key="reg_email_in")
    password = st.text_input("🔒 Password", type="password", placeholder="Minimum 6 characters", key="reg_pass_in")
    confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Re-enter your password", key="reg_conf_pass_in")

    user_type = st.selectbox(
        "👥 Select Account Category",
        (
            "School Student",
            "College Student",
            "Employee",
            "Senior Citizen"
        ),
        key="reg_type_sel"
    )

    st.write("")

    # Register Button
    if st.button("REGISTER", use_container_width=True, key="reg_submit_btn"):
        name_clean = full_name.strip()
        email_clean = email.strip()

        # Day 27: Form Validation
        if name_clean == "" or email_clean == "" or password == "" or confirm_password == "":
            st.warning("Please fill in all fields.")
        elif len(name_clean) < 2:
            st.error("Full name must contain at least 2 characters.")
        elif "@" not in email_clean or "." not in email_clean:
            st.error("Please enter a valid email address.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters long.")
        else:
            # Delegate to auth.py (Day 29: Separation of Concerns)
            success, msg, user_id = auth.register_user(
                full_name=name_clean,
                email=email_clean,
                password=password,
                user_type=user_type,
                role="user"
            )

            if success:
                st.session_state["registration_success"] = True
                st.session_state["registered_name"] = name_clean
                st.rerun()
            else:
                st.error(msg)

st.write("---")
st.write("Already have an account?")

if st.button("Back to Login", use_container_width=False, key="back_to_login_btn"):
    st.switch_page("pages/2_login.py")