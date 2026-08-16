"""
database.py - SQLite Database Operations for Heal-Together
Demonstrates Python syllabus concepts:
- Day 1: Variables and basic data types
- Day 2: Operators
- Day 3: Conditional statements
- Day 4: Loops (for, while)
- Day 5: Strings and formatting
- Day 6: Lists
- Day 7: Tuples
- Day 9-10: Dictionaries (dict(sqlite3.Row), dictionary comprehensions)
- Day 11: Functions, arguments, and return statements
- Day 12: Default parameters and multiple return values
- Day 23: File handling & SQLite database management
- Day 29: Project integration
"""

import os
import sqlite3
from datetime import datetime

DB_NAME = "mindbridge.db"


# ====================================================================
# 1. DATABASE CONNECTION HELPER (Day 11: Functions & Day 23: DB Connection)
# ====================================================================
def get_connection():
    """
    Establishes and returns a connection to the SQLite database
    configured with sqlite3.Row for dictionary-like column access.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ====================================================================
# 2. DATABASE INITIALIZATION & SCHEMA CREATION (Day 29: Project Integration)
# ====================================================================
def create_database():
    """
    Initializes all SQLite database tables with normalized schemas,
    foreign key constraints, and seeds the default administrator.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. USERS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            user_type TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TEXT NOT NULL
        )
    """)

    # 2. PERSONAL INFORMATION TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personal_information (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            full_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            category TEXT NOT NULL,
            saved_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # 3. ASSESSMENT RESULTS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessment_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT NOT NULL,
            assessment_type TEXT NOT NULL,
            mental_health_score INTEGER,
            loneliness_score INTEGER,
            wellbeing_score INTEGER,
            total_score INTEGER,
            interpretation TEXT,
            assessment_date TEXT NOT NULL,
            assessment_time TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # 4. MOOD ENTRIES TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mood_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            mood TEXT NOT NULL,
            mood_score INTEGER NOT NULL,
            note TEXT,
            logged_date TEXT NOT NULL,
            logged_time TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # 5. JOURNAL ENTRIES TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT,
            content TEXT NOT NULL,
            entry_date TEXT NOT NULL,
            entry_time TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # 6. CONNECTION CHECK-INS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS connection_checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            feeling TEXT NOT NULL,
            goals TEXT,
            logged_date TEXT NOT NULL,
            logged_time TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # 7. WELLNESS ACTIVITIES TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wellness_activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            activity_type TEXT NOT NULL,
            duration_minutes INTEGER,
            details TEXT,
            activity_date TEXT NOT NULL,
            activity_time TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # 8. ALARMS & REMINDERS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alarm_reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            reminder_time TEXT NOT NULL,
            label TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # 9. USER MOTIVATIONAL QUOTES TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            author_name TEXT NOT NULL,
            quote_text TEXT NOT NULL,
            category TEXT DEFAULT 'Self-Motivation',
            created_date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # --- AUTO-MIGRATIONS FOR BACKWARD COMPATIBILITY ---
    cursor.execute("PRAGMA table_info(personal_information)")
    pi_cols = [row[1] for row in cursor.fetchall()]
    if "user_id" not in pi_cols:
        cursor.execute("ALTER TABLE personal_information ADD COLUMN user_id INTEGER")

    cursor.execute("PRAGMA table_info(assessment_results)")
    ar_cols = [row[1] for row in cursor.fetchall()]
    if "user_id" not in ar_cols:
        cursor.execute("ALTER TABLE assessment_results ADD COLUMN user_id INTEGER")
    if "interpretation" not in ar_cols:
        cursor.execute("ALTER TABLE assessment_results ADD COLUMN interpretation TEXT")

    # --- SEED DEFAULT SYSTEM ADMINISTRATOR ---
    cursor.execute("SELECT id FROM users WHERE role = 'admin'")
    if not cursor.fetchone():
        from auth import hash_password
        admin_email = os.environ.get("ADMIN_EMAIL", "admin@mindbridge.com")
        admin_pw = os.environ.get("ADMIN_PASSWORD", "Admin@123")
        pw_hash, salt = hash_password(admin_pw)
        now_str = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        cursor.execute("""
            INSERT INTO users (full_name, email, password_hash, salt, user_type, role, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("System Administrator", admin_email, pw_hash, salt, "Administrator", "admin", now_str))

    conn.commit()
    conn.close()


