# Streamlit Notes App with LLM & Google OAuth

A full-stack notes application built with Streamlit, featuring user authentication, SQLite database, and OpenAI integration.

## 🎥 Demo Video
[Insert your video link here]

## ✨ Features Implemented

### Core Features:
- ✅ User authentication (Sign up / Login)
- ✅ SQLite database with CRUD operations
- ✅ Personal notes management
- ✅ View all users' notes

### Bonus Features (+40 Points):
- ✅ **Google Sign-in** (+20 points) - OAuth 2.0 integration
- ✅ **Chatbot UI** (+10 points) - GPT-4 powered assistant
- ✅ **Hashed Passwords** (+5 points) - Secure password storage
- ✅ **Public Link** (+5 points) - Cloudflare tunnel deployment

## 🚀 How to Run Locally

### 1. Install Dependencies
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# OR
source .venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
```

### 2. Configure API Keys

**For OpenAI (Required for Chatbot):**

Create `secrets.py` in the root folder:
```python
OPENAI_API_KEY = "sk-your-key-here"
```

**For Google OAuth (Optional):**

Create `.streamlit/secrets.toml`:
```toml
client_id = "your-google-client-id"
client_secret = "your-google-client-secret"
redirect_uri = "http://localhost:8501"
```

### 3. Run the App
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 🌐 Deploy Publicly (Cloudflare Tunnel)

1. Install Cloudflare tunnel:
   ```bash
   # Download from https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
   ```

2. Run your Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. In another terminal, create tunnel:
   ```bash
   cloudflared tunnel --url http://localhost:8501
   ```

4. Copy the public URL provided (e.g., `https://xyz.trycloudflare.com`)

## 📁 Project Structure

```
streamlit_app/
├── app.py              # Main Streamlit application
├── auth_ui.py          # Login/Signup UI and Google OAuth
├── db.py               # SQLite database operations
├── llm_utils.py        # OpenAI integration (summarize, chat)
├── secrets.py          # API keys (DO NOT COMMIT)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## 🔒 Security Notes

- `secrets.py` contains your OpenAI API key - **never commit this file**
- `.streamlit/secrets.toml` contains OAuth credentials - **keep private**
- For submission: Replace real keys with placeholder text

## 👥 Team Members
[Add your team member names here]
