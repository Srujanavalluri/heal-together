"""
pages/3_form.py - Personal Information Form for Heal-Together
Demonstrates Python syllabus concepts:
- Day 1: Variables and input
- Day 2: Operators
- Day 3: Conditional statements
- Day 5: Strings and regular expressions
- Day 6: Lists
- Day 7: Tuples
- Day 9-10: Dictionaries
- Day 11: Functions
- Day 26: Streamlit forms and session state
- Day 27: Data validation
- Day 29: Project integration
"""

import re
import streamlit as st
import auth
import database as db

# Configure Page
st.set_page_config(
    page_title="Personal Information",
    page_icon="👤",
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
    height: 50px;
    font-size: 17px;
    font-weight: 600;
    border: none;
}
.stButton > button:hover {
    background-color: #4E9447;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Guard against unauthenticated access (Day 26)
auth.require_login()

user_id = auth.get_current_user_id()
existing_info = db.get_personal_information(user_id=user_id)

# -------------------------------------------------------------
# PAGE HEADER
# -------------------------------------------------------------
st.title("👤 Personal Information")
st.write("🌿 Tell us a little about yourself so we can personalize your experience.")
st.divider()

# Prepopulate existing values if available (Day 9-10: Dictionaries)
default_name = existing_info["full_name"] if existing_info else st.session_state.get("full_name", "")
default_age = existing_info["age"] if existing_info else 20
default_gender = existing_info["gender"] if existing_info else "Select Gender"
default_category = existing_info["category"] if existing_info else st.session_state.get("user_type", "Select Category")

gender_options = ["Select Gender", "Male", "Female", "Other"]
category_options = ["Select Category", "School Student", "College Student", "Employee", "Senior Citizen"]

gender_idx = gender_options.index(default_gender) if default_gender in gender_options else 0
category_idx = category_options.index(default_category) if default_category in category_options else 0

# -------------------------------------------------------------
# FORM INPUTS (Day 26: Streamlit Forms)
# -------------------------------------------------------------
col1, col2 = st.columns([2, 1])

with col1:
    name = st.text_input(
        "👤 Full Name",
        value=default_name,
        placeholder="Enter your full name",
        key="form_name_input"
    )

    age = st.number_input(
        "🎂 Age",
        min_value=1,
        max_value=120,
        value=int(default_age),
        step=1,
        key="form_age_input"
    )

    gender = st.selectbox(
        "👥 Gender",
        gender_options,
        index=gender_idx,
        key="form_gender_select"
    )

    category = st.selectbox(
        "🎓 Category",
        category_options,
        index=category_idx,
        key="form_category_select"
    )

    st.write("")

    # Save & Proceed Button
    if st.button("NEXT", use_container_width=True, key="form_submit_btn"):
        # Day 27: Comprehensive Input Validation
        if name.strip() == "":
            st.error("Please enter your full name.")
        elif len(name.strip()) < 2:
            st.error("Name must contain at least 2 characters.")
        elif not re.fullmatch(r"[A-Za-z ]+", name.strip()):
            st.error("Name should contain only letters and spaces.")
        elif name.lower() in ["qwerty", "asdf", "asdfgh", "zxcvbn", "test", "admin"]:
            st.error("Please enter a valid name.")
        elif age <= 0:
            st.error("Please enter a valid age.")
        elif gender == "Select Gender":
            st.error("Please select your gender.")
        elif category == "Select Category":
            st.error("Please select your category.")
        else:
            # Save into SQLite database (Day 29: Integration)
            db.save_personal_information(
                user_id=user_id,
                full_name=name.strip(),
                age=int(age),
                gender=gender,
                category=category
            )

            # Update session state with the confirmed full name
            st.session_state["full_name"] = name.strip()
            st.session_state["user_type"] = category

            st.success("✅ Information saved successfully!")

            # Go to Assessment Hub
            st.switch_page("pages/4_Assessment.py")