# ====================================================================
# 3. PERSONAL INFORMATION OPERATIONS (Day 9-10: Dictionaries & Day 11)
# ====================================================================
def save_personal_information(
    full_name: str,
    age: int,
    gender: str,
    category: str,
    user_id: int | None = None
):
    """
    Saves or updates personal information for a user.
    """
    saved_at = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if user_id:
        cursor.execute("SELECT id FROM personal_information WHERE user_id = ?", (user_id,))
        existing = cursor.fetchone()
        if existing:
            cursor.execute("""
                UPDATE personal_information
                SET full_name = ?, age = ?, gender = ?, category = ?, saved_at = ?
                WHERE user_id = ?
            """, (full_name, age, gender, category, saved_at, user_id))
            conn.commit()
            conn.close()
            return

    cursor.execute("""
        INSERT INTO personal_information (user_id, full_name, age, gender, category, saved_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, full_name, age, gender, category, saved_at))

    conn.commit()
    conn.close()


def get_personal_information(user_id: int | None = None):
    """
    Retrieves personal information record for a user (or all users if user_id is None).
    """
    conn = get_connection()
    cursor = conn.cursor()

    if user_id is not None:
        cursor.execute("""
            SELECT id, user_id, full_name, age, gender, category, saved_at
            FROM personal_information
            WHERE user_id = ?
            ORDER BY id DESC LIMIT 1
        """, (user_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    else:
        cursor.execute("""
            SELECT 
                p.id,
                p.user_id,
                COALESCE(u.full_name, p.full_name) AS full_name,
                COALESCE(u.email, 'N/A') AS email,
                p.age,
                p.gender,
                p.category,
                p.saved_at
            FROM personal_information p
            LEFT JOIN users u ON p.user_id = u.id
            ORDER BY p.id DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]


# ====================================================================
# 4. ASSESSMENT RESULTS OPERATIONS (Day 6: Lists, Day 12: Default Parameters)
# ====================================================================
def save_assessment_result(
    username: str,
    assessment_type: str,
    mental_health_score: int | None = None,
    loneliness_score: int | None = None,
    wellbeing_score: int | None = None,
    total_score: int | None = None,
    interpretation: str | None = None,
    user_id: int | None = None
):
    """
    Saves an assessment result linked to the user's account.
    """
    now = datetime.now()
    assessment_date = now.strftime("%d-%m-%Y")
    assessment_time = now.strftime("%I:%M:%S %p")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO assessment_results (
            user_id,
            username,
            assessment_type,
            mental_health_score,
            loneliness_score,
            wellbeing_score,
            total_score,
            interpretation,
            assessment_date,
            assessment_time
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        username,
        assessment_type,
        mental_health_score,
        loneliness_score,
        wellbeing_score,
        total_score,
        interpretation,
        assessment_date,
        assessment_time
    ))

    conn.commit()
    conn.close()


