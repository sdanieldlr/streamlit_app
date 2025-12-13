
import streamlit as st
import os

from auth_ui import signup_view, login_view, account_view
from db import (
    init_db,
    create_note,
    get_user_notes,
    get_all_notes,
    delete_note,
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

    tab1, tab2, tab3, tab4 = st.tabs(["My Notes", "All Notes", "Chatbot", "Account"])
    with tab1:
        st.subheader("Create a new note")

        title = st.text_input("Title")
        content = st.text_area("Content")
        uploaded_file = st.file_uploader("Attach PDF (optional)", type=["pdf"])

        if st.button("Save Note"):
            pdf_path = None
            pdf_text = ""
            if uploaded_file is not None:
                try:
                    import os
                    from PyPDF2 import PdfReader
                    
                    # Save PDF file
                    os.makedirs("data/pdfs", exist_ok=True)
                    pdf_filename = f"{user['id']}_{uploaded_file.name}"
                    pdf_path = f"data/pdfs/{pdf_filename}"
                    with open(pdf_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Extract text for chatbot
                    uploaded_file.seek(0)  # Reset file pointer
                    pdf_reader = PdfReader(uploaded_file)
                    pdf_text = "\n\n".join([page.extract_text() for page in pdf_reader.pages])
                except Exception as e:
                    st.warning(f"Could not process PDF: {e}")
            
            # Combine content with PDF text for chatbot access
            final_content = content
            if pdf_text:
                final_content = f"{content}\n\n--- PDF Content ---\n{pdf_text}" if content else pdf_text
            
            if title.strip() and (final_content.strip() or pdf_path):
                if user.get("id") is None:
                    st.error("Could not find your user ID. Try logging out and back in.")
                else:
                    create_note(user["id"], title, final_content, pdf_path)
                    st.success("Note saved!")
                    st.rerun()
            else:
                st.error("Title and content/PDF cannot be empty.")

        st.subheader("Your Notes")

        if user.get("id") is not None:
            notes = get_user_notes(user["id"])
        else:
            notes = []

        if notes:
            for note_id, note_title, note_content, created_at, pdf_path in notes:
                col1, col2 = st.columns([6, 1])
                with col1:
                    st.markdown(f"### {note_title}")
                with col2:
                    if st.button("🗑️", key=f"del_{note_id}"):
                        if delete_note(note_id, user["id"]):
                            st.success("Note deleted!")
                            st.rerun()
                        else:
                            st.error("Failed to delete note.")
                if note_content:
                    st.write(note_content)
                if pdf_path and os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        st.download_button("📄 Download PDF", f.read(), file_name=os.path.basename(pdf_path), mime="application/pdf")
                st.caption(f"Created at: {created_at}")
                st.markdown("---")
        else:
            st.info("You have no notes yet.")
    with tab2:
        st.subheader("All Notes (All Users)")
        all_notes = get_all_notes()

        if all_notes:
            for note_id, email, title, content, created_at, pdf_path in all_notes:
                st.markdown(f"### {title}  \n*by {email}*")
                if content:
                    st.write(content)
                if pdf_path and os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        pdf_bytes = f.read()
                        import base64
                        base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="500" type="application/pdf"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)
                st.caption(f"Created at: {created_at}")
                st.markdown("---")
        else:
            st.info("No notes available.")
    with tab3:
        st.subheader("Chatbot")
        
        st.info("💬 This AI chatbot can help you with questions about your notes. It has access to all notes in the system (yours and others'), so you can ask about any content stored in the app. Try asking to summarize notes, find specific information, or get insights from the stored content.")

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

    with tab4:
        account_view()