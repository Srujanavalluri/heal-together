"""
pages/5.3_Loneliness.py - Connection & Social Support for Heal-Together
Demonstrates Python syllabus concepts:
- Day 4: Loops
- Day 5: Strings and formatting
- Day 6: Lists
- Day 7: Tuples
- Day 9-10: Dictionaries
- Day 11: Functions
- Day 24: Streamlit project setup
- Day 28: Streamlit display features
- Day 29: Project integration
"""

import random
import streamlit as st
import auth
import database as db

# Configure Page
st.set_page_config(
    page_title="Loneliness & Connection",
    page_icon="🤝",
    layout="wide"
)

# Custom Styling - Calm, clean, dark theme with green accents
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
    font-size: 15px;
    margin: 12px 0;
}
.simple-card {
    background-color: #161B22;
    border: 1px solid #30363D;
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# Guard against unauthenticated access
auth.require_login()

user_id = auth.get_current_user_id()
full_name = auth.get_current_user_name()

# PAGE HEADER
st.title("🤝 Loneliness & Connection")
st.write(f"Welcome, **{full_name}** 🤍")
st.write(
    "> *\"If you are feeling left out, lonely, or quiet today, please remember: "
    "your presence matters, and this feeling is temporary. You are never truly alone.\"* ✨"
)
st.divider()

# TABS FOR LONELINESS
tab_journal, tab_quotes, tab_step = st.tabs([
    "📖 1. Private Daily Journal",
    "✨ 2. Comforting Words, Stories & My Quotes",
    "🤝 3. One Small Connection Step"
])


# ====================================================================
# TAB 1: PRIVATE DAILY JOURNAL (SECURE CRUD)
# ====================================================================
with tab_journal:
    st.subheader("📖 Private Daily Journal")
    st.write("Write whatever is in your heart. This is 100% private and visible only to you. 🔒")

    if "edit_j_id" not in st.session_state:
        st.session_state["edit_j_id"] = None

    col_j1, col_j2 = st.columns([1, 1])

    with col_j1:
        if st.session_state["edit_j_id"] is not None:
            # EDIT MODE
            st.write("#### ✏️ Edit Your Note:")
            e_id = st.session_state["edit_j_id"]
            entries = db.get_journal_entries(user_id=user_id)
            current_e = next((e for e in entries if e["id"] == e_id), None)

            if current_e:
                new_t = st.text_input("Title:", value=current_e["title"], key="edit_t_input")
                new_c = st.text_area("Your thoughts:", value=current_e["content"], height=160, key="edit_c_input")

                col_s, col_c = st.columns(2)
                with col_s:
                    if st.button("💾 Save Update", use_container_width=True, key="save_edit_btn"):
                        db.update_journal_entry(e_id, user_id, new_t, new_c)
                        st.session_state["edit_j_id"] = None
                        st.success("Updated successfully!")
                        st.rerun()
                with col_c:
                    if st.button("Cancel", use_container_width=True, key="cancel_edit_btn"):
                        st.session_state["edit_j_id"] = None
                        st.rerun()
            else:
                st.session_state["edit_j_id"] = None
                st.rerun()
        else:
            # NEW ENTRY MODE
            st.write("#### ✍️ Write Today's Thoughts:")
            title_in = st.text_input("Title:", placeholder="e.g. How I felt today", key="j_title_new")
            content_in = st.text_area(
                "Write freely here:",
                placeholder="Write whatever you want... What made you feel alone? What is something small that made you smile today?",
                height=160,
                key="j_content_new"
            )

            if st.button("📝 Save in My Private Journal", use_container_width=True, key="save_new_j"):
                if content_in.strip():
                    db.save_journal_entry(
                        user_id=user_id,
                        title=title_in.strip() if title_in.strip() else "My Daily Reflection",
                        content=content_in.strip()
                    )
                    st.success("✅ Saved privately to your journal!")
                    st.rerun()
                else:
                    st.warning("Please write something before saving.")

    with col_j2:
        st.write("#### 📚 Your Past Reflections:")
        user_entries = db.get_journal_entries(user_id=user_id)
        if user_entries:
            for entry in user_entries:
                with st.expander(f"📅 {entry['entry_date']} — {entry['title']}"):
                    st.write(entry["content"])
                    st.divider()
                    col_btn_e, col_btn_d = st.columns(2)
                    with col_btn_e:
                        if st.button("✏️ Edit", key=f"edit_btn_{entry['id']}", use_container_width=True):
                            st.session_state["edit_j_id"] = entry["id"]
                            st.rerun()
                    with col_btn_d:
                        if st.button("🗑️ Delete", key=f"del_btn_{entry['id']}", use_container_width=True):
                            db.delete_journal_entry(entry["id"], user_id)
                            st.success("Deleted.")
                            st.rerun()
        else:
            st.info("No journal notes yet. Write a few words on the left!")


# ====================================================================
# TAB 2: COMFORTING WORDS, STORIES & MY OWN QUOTES
# ====================================================================
with tab_quotes:
    st.subheader("✨ Comforting Words & Self-Motivation Quotes")
    st.write("Simple, warm thoughts to make you smile and feel lighter.")

    comfort_quotes = [
        "\"If people left you out today, remember: their inability to see your worth does not decrease your value.\" ❤️",
        "\"You don't need a hundred friends. Just one honest, kind heart — starting with being kind to yourself.\" 🌿",
        "\"Some days are quiet, and that's okay. Use this quiet time to care for yourself.\" 🌸",
        "\"You survived all your difficult days so far. You will make it through this one too.\" ✨",
        "\"A flower does not think of competing with the flower next to it. It just blooms.\" 🌼"
    ]

    funny_stories = [
        {
            "title": "🐕 The Dog and the Sneeze",
            "text": "A friendly dog was trying to look very serious and dignified during training. Right as he got his certificate, he sneezed so hard he rolled backward into a pile of leaves and wagged his tail happily with a leaf on his nose! Life doesn't need to be serious all the time. 😂"
        },
        {
            "title": "👓 Looking Everywhere for What You Already Have",
            "text": "Someone searched the entire house for 30 minutes looking for their phone, using their phone's flashlight to search under the bed! Sometimes what we are looking for is already with us. Take a breath and laugh! 📱💡"
        },
        {
            "title": "🐧 The Penguin's Pebble",
            "text": "In Antarctica, penguins search through thousands of stones to find the smoothest pebble and give it to a friend. Even in the freezing snow, kindness is always shared. You deserve good people in your life! 🐧❤️"
        },
        {
            "title": "🐱 The Cat and the Laptop",
            "text": "A cat walked across a laptop keyboard in the middle of a very quiet online class, submitted 'MEOWMEOW123' in the chat, and then took a peaceful nap on the keyboard. Always find time to rest like a cat! 🐾"
        }
    ]

    col_q, col_s = st.columns([1, 1])

    with col_q:
        st.write("#### 💌 Comforting Quotes:")
        for q in comfort_quotes[:3]:
            st.markdown(f"<blockquote>{q}</blockquote>", unsafe_allow_html=True)

        if st.button("🎲 Another Comforting Quote", use_container_width=True, key="rand_q_btn"):
            q_pick = random.choice(comfort_quotes)
            st.info(q_pick)

    with col_s:
        st.write("#### 😂 Short Smile Story:")
        if "story_num" not in st.session_state:
            st.session_state["story_num"] = 0

        st_item = funny_stories[st.session_state["story_num"] % len(funny_stories)]

        st.markdown(f"""
        <div class="simple-card">
            <h4 style="color: #66B35A; margin-top:0;">{st_item['title']}</h4>
            <p style="color: #E2E8F0; font-size: 14px; line-height: 1.7;">
                {st_item['text']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🎲 Another Short Story", use_container_width=True, key="next_st_btn"):
            st.session_state["story_num"] = (st.session_state["story_num"] + 1) % len(funny_stories)
            st.rerun()

    st.write("---")
    st.write("### ✍️ Add Your Own Personal Motivational Quote")
    st.write("Create your own mantra to encourage and uplift yourself whenever you need it.")

    col_add_q1, col_add_q2 = st.columns([1, 1])

    with col_add_q1:
        my_lon_quote = st.text_area(
            "Your Personal Quote / Encouraging Words:",
            placeholder="e.g. Even in solitude, I am growing stronger and kinder every day.",
            height=100,
            key="lon_quote_input"
        )
        quote_tag = st.selectbox("Topic:", ["Belonging & Connection 🤝", "Self-Love ❤️", "Patience & Hope 🌿", "Inner Strength ✨"], key="lon_quote_tag")

        if st.button("💾 Save My Quote into Backend", use_container_width=True, key="save_lon_quote_btn"):
            if my_lon_quote.strip():
                db.save_user_quote(
                    user_id=user_id,
                    author_name=full_name,
                    quote_text=my_lon_quote.strip(),
                    category=quote_tag
                )
                st.success(f"✅ Saved quote by {full_name} into your backend database!")
                st.rerun()
            else:
                st.warning("Please enter a quote before saving.")

    with col_add_q2:
        st.write("#### 💌 My Saved Affirmations:")
        user_quotes_list = db.get_user_quotes(user_id=user_id)
        if user_quotes_list:
            for q in user_quotes_list:
                with st.expander(f"✨ {q['category']} — {q['created_date']}"):
                    st.write(f"\"{q['quote_text']}\"")
                    st.caption(f"Author: {q['author_name']}")
                    if st.button("Delete", key=f"del_lq_{q['id']}"):
                        db.delete_user_quote(q["id"], user_id)
                        st.success("Deleted.")
                        st.rerun()
        else:
            st.info("You have not added any personal quotes yet.")


# ====================================================================
# TAB 3: ONE SMALL CONNECTION STEP
# ====================================================================
with tab_step:
    st.subheader("🤝 One Small Connection Step")
    st.write("Connection doesn't need to be big. Taking one tiny step helps you feel connected.")

    col_c1, col_c2 = st.columns([1, 1])

    with col_c1:
        st.write("#### 💬 How connected do you feel today?")
        conn_options = [
            "💚 Feeling Connected",
            "🌱 A bit quiet / Disconnected",
            "🌿 Feeling Lonely",
            "🫂 Feeling Left Out / Heavy"
        ]
        selected_conn = st.radio("Choose:", conn_options, index=1, key="simple_conn_rad")
        conn_note = st.text_input("One-line thought (optional):", placeholder="e.g. Spent a lot of time alone today", key="simple_conn_txt")

        if st.button("💾 Record Feeling", use_container_width=True, key="save_conn_feeling_btn"):
            db.save_connection_checkin(
                user_id=user_id,
                feeling=selected_conn,
                goals=conn_note.strip()
            )
            st.success("✅ Feeling recorded.")
            st.rerun()

    with col_c2:
        st.write("#### 🎯 Pick One Simple Step for Today:")
        micro_goals = [
            "Send a simple 'Hi' to a friend or family member",
            "Step outside and smile at one person",
            "Drink tea while watching the birds outside",
            "Talk to a coworker or neighbour for 2 minutes",
            "Spend 10 minutes on a favorite hobby"
        ]
        chosen_micro = st.selectbox("Choose a micro-step:", micro_goals, key="micro_goal_pick")

        if st.button("📌 Complete This Small Step", use_container_width=True, key="save_micro_btn"):
            db.save_wellness_activity(
                user_id=user_id,
                activity_type="Connection Goal",
                duration_minutes=10,
                details=chosen_micro
            )
            st.success(f"🎉 Great job! You chose to: '{chosen_micro}'")

st.divider()

col_nav1, col_nav2 = st.columns(2)
with col_nav1:
    if st.button("🌿 Back to Support & Reflection", use_container_width=True, key="lon_back_btn"):
        st.switch_page("pages/5_choose.py")
with col_nav2:
    if st.button("📊 Go to My Dashboard", use_container_width=True, key="lon_dash_btn"):
        st.switch_page("pages/User_Dashboard.py")
