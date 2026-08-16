"""
pages/2_login.py - User Login Page for Heal-Together
Demonstrates Python syllabus concepts:
- Day 1: Variables and input/output
- Day 2: Comparison and logical operators
- Day 3: Conditional statements (if, elif, else)
- Day 5: Strings and string methods
- Day 9-10: Dictionaries
- Day 11: Functions and return values
- Day 26: Streamlit session state management
- Day 27: Data validation
- Day 29: Project integration
"""

import streamlit as st
import auth
import database as db

# Configure page
st.set_page_config(
    page_title="Login",
    page_icon="🔑",
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

# Guard against already-authenticated users
if auth.is_logged_in():
    if auth.is_admin():
        st.info("Logged in as Administrator.")
        if st.button("Go to Admin Dashboard", key="admin_dash_btn"):
            st.session_state["redirect_target"] = "pages/6_View_Data.py"
            st.rerun()
    else:
        st.info(f"Already logged in as **{st.session_state.get('full_name')}**.")
        if st.button("Go to My Dashboard", key="user_dash_btn"):
            st.session_state["redirect_target"] = "pages/User_Dashboard.py"
            st.rerun()
    st.stop()


# ============================================================
# LOGIN PAGE HEADER
# ============================================================
st.title("🔑 Login")

st.write("""
### Welcome Back 💚
> *"We're happy you're here. Let's continue your wellness journey together."* ❤️
""")

st.divider()


# ============================================================
# LOGIN FORM (Day 26: Session State & Day 27: Validation)
# ============================================================
col1, col2 = st.columns([2, 1])

with col1:
    username = st.text_input(
        "📧 Email Address / Username",
        placeholder="Enter your registered email address",
        key="login_user_input"
    )

    password = st.text_input(
        "🔒 Password",
        type="password",
        placeholder="Enter your password",
        key="login_pass_input"
    )

    st.write("")

    if st.button("LOGIN", use_container_width=True, key="login_submit_btn"):
        if username.strip() == "" or password == "":
            st.warning("Please enter both email/username and password.")
        else:
            # Authenticate via auth.py (Day 29)
            user = auth.authenticate_user(username.strip(), password)
            if user:
                auth.login_user(user)
                st.success(f"Welcome back, {user['full_name']}! 🎉")

                # Role-based Redirection
                if user.get("role") == "admin":
                    st.session_state["redirect_target"] = "pages/6_View_Data.py"
                else:
                    pinfo = db.get_personal_information(user_id=user["id"])
                    if pinfo:
                        st.session_state["redirect_target"] = "pages/User_Dashboard.py"
                    else:
                        st.session_state["redirect_target"] = "pages/3_form.py"
                st.rerun()
            else:
                st.error("Invalid email/username or password. Please try again.")

    # ============================================================
    # FORGOT PASSWORD & USERNAME RECOVERY (Day 3 & 5)
    # ============================================================
    st.write("")
    with st.expander("❓ Forgot Password?"):
        st.write("#### 🔑 Reset Your Password")
        st.write("Enter your registered email address and create a new password.")

        reset_email = st.text_input("Registered Email Address:", placeholder="name@example.com", key="reset_email_in")
        new_pw = st.text_input("New Password:", type="password", placeholder="Min 6 characters", key="reset_new_pw")
        confirm_new_pw = st.text_input("Confirm New Password:", type="password", placeholder="Re-enter new password", key="reset_confirm_pw")

        if st.button("🔄 Reset My Password", use_container_width=True, key="btn_reset_pw"):
            if not reset_email.strip() or not new_pw:
                st.warning("Please fill in all fields.")
            elif new_pw != confirm_new_pw:
                st.error("New passwords do not match.")
            elif len(new_pw) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                ok, msg = auth.reset_user_password(reset_email.strip(), new_pw)
                if ok:
                    st.success(f"✅ {msg}")
                else:
                    st.error(f"❌ {msg}")

    with st.expander("❓ Forgot Username / Email?"):
        st.write("#### 🔍 Find Your Account")
        st.write("Enter your name and account type to look up your registered email address.")

        rec_name = st.text_input("Full Name (as registered):", placeholder="e.g. Srujana", key="rec_name_in")
        rec_type = st.selectbox(
            "Account Type:",
            ["School Student", "College Student", "Employee", "Senior Citizen"],
            key="rec_type_sel"
        )

        if st.button("🔍 Find My Registered Email", use_container_width=True, key="btn_find_acc"):
            if not rec_name.strip():
                st.warning("Please enter your name.")
            else:
                matches = auth.recover_user_account(rec_name.strip(), rec_type)
                if matches:
                    st.success(f"Found {len(matches)} matching account(s):")
                    for m in matches:
                        st.info(f"👤 **Name:** {m['full_name']} | 📧 **Email:** `{m['email']}`")
                else:
                    st.warning("No account found matching this name and user type. Please check spelling or create a new account.")

st.divider()

st.write("Don't have an account?")

if st.button(
    "CREATE A NEW ACCOUNT",
    use_container_width=False,
    key="login_to_register_btn"
):
    st.switch_page("pages/1_Register.py")