def get_assessment_results(user_id: int | None = None, assessment_type: str | None = None) -> list[dict]:
    """
    Retrieves assessment results filtered by user_id and optional assessment_type.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            a.id,
            a.user_id,
            COALESCE(u.full_name, a.username) AS username,
            COALESCE(u.email, 'N/A') AS email,
            a.assessment_type,
            a.mental_health_score,
            a.loneliness_score,
            a.wellbeing_score,
            a.total_score,
            a.interpretation,
            a.assessment_date,
            a.assessment_time
        FROM assessment_results a
        LEFT JOIN users u ON a.user_id = u.id
        WHERE 1=1
    """
    params = []

    if user_id is not None:
        query += " AND a.user_id = ?"
        params.append(user_id)

    if assessment_type and assessment_type != "All":
        query += " AND a.assessment_type = ?"
        params.append(assessment_type)

    query += " ORDER BY a.id DESC"

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_latest_assessment(user_id: int) -> dict | None:
    """
    Gets the most recent assessment for a specific user.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM assessment_results
        WHERE user_id = ?
        ORDER BY id DESC LIMIT 1
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


# ====================================================================
# 5. MOOD TRACKING OPERATIONS
# ====================================================================
def save_mood_entry(user_id: int, mood: str, mood_score: int, note: str = ""):
    now = datetime.now()
    logged_date = now.strftime("%d-%m-%Y")
    logged_time = now.strftime("%I:%M %p")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO mood_entries (user_id, mood, mood_score, note, logged_date, logged_time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, mood, mood_score, note.strip(), logged_date, logged_time))
    conn.commit()
    conn.close()


def get_mood_entries(user_id: int, limit: int = 30) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, mood, mood_score, note, logged_date, logged_time
        FROM mood_entries
        WHERE user_id = ?
        ORDER BY id DESC LIMIT ?
    """, (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ====================================================================
# 6. DAILY JOURNAL OPERATIONS (SECURE CRUD)
# ====================================================================
def save_journal_entry(user_id: int, title: str, content: str):
    now = datetime.now()
    entry_date = now.strftime("%d-%m-%Y")
    entry_time = now.strftime("%I:%M %p")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO journal_entries (user_id, title, content, entry_date, entry_time)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, title.strip() if title else "My Reflection", content.strip(), entry_date, entry_time))
    conn.commit()
    conn.close()


def update_journal_entry(entry_id: int, user_id: int, title: str, content: str) -> bool:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE journal_entries
        SET title = ?, content = ?
        WHERE id = ? AND user_id = ?
    """, (title.strip(), content.strip(), entry_id, user_id))
    affected = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return affected


def get_journal_entries(user_id: int) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, content, entry_date, entry_time
        FROM journal_entries
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_journal_entry(entry_id: int, user_id: int) -> bool:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM journal_entries WHERE id = ? AND user_id = ?", (entry_id, user_id))
    affected = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return affected


# ====================================================================
# 7. USER MOTIVATIONAL QUOTES & MANTRAS
# ====================================================================
def save_user_quote(user_id: int, author_name: str, quote_text: str, category: str = "Self-Motivation") -> int:
    now_str = datetime.now().strftime("%d-%m-%Y")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_quotes (user_id, author_name, quote_text, category, created_date)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, author_name.strip(), quote_text.strip(), category.strip(), now_str))
    quote_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return quote_id


def get_user_quotes(user_id: int) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, user_id, author_name, quote_text, category, created_date
        FROM user_quotes
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_user_quote(quote_id: int, user_id: int) -> bool:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_quotes WHERE id = ? AND user_id = ?", (quote_id, user_id))
    affected = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return affected


def get_random_user_quote(user_id: int) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, user_id, author_name, quote_text, category, created_date
        FROM user_quotes
        WHERE user_id = ?
        ORDER BY RANDOM() LIMIT 1
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


# ====================================================================
# 8. CONNECTION & WELLNESS ACTIVITIES
# ====================================================================
def save_connection_checkin(user_id: int, feeling: str, goals: str = ""):
    now = datetime.now()
    logged_date = now.strftime("%d-%m-%Y")
    logged_time = now.strftime("%I:%M %p")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO connection_checkins (user_id, feeling, goals, logged_date, logged_time)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, feeling, goals.strip(), logged_date, logged_time))
    conn.commit()
    conn.close()


def get_connection_checkins(user_id: int) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, feeling, goals, logged_date, logged_time
        FROM connection_checkins
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def save_wellness_activity(user_id: int, activity_type: str, duration_minutes: int = 0, details: str = ""):
    now = datetime.now()
    activity_date = now.strftime("%d-%m-%Y")
    activity_time = now.strftime("%I:%M %p")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO wellness_activities (user_id, activity_type, duration_minutes, details, activity_date, activity_time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, activity_type, duration_minutes, details.strip(), activity_date, activity_time))
    conn.commit()
    conn.close()


def get_wellness_activities(user_id: int) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, activity_type, duration_minutes, details, activity_date, activity_time
        FROM wellness_activities
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ====================================================================
# 9. ALARMS & REMINDERS OPERATIONS
# ====================================================================
def save_alarm_reminder(user_id: int, title: str, reminder_time: str, label: str = ""):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO alarm_reminders (user_id, title, reminder_time, label)
        VALUES (?, ?, ?, ?)
    """, (user_id, title.strip(), reminder_time.strip(), label.strip()))
    conn.commit()
    conn.close()


