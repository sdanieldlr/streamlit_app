# Streamlit Notes App with LLM & Google OAuth

A full-stack notes application built with Streamlit, featuring user authentication, SQLite database, PDF uploads, and OpenAI-powered chatbot.

## 🎥 Demo Video
[Insert your video link here]

## ✨ Features Implemented

### Core Features:
- ✅ User authentication (Sign up / Login with email/password)
- ✅ SQLite database with CRUD operations
- ✅ Create, view, and delete personal notes
- ✅ View all users' notes with author information
- ✅ PDF upload and embedded viewer
- ✅ Account management page with logout, password change, and account deletion

### Bonus Features (+40 Points):
- ✅ **Google Sign-in** (+20 points) - OAuth 2.0 integration
- ✅ **Chatbot UI** (+10 points) - GPT-4o-mini powered assistant that can read note content and PDFs
- ✅ **Hashed Passwords** (+5 points) - Secure bcrypt password storage
- ✅ **Public Link** (+5 points) - Cloudflare tunnel deployment

## 🚀 Quick Start for Peers/Testers

### Prerequisites
- Python 3.8+
- OpenAI API key (for chatbot functionality)
- Google OAuth credentials (optional, for Google sign-in)

### 1. Clone & Install
```bash
# Clone the repository
git clone <repository-url>
cd streamlit_app

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Secrets

#### Required: OpenAI API Key
Copy the example file and add your key:
```bash
# Windows
copy secrets.py.example secrets.py

# macOS/Linux
cp secrets.py.example secrets.py
```

Then edit `secrets.py`:
```python
OPENAI_API_KEY = "sk-your-actual-openai-key"
```

#### Optional: Google OAuth (for +20 bonus points)
Copy the example file and add your credentials:
```bash
# Windows
copy .streamlit\secrets.toml.example .streamlit\secrets.toml

# macOS/Linux
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Then edit `.streamlit/secrets.toml`:
```toml
client_id = "your-client-id.apps.googleusercontent.com"
client_secret = "your-client-secret"
redirect_uri = "http://localhost:8501"
```

**Get Google OAuth credentials:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create OAuth 2.0 Client ID (Web application)
3. Add authorized redirect URI: `http://localhost:8501`

### 3. Run the App
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### 4. Test Features
- **Sign up** with email/password or Google
- **Create notes** with optional PDF attachments
- **Chat** with the AI assistant about your notes
- **Manage account** - change password, logout, delete account
- **View all notes** from all users

## 🌐 Deploy Publicly (Cloudflare Tunnel) - For +5 Bonus

### Option 1: Quick Tunnel (No Account Required)
1. Download Cloudflare tunnel from [here](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/)

2. Run your Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. In another terminal, create tunnel:
   ```bash
   cloudflared tunnel --url http://localhost:8501
   ```

4. Copy the public URL (e.g., `https://xyz.trycloudflare.com`)

5. **Important for Google OAuth:** Update your redirect URI in:
   - `.streamlit/secrets.toml` - Change `redirect_uri` to your Cloudflare URL
   - [Google Cloud Console](https://console.cloud.google.com/apis/credentials) - Add Cloudflare URL to authorized redirect URIs

### Option 2: Streamlit Community Cloud (Free, Persistent)
1. Push your code to GitHub
2. Go to [share.streamli        # Main application with tabs (My Notes, All Notes, Chatbot, Account)
├── auth_ui.py                  # Authentication views (Login, Signup, Account management)
├── db.py                       # Database layer (SQLite operations, user/note CRUD)
├── llm_utils.py                # OpenAI integration (chatbot functionality)
├── secrets.py                  # API keys (NOT in repo - use secrets.py.example)
├── secrets.py.example          # Template for secrets.py
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
├── .streamlit/
│   ├── secrets.toml            # OAuth credentials (NOT in repo - use example)
│   └── secrets.toml.example    # Template for secrets.toml
└── data/
    ├── app.db                  # SQLite database (auto-created)
    └── pdfs/                   # Uploaded PDF storage (auto-created)
```

## 🔒 Security & Git Best Practices

**Files excluded from Git (in `.gitignore`):**
- `secrets.py` - Contains OpenAI API key
- `.streamlit/secrets.toml` - Contains Google OAuth credentials
- `data/app.db` - User database with passwords
- `data/pdfs/` - Uploaded PDFs
- `__pycache__/` - Python cache files
- `.venv/` - Virtual environment

**For submission:**
- The `.example` files show the format needed
- Never share real API keys or credentials
- The professor will use their own keys when testing

## 🐛 Troubleshooting

**"Module not found" errors:**
```bash
pip install -r requirements.txt
```

**Chatbot not working:**
- Check that `secrets.py` exists with valid OpenAI API key
- Verify the key starts with `sk-`

**Google sign-in not working:**
- Ensure `.streamlit/secrets.toml` exists with valid credentials
- Check redirect URI matches in both secrets.toml and Google Console
- For local testing: use `http://localhost:8501`
- For Cloudflare: use your cloudflare URL

**Database errors:**
- Delete `data/app.db` to reset (creates fresh database on next run)

## 👥 Team Members
[Add your team member names here]

## 📝 Assignment Requirements Checklist

- ✅ Email/password authentication
- ✅ SQLite database integration
- ✅ Create and manage notes
- ✅ View all users' notes
- ✅ Google Sign-in (+20 bonus)
- ✅ Chatbot UI (+10 bonus)
- ✅ Hashed passwords with bcrypt (+5 bonus)
- ✅ Public link via Cloudflare (+5 bonus)
- ⏳ Video demonstration
- ⏳ ZIP file submission
## 🔒 Security Notes

- `secrets.py` contains your OpenAI API key - **never commit this file**
- `.streamlit/secrets.toml` contains OAuth credentials - **keep private**
- For submission: Replace real keys with placeholder text

## 👥 Team Members
[Add your team member names here]
