"""
pages/5.1_MentalHealth.py - Mental Wellness & Interactive Self-Care for Heal-Together
Demonstrates Python syllabus concepts:
- Day 4: Loops
- Day 5: Strings and formatting
- Day 6: Lists
- Day 7: Tuples
- Day 9-10: Dictionaries
- Day 11: Functions
- Day 24: Streamlit project setup
- Day 26: Streamlit session state
- Day 28: Streamlit display features (visual animations, interactive timers)
- Day 29: Project integration
"""

import time
from datetime import datetime
import streamlit as st
import auth
import database as db

# Configure Page
st.set_page_config(
    page_title="Mental Health",
    page_icon="🧠",
    layout="wide"
)

# Custom Styling - Calm, soothing theme with breathing orb animation
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
    color: #CBD5E1;
}
.clean-card {
    background-color: #161B22;
    border: 1px solid #30363D;
    border-radius: 10px;
    padding: 18px;
    margin-bottom: 14px;
}
.notification-banner {
    background-color: #161B22;
    border: 1px solid #66B35A;
    border-left: 5px solid #66B35A;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 16px;
}
.mood-tile-sm {
    background-color: #161B22;
    border: 1px solid #30363D;
    border-left: 4px solid #66B35A;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 8px;
}
.progress-container {
    background-color: #21262D;
    border-radius: 6px;
    padding: 2px;
    margin: 4px 0;
}
.progress-bar-fill {
    background-color: #66B35A;
    height: 8px;
    border-radius: 4px;
}

/* Breathing Orb Animation */
@keyframes breatheAnimation {
    0% { transform: scale(1.0); box-shadow: 0 0 15px rgba(102, 179, 90, 0.4); }
    33% { transform: scale(1.45); box-shadow: 0 0 35px rgba(102, 179, 90, 0.85); }
    66% { transform: scale(1.45); box-shadow: 0 0 30px rgba(102, 179, 90, 0.6); }
    100% { transform: scale(1.0); box-shadow: 0 0 15px rgba(102, 179, 90, 0.4); }
}