def get_alarm_reminders(user_id: int) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, reminder_time, label
        FROM alarm_reminders
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_alarm_reminder(reminder_id: int, user_id: int) -> bool:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alarm_reminders WHERE id = ? AND user_id = ?", (reminder_id, user_id))
    affected = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return affected


# ====================================================================
# 10. ADMIN ANALYTICS & DIRECTORY OPERATIONS (Day 9, 10, 11)
# ====================================================================
def get_admin_analytics() -> dict:
    """
    Aggregates metrics for the Admin Dashboard.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) AS total FROM users WHERE role != 'admin'")
    total_users = cur.fetchone()["total"]

    cur.execute("SELECT COUNT(*) AS total FROM assessment_results")
    total_assessments = cur.fetchone()["total"]

    cur.execute("SELECT COUNT(*) AS total FROM assessment_results WHERE assessment_type = 'Mental Health'")
    mh_count = cur.fetchone()["total"]

    cur.execute("SELECT COUNT(*) AS total FROM assessment_results WHERE assessment_type = 'Loneliness'")
    lon_count = cur.fetchone()["total"]

    cur.execute("SELECT COUNT(*) AS total FROM assessment_results WHERE assessment_type = 'Both'")
    both_count = cur.fetchone()["total"]

    cur.execute("SELECT COUNT(*) AS total FROM assessment_results WHERE assessment_type = 'Not Sure'")
    not_sure_count = cur.fetchone()["total"]

    cur.execute("SELECT COUNT(*) AS total FROM mood_entries")
    total_moods = cur.fetchone()["total"]

    cur.execute("SELECT COUNT(*) AS total FROM journal_entries")
    total_journals = cur.fetchone()["total"]

    conn.close()
    return {
        "total_users": total_users,
        "total_assessments": total_assessments,
        "mental_health_count": mh_count,
        "loneliness_count": lon_count,
        "both_count": both_count,
        "not_sure_count": not_sure_count,
        "total_moods": total_moods,
        "total_journals": total_journals
    }


def get_all_users(search_query: str | None = None, user_type_filter: str | None = None) -> list[dict]:
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT 
            u.id,
            u.full_name,
            u.email,
            u.user_type,
            u.role,
            u.created_at,
            p.age,
            p.gender,
            p.category
        FROM users u
        LEFT JOIN personal_information p ON u.id = p.user_id
        WHERE u.role != 'admin'
    """
    params = []

    if search_query:
        query += " AND (LOWER(u.full_name) LIKE ? OR LOWER(u.email) LIKE ?)"
        q = f"%{search_query.strip().lower()}%"
        params.extend([q, q])

    if user_type_filter and user_type_filter != "All":
        query += " AND u.user_type = ?"
        params.append(user_type_filter)

    query += " ORDER BY u.id DESC"

    cur.execute(query, tuple(params))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_user_drilldown_data(user_id: int) -> dict | None:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, full_name, email, user_type, role, created_at FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    if not user:
        conn.close()
        return None

    cur.execute("SELECT * FROM personal_information WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,))
    personal_info = cur.fetchone()

    cur.execute("SELECT * FROM assessment_results WHERE user_id = ? ORDER BY id DESC", (user_id,))
    assessments = cur.fetchall()

    cur.execute("SELECT * FROM mood_entries WHERE user_id = ? ORDER BY id DESC LIMIT 10", (user_id,))
    moods = cur.fetchall()

    conn.close()
    return {
        "user": dict(user),
        "personal_info": dict(personal_info) if personal_info else None,
        "assessments": [dict(a) for a in assessments],
        "moods": [dict(m) for m in moods]
    }