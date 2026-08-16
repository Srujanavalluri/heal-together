"""
auth.py - Authentication and Access Control for Heal-Together
Demonstrates Python syllabus concepts:
- Day 1: Variables and basic data types
- Day 2: Comparison and logical operators
- Day 3: Conditional statements (if, elif, else)
- Day 5: Strings and string methods (.strip(), .lower())
- Day 9-10: Dictionaries and dictionary methods (.get(), keys)
- Day 11: Functions, parameters, and return statements
- Day 12: Default parameters and tuple returns
- Day 26: Streamlit session state management
- Day 27: Data validation
- Day 29: Project integration
"""

import hashlib
import os
import secrets
import sqlite3
import streamlit as st

DB_NAME = "mindbridge.db"


# ====================================================================
# 1. SECURE PASSWORD HASHING (Day 11 & 12: Functions with Tuples)
# ====================================================================
def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """
    Hashes a password using PBKDF2-HMAC-SHA256 with a unique cryptographic salt.
    Returns: (password_hash, salt) tuple.
    """
    if not salt:
        salt = secrets.token_hex(16)
    pw_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return pw_hash, salt


def verify_password(password: str, salt: str, expected_hash: str) -> bool:
    """
    Verifies a plaintext password against the stored salt and hash securely.
    """
    pw_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(pw_hash, expected_hash)


# ====================================================================
# 2. USER REGISTRATION (Day 5, 27: String validation & Error Handling)
# ====================================================================
def register_user(
    full_name: str,
    email: str,
    password: str,
    user_type: str = "General",
    role: str = "user"
) -> tuple[bool, str, int | None]:
    """
    Validates and registers a new user into SQLite database.
    Prevents duplicate accounts and hashes the password before storing.
    """
    from datetime import datetime

    name_clean = full_name.strip()
    email_clean = email.strip().lower()

    # Day 27: Input Validation
    if not name_clean or not email_clean or not password:
        return False, "All fields are required.", None

    if len(name_clean) < 2:
        return False, "Name must be at least 2 characters long.", None

    if "@" not in email_clean or "." not in email_clean:
        return False, "Please enter a valid email address.", None

    if len(password) < 6:
        return False, "Password must be at least 6 characters long.", None

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Prevent duplicate account creation
    cur.execute("SELECT id FROM users WHERE LOWER(email) = ?", (email_clean,))
    if cur.fetchone():
        conn.close()
        return False, "An account with this email address already exists. Please log in.", None

    pw_hash, salt = hash_password(password)
    created_at = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

    try:
        cur.execute("""
            INSERT INTO users (full_name, email, password_hash, salt, user_type, role, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name_clean, email_clean, pw_hash, salt, user_type, role, created_at))
        user_id = cur.lastrowid
        conn.commit()
    except Exception as e:
        conn.close()
        return False, f"Registration failed: {str(e)}", None

    conn.close()
    return True, "Registration successful!", user_id


# ====================================================================
# 3. USER AUTHENTICATION & LOGIN (Day 9-10: Dictionaries, Day 26: Session State)
# ====================================================================
def authenticate_user(email_or_username: str, password: str) -> dict | None:
    """
    Authenticates a user against SQLite users table.
    Returns user record dictionary if valid, else None.
    """
    email_clean = email_or_username.strip().lower()
    if not email_clean or not password:
        return None

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT id, full_name, email, password_hash, salt, user_type, role, created_at
        FROM users
        WHERE LOWER(email) = ? OR LOWER(full_name) = ?
    """, (email_clean, email_clean))

    user_row = cur.fetchone()
    conn.close()

    if not user_row:
        return None

    if verify_password(password, user_row["salt"], user_row["password_hash"]):
        return dict(user_row)

    return None


def login_user(user: dict):
    """
    Populates Streamlit session state with authenticated user details.
    """
    st.session_state["logged_in"] = True
    st.session_state["user_id"] = user["id"]
    st.session_state["username"] = user["email"]
    st.session_state["full_name"] = user["full_name"]
    st.session_state["role"] = user.get("role", "user")
    st.session_state["user_type"] = user.get("user_type", "General")


def logout_user():
    """
    Clears all authentication and user data from session state.
    """
    keys_to_clear = [
        "logged_in", "user_id", "username", "full_name", "role", "user_type",
        "redirect_target", "mh_submitted", "lon_submitted", "both_submitted",
        "ns_submitted", "editing_journal_id", "story_idx"
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state["logged_in"] = False


# ====================================================================
# 4. SESSION HELPERS & ACCESS GUARDS (Day 3 & 11: Boolean Functions)
# ====================================================================
def is_logged_in() -> bool:
    """Checks if a user is currently authenticated."""
    return bool(st.session_state.get("logged_in") and st.session_state.get("user_id"))


def is_admin() -> bool:
    """Checks if the authenticated user has administrator privileges."""
    return is_logged_in() and st.session_state.get("role") == "admin"


def get_current_user() -> dict | None:
    """Returns dictionary of currently logged-in user details."""
    if not is_logged_in():
        return None
    return {
        "id": st.session_state.get("user_id"),
        "full_name": st.session_state.get("full_name"),
        "email": st.session_state.get("username"),
        "role": st.session_state.get("role"),
        "user_type": st.session_state.get("user_type")
    }


def get_current_user_id() -> int | None:
    """Returns the user ID of the current logged-in user."""
    return st.session_state.get("user_id")


def get_current_user_name() -> str:
    """Returns the full name of the current logged-in user."""
    return st.session_state.get("full_name", "Friend")


def require_login():
    """Guard function to protect authenticated user pages."""
    if not is_logged_in():
        st.warning("🔒 Please log in to access this page.")
        if st.button("Go to Login", key="guard_login_btn"):
            st.switch_page("pages/2_login.py")
        st.stop()


def require_admin():
    """Guard function to strictly protect administrator pages."""
    if not is_logged_in():
        st.warning("🔒 Please log in as an administrator to access this page.")
        if st.button("Go to Login", key="guard_admin_login_btn"):
            st.switch_page("pages/2_login.py")
        st.stop()

    if not is_admin():
        st.error("⛔ Access Denied. This section is restricted to administrators only.")
        if st.button("Return to Home", key="guard_admin_home_btn"):
            st.switch_page("pages/Home.py")
        st.stop()


# ====================================================================
# 5. PASSWORD RESET & RECOVERY (Day 5, 11, 27)
# ====================================================================
def reset_user_password(email: str, new_password: str) -> tuple[bool, str]:
    """Resets user password securely in SQLite."""
    email_clean = email.strip().lower()
    if not email_clean:
        return False, "Please enter your registered email address."
    if len(new_password) < 6:
        return False, "New password must be at least 6 characters long."

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE LOWER(email) = ?", (email_clean,))
    user = cur.fetchone()

    if not user:
        conn.close()
        return False, "No account found with this email address."

    pw_hash, salt = hash_password(new_password)
    cur.execute("UPDATE users SET password_hash = ?, salt = ? WHERE id = ?", (pw_hash, salt, user[0]))
    conn.commit()
    conn.close()
    return True, "Password reset successfully! You can now log in with your new password."


def recover_user_account(full_name: str, user_type: str) -> list[dict]:
    """Finds registered user account by full name and user type."""
    name_clean = full_name.strip().lower()
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT full_name, email, user_type, created_at
        FROM users
        WHERE LOWER(full_name) LIKE ? AND user_type = ? AND role != 'admin'
    """, (f"%{name_clean}%", user_type))

    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