.breathing-orb {
    width: 140px;
    height: 140px;
    margin: 25px auto;
    border-radius: 50%;
    background: radial-gradient(circle, #66B35A 0%, #2A4722 80%);
    animation: breatheAnimation 12s infinite ease-in-out;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    font-size: 14px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Guard against unauthenticated access
auth.require_login()

user_id = auth.get_current_user_id()
full_name = auth.get_current_user_name()

# ====================================================================
# TOP ACTIVE NOTIFICATION & MANTRA BANNER
# ====================================================================
active_alarms = db.get_alarm_reminders(user_id=user_id)
random_quote = db.get_random_user_quote(user_id=user_id)

if active_alarms:
    nearest = active_alarms[0]
    st.markdown(f"""
    <div class="notification-banner">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-weight:600; color:#66B35A; font-size:16px;">🔔 Active Mindful Reminder: {nearest['title']}</span>
            <span style="font-size:13px; color:#A0AEC0;">⏰ Scheduled: {nearest['reminder_time']}</span>
        </div>
        <div style="color:#CBD5E1; font-size:13px; margin-top:4px;">
            <em>Status: 🟢 Active in your system. Pause and care for yourself when this notification is reached.</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

if random_quote:
    st.markdown(f"""
    <div style="background-color:#161B22; border:1px solid #30363D; border-radius:8px; padding:10px 16px; margin-bottom:14px;">
        <span style="color:#66B35A; font-size:13px; font-weight:600;">✨ Your Personal Mantra:</span>
        <span style="color:#F5F5F5; font-size:14px; font-style:italic;"> "{random_quote['quote_text']}"</span>
        <span style="color:#8F8F8F; font-size:12px;"> — {random_quote['author_name']} ({random_quote['category']})</span>
    </div>
    """, unsafe_allow_html=True)

# PAGE HEADER
st.title("🧠 Mental Health & Wellness")
st.write(f"Welcome, **{full_name}** 💙")
st.write(
    "> *\"Take care of your mind. Small daily routines make a big difference in how you feel.\"* 🌿"
)
st.divider()

# TABS FOR THE 6 CORE FEATURES
tab_mood, tab_sleep, tab_walk, tab_breathing, tab_alarm, tab_quotes = st.tabs([
    "🌸 1. Mood Check-in",
    "😴 2. Sleep Routine",
    "🚶 3. Outdoor Walk",
    "🌿 4. Calm Breathing",
    "⏰ 5. Gentle Reminders",
    "✨ 6. My Personal Quotes"
])


# ====================================================================
# FEATURE 1: DAILY MOOD CHECK-IN
# ====================================================================
with tab_mood:
    st.subheader("🌸 Daily Mood Check-in")
    st.write("How are you feeling right now? Record your emotional state to track your balance over time.")

    col_m1, col_m2 = st.columns([1, 1])

    with col_m1:
        mood_map = {
            "😄 Very Happy": 5,
            "🙂 Good / Peaceful": 4,
            "😐 Neutral / Okay": 3,
            "😔 Low / Sad": 2,
            "😢 Stressed / Overwhelmed": 1
        }
        selected_mood = st.radio("Select your current mood:", list(mood_map.keys()), index=1, key="mh_simple_mood")
        mood_note = st.text_input("Quick note (optional):", placeholder="e.g. Feeling relaxed after a good conversation", key="mh_simple_note")

        if st.button("💾 Save Mood Check-in", use_container_width=True, key="save_mood_btn"):
            db.save_mood_entry(
                user_id=user_id,
                mood=selected_mood,
                mood_score=mood_map[selected_mood],
                note=mood_note
            )
            st.success("✅ Mood check-in saved successfully!")
            st.rerun()

    with col_m2:
        st.subheader("🌸 Recent Mood Check-ins")
        past_moods = db.get_mood_entries(user_id=user_id, limit=6)
        if past_moods:
            for m in past_moods:
                score_val = m["mood_score"] # 1 to 5
                pct_val = int((score_val / 5.0) * 100)
                n_str = f" — *\"{m['note']}\"*" if m.get("note") else ""
                st.markdown(f"""
                <div class="mood-tile-sm">
                    <div style="display:flex; justify-content:space-between;">
                        <span style="font-weight:600; color:#F5F5F5;">{m['mood']}</span>
                        <span style="font-size:12px; color:#8F8F8F;">{m['logged_date']}</span>
                    </div>
                    <div class="progress-container">
                        <div class="progress-bar-fill" style="width: {pct_val}%;"></div>
                    </div>
                    <div style="font-size:12px; color:#CBD5E1;">
                        Harmony Level: {score_val}/5{n_str}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No mood entries logged yet. Record how you feel on the left!")


# ====================================================================
# FEATURE 2: SLEEP ROUTINE
# ====================================================================
with tab_sleep:
    st.subheader("😴 Sleep Routine")
    st.write("Set a peaceful bedtime schedule for yourself to give your mind restful recovery.")

    col_s1, col_s2 = st.columns([1, 1])

    with col_s1:
        bedtime = st.time_input("🌙 Target Bedtime", value=datetime.strptime("22:30", "%H:%M").time(), key="s_bed")
        wake_time = st.time_input("☀️ Target Wake-up Time", value=datetime.strptime("06:30", "%H:%M").time(), key="s_wake")
        sleep_habit = st.selectbox(
            "Pre-sleep Relaxation Habit:",
            ["Listen to quiet nature sounds", "Read a comforting book", "Drink warm chamomile tea / water", "No screens 30 mins before bed"],
            key="sleep_habit_pick"
        )

        if st.button("💾 Save Sleep Schedule", use_container_width=True, key="save_sleep_s_btn"):
            routine_details = f"Bedtime: {bedtime.strftime('%I:%M %p')} | Wake: {wake_time.strftime('%I:%M %p')} | Habit: {sleep_habit}"
            db.save_wellness_activity(
                user_id=user_id,
                activity_type="Sleep Routine",
                duration_minutes=480,
                details=routine_details
            )
            st.success(f"✅ Sleep schedule saved: {routine_details}")

    with col_s2:
        st.markdown("""
        <div class="clean-card">
            <h4 style="color: #66B35A; margin-top:0;">💡 Peaceful Sleep Guidelines</h4>
            <p style="color: #CBD5E1; font-size: 14px; line-height: 1.7;">
                • Maintain consistent sleep and wake timings, even on weekends.<br>
                • Keep your bedroom quiet, dark, and slightly cool.<br>
                • Take 3 gentle, deep breaths when getting under the blanket.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ====================================================================
# FEATURE 3: INTERACTIVE OUTDOOR WALK (Verified Activity)
# ====================================================================
with tab_walk:
    st.subheader("🚶 Verified Outdoor Walk Tracker")
    st.write("A short walk in fresh air oxygenates the body and helps clear overwhelmed thoughts.")

    col_w1, col_w2 = st.columns([1, 1])

    with col_w1:
        st.markdown("""
        <div class="clean-card">
            <h4 style="color: #66B35A; margin-top:0;">👟 Walk Session Verification</h4>
            <p style="color:#CBD5E1; font-size:14px;">
                Enter your genuine walking details or steps taken so your wellness journey is truly tracked.
            </p>
        </div>
        """, unsafe_allow_html=True)

        walk_steps = st.number_input("🚶 Steps Walked (approximate):", min_value=100, max_value=50000, value=2000, step=500, key="walk_steps_in")
        walk_mins = st.slider("⏱️ Walking Duration (minutes):", min_value=5, max_value=90, value=20, step=5, key="w_slider")
        walk_feeling = st.selectbox(
            "🌟 How did you feel during/after the walk?",
            ["🌿 Refreshed & Calmer", "☀️ More Energetic", "🧠 Mind Feels Lighter", "💪 Accomplished"],
            key="walk_feel_sel"
        )
        walk_loc = st.text_input("📍 Location / Nature notes (optional):", placeholder="e.g. In the park near trees / Evening neighborhood walk", key="walk_loc_in")

        if st.button("✅ Complete & Log My Walk", use_container_width=True, key="save_walk_s_btn"):
            loc_str = f" at {walk_loc.strip()}" if walk_loc.strip() else ""
            details_str = f"Walked {walk_steps:,} steps ({walk_mins} mins){loc_str}. Feeling: {walk_feeling}"
            db.save_wellness_activity(
                user_id=user_id,
                activity_type="Outdoor Walk",
                duration_minutes=walk_mins,
                details=details_str
            )
            st.success(f"🎉 Fantastic! Verified and logged: {details_str}")
            st.rerun()

    with col_w2:
        st.write("#### 📜 Your Completed Walks:")
        all_acts = db.get_wellness_activities(user_id=user_id)
        walk_logs = [a for a in all_acts if a["activity_type"] == "Outdoor Walk"]
        if walk_logs:
            for w in walk_logs[:5]:
                st.markdown(f"""
                <div class="clean-card" style="border-left: 3px solid #66B35A; padding: 12px; margin-bottom: 8px;">
                    <div style="font-size: 13px; color: #8F8F8F;">📅 {w['activity_date']} ({w['activity_time']})</div>
                    <div style="font-size: 14px; color: #F5F5F5; margin-top: 4px;">{w['details']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No walks recorded yet. Take a short walk outside and record your steps!")


# ====================================================================
# FEATURE 4: LIVE INTERACTIVE GUIDED BREATHING (Verified Session)
# ====================================================================
with tab_breathing:
    st.subheader("🌿 Interactive Guided Box Breathing (4-4-4)")
    st.write("Follow the live visual rhythm to synchronize your breath and reset your nervous system.")

    col_b1, col_b2 = st.columns([1, 1])

    with col_b1:
        # Visual Animated Breathing Orb
        st.markdown("""
        <div style="text-align: center; margin: 10px 0;">
            <div class="breathing-orb">
                Breathe<br>Rhythm
            </div>
            <p style="color: #66B35A; font-size: 14px; margin-top: 6px;">
                <strong>4s Breathe In</strong> ➔ <strong>4s Hold</strong> ➔ <strong>4s Breathe Out</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("#### ▶️ Start a Live 1-Minute Breathing Session")
        st.write("Click the button below to follow an interactive 4-cycle guided breathing exercise:")

        if st.button("🌬️ Start Guided 1-Minute Session", use_container_width=True, key="start_live_breath_btn"):
            progress_bar = st.progress(0)
            status_text = st.empty()

            cycles = 3
            for c in range(1, cycles + 1):
                # Breathe in (4s)
                for sec in range(1, 5):
                    status_text.markdown(f"### 🌬️ Cycle {c}/{cycles}: **Breathe in slowly...** ({sec}/4s)")
                    progress_bar.progress(((c - 1) * 12 + sec) / (cycles * 12))
                    time.sleep(1)

                # Hold (4s)
                for sec in range(1, 5):
                    status_text.markdown(f"### ⏸️ Cycle {c}/{cycles}: **Hold gently...** ({sec}/4s)")
                    progress_bar.progress(((c - 1) * 12 + 4 + sec) / (cycles * 12))
                    time.sleep(1)

                # Breathe out (4s)
                for sec in range(1, 5):
                    status_text.markdown(f"### 💨 Cycle {c}/{cycles}: **Breathe out smoothly...** ({sec}/4s)")
                    progress_bar.progress(((c - 1) * 12 + 8 + sec) / (cycles * 12))
                    time.sleep(1)

            progress_bar.progress(1.0)
            status_text.markdown("### ✅ **Well done! Session complete.** 🌿")

            # Save completed verified session
            db.save_wellness_activity(
                user_id=user_id,
                activity_type="Mindful Breathing",
                duration_minutes=1,
                details=f"Completed {cycles}-cycle interactive box breathing session"
            )
            st.success("🎉 Your breathing session has been verified and saved to your wellness record!")

    with col_b2:
        st.markdown("""
        <div class="clean-card">
            <h4 style="color: #66B35A; margin-top:0;">🤍 Why Box Breathing Works</h4>
            <p style="color: #CBD5E1; font-size: 14px; line-height: 1.7;">
                • Directly activates the parasympathetic (calming) nervous system.<br>
                • Lowers elevated heart rate and clears physical tension.<br>
                • Gently grounds your awareness in the present moment.
            </p>
        </div>
        """, unsafe_allow_html=True)

        recent_breath = [a for a in db.get_wellness_activities(user_id=user_id) if a["activity_type"] == "Mindful Breathing"]
        if recent_breath:
            st.write("#### 📜 Recent Breathing Sessions:")
            for b in recent_breath[:4]:
                st.write(f"• **{b['activity_date']} ({b['activity_time']}):** {b['details']}")


# ====================================================================
# FEATURE 5: GENTLE REMINDERS & LIVE NOTIFICATIONS
# ====================================================================
with tab_alarm:
    st.subheader("⏰ Gentle Reminders & Live System Notifications")
    st.write("Set mindful reminders that alert you to pause, drink water, stretch, or prepare for rest.")

    col_a1, col_a2 = st.columns([1, 1])

    with col_a1:
        reminder_types = [
            "💧 Drink a glass of water",
            "🚶 Stand up & stretch your shoulders",
            "🌿 Take 3 deep conscious breaths",
            "🌙 Time to disconnect and sleep",
            "✨ Custom reminder..."
        ]
        chosen_rem = st.selectbox("Choose a reminder type:", reminder_types, key="rem_choice")
        custom_rem_text = ""
        if chosen_rem == "✨ Custom reminder...":
            custom_rem_text = st.text_input("Enter your reminder:", placeholder="e.g. Call my parents / Step outside", key="custom_rem_txt")

        rem_title = custom_rem_text if chosen_rem == "✨ Custom reminder..." else chosen_rem
        rem_time = st.time_input("Reminder Time:", value=datetime.now().time(), key="rem_time_pick")

        if st.button("⏰ Set & Activate Reminder", use_container_width=True, key="save_rem_s_btn"):
            if rem_title.strip():
                db.save_alarm_reminder(
                    user_id=user_id,
                    title=rem_title.strip(),
                    reminder_time=rem_time.strftime("%I:%M %p"),
                    label="Active Reminder"
                )
                st.success(f"⏰ Reminder activated for {rem_time.strftime('%I:%M %p')}: {rem_title}")
                st.rerun()

        st.write("---")
        st.write("#### 🔔 Test Live Notification Banner")
        if st.button("🔊 Trigger Test Notification", use_container_width=True, key="test_notif_btn"):
            st.toast("🔔 Mindful Reminder: Take a gentle pause and drink water! 💧", icon="🌿")
            st.info("🔔 **Live Alert:** *Take a moment to breathe and relax your shoulders.*")

    with col_a2:
        st.write("#### 📋 Your Active System Reminders:")
        alarms = db.get_alarm_reminders(user_id=user_id)
        if alarms:
            for al in alarms:
                col_al_txt, col_al_del = st.columns([3, 1])
                with col_al_txt:
                    st.markdown(f"""
                    <div style="background-color:#161B22; border:1px solid #30363D; border-left:3px solid #66B35A; border-radius:8px; padding:10px 14px; margin-bottom:8px;">
                        <span style="font-weight:600; color:#66B35A;">⏰ {al['reminder_time']}</span>
                        <div style="color:#F5F5F5; font-size:14px; margin-top:2px;">{al['title']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_al_del:
                    if st.button("🗑️ Delete", key=f"del_al_{al['id']}"):
                        db.delete_alarm_reminder(al["id"], user_id)
                        st.success("Deleted.")
                        st.rerun()
        else:
            st.info("No active reminders set. Set one on the left to keep mindful habits!")


# ====================================================================
# FEATURE 6: MY PERSONAL MOTIVATIONAL QUOTES & MANTRAS
# ====================================================================
with tab_quotes:
    st.subheader("✨ My Personal Motivational Quotes & Affirmations")
    st.write("Create and store your own uplifting quotes in your private vault to encourage yourself.")

    col_q1, col_q2 = st.columns([1, 1])

    with col_q1:
        st.write("#### ✍️ Add Your Own Personal Quote:")
        my_quote_text = st.text_area(
            "Your Quote / Affirmation:",
            placeholder="e.g. I am worthy of peace, patience, and inner strength.",
            height=110,
            key="user_quote_in"
        )
        quote_cat = st.selectbox(
            "Category:",
            ["Self-Care 🌸", "Courage & Strength 💪", "Peace of Mind 🌿", "Hope & Healing ☀️", "Positive Growth 🌱"],
            key="user_quote_cat"
        )

        if st.button("💾 Save My Personal Quote", use_container_width=True, key="save_my_quote_btn"):
            if my_quote_text.strip():
                db.save_user_quote(
                    user_id=user_id,
                    author_name=full_name,
                    quote_text=my_quote_text.strip(),
                    category=quote_cat
                )
                st.success("🎉 Your personal quote has been saved securely in your backend vault!")
                st.rerun()
            else:
                st.warning("Please enter a quote before saving.")

    with col_q2:
        st.write("#### 💌 Your Saved Personal Quotes:")
        saved_q = db.get_user_quotes(user_id=user_id)
        if saved_q:
            for q in saved_q:
                with st.expander(f"✨ {q['category']} — {q['created_date']}"):
                    st.markdown(f"<blockquote>\"{q['quote_text']}\"</blockquote>", unsafe_allow_html=True)
                    st.caption(f"Author: {q['author_name']}")
                    if st.button("🗑️ Delete Quote", key=f"del_q_{q['id']}"):
                        db.delete_user_quote(q["id"], user_id)
                        st.success("Quote deleted.")
                        st.rerun()
        else:
            st.info("You haven't added any personal quotes yet. Add one on the left to inspire yourself!")

st.divider()

col_nav1, col_nav2 = st.columns(2)
with col_nav1:
    if st.button("🌿 Back to Support & Reflection", use_container_width=True, key="mh_back_btn"):
        st.switch_page("pages/5_choose.py")
with col_nav2:
    if st.button("📊 Go to My Dashboard", use_container_width=True, key="mh_dash_btn"):
        st.switch_page("pages/User_Dashboard.py")