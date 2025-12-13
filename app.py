
import streamlit as st

from auth_ui import signup_view, login_view, logout_button
from db import (
    init_db,
    create_note,
    get_user_notes,
    get_all_notes,
)
from llm_utils import chat_reply

if "oauth_cleared" not in st.session_state:
    st.cache_data.clear()
    st.cache_resource.clear()
    st.session_state["oauth_cleared"] = True

st.set_page_config(page_title="Notes App", page_icon="📝")
st.title("Notes App")

init_db()

user = st.session_state.get("user")

if not user:
    tab1, tab2 = st.tabs(["Login", "Sign up"])
    with tab1:
        login_view()
    with tab2:
        signup_view()

else:
    name_display = user.get("name") or user.get("email")
    st.success(f"Welcome, {name_display}")

    tab1, tab2, tab3 = st.tabs(["My Notes", "All Notes", "Chatbot"])
    with tab1:
        st.subheader("Create a new note")

        title = st.text_input("Title")
        content = st.text_area("Content")

        if st.button("Save Note"):
            if title.strip() and content.strip():
                if user.get("id") is None:
                    st.error("Could not find your user ID. Try logging out and back in.")
                else:
                    create_note(user["id"], title, content)
                    st.success("Note saved!")
                    st.rerun()
            else:
                st.error("Title and content cannot be empty.")

        st.subheader("Your Notes")

        if user.get("id") is not None:
            notes = get_user_notes(user["id"])
        else:
            notes = []

        if notes:
            for note_id, note_title, note_content, created_at in notes:
                st.markdown(f"### {note_title}")
                st.write(note_content)
                st.caption(f"Created at: {created_at}")
                st.markdown("---")
        else:
            st.info("You have no notes yet.")
    with tab2:
        st.subheader("All Notes (all users)")
        all_notes = get_all_notes()

        if all_notes:
            for note_id, email, title, content, created_at in all_notes:
                st.markdown(f"### {title}  \n*by {email}*")
                st.write(content)
                st.caption(f"Created at: {created_at}")
                st.markdown("---")
        else:
            st.info("No notes available.")
    with tab3:
        st.subheader("Chatbot")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Display chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # User input
        if prompt := st.chat_input("Ask me anything..."):
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            # Get AI response
            response = chat_reply(prompt, st.session_state.chat_history[:-1])  # Exclude the latest user message from history for reply
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.write(response)

    st.markdown("---")
    logout_button()