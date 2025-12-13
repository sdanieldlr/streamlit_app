# The Notes App (Streamlit App with LLM & Google OAuth)

A full-stack notes application built with Streamlit, featuring user authentication, SQLite database, PDF uploads, and OpenAI-powered chatbot.

## Demo Video
[Insert your video link here]

## Features Implemented

### Core Features:
- User authentication (Sign up / Login with email/password)
- SQLite database with CRUD operations
- Create, view, and delete personal notes
- View all users' notes with author information
- PDF upload and embedded viewer
- Account management page with logout, password change, and account deletion

### Bonus Features (+40 Points):
- **Google Sign-in** (+20 points) - OAuth 2.0 integration
- **Chatbot UI** (+10 points) - GPT-4o-mini powered assistant that can read note content and PDFs
- **Hashed Passwords** (+5 points) - Secure bcrypt password storage
- **Public Link** (+5 points) - Cloudflare tunnel deployment

## Instructions for Peers/Testers

### 1) Install

**Option A: From ZIP file (for submission)**
```bash
# Extract the ZIP file, then navigate to the folder
cd streamlit_app
# (Skip the cd command if you're already inside the streamlit_app folder)
```

**Option B: Clone from GitHub (for peers/testers)**
```bash
git clone https://github.com/sdanieldlr/streamlit_app
cd streamlit_app
```

**Then continue with:**
```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# or
source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

### 2) Enable Chatbot (OpenAI)
```bash
copy secrets.py.example secrets.py   # Windows
```
```bash
cp secrets.py.example secrets.py   # macOS/Linux
```
Edit `secrets.py` and set your key:
```python
OPENAI_API_KEY = "sk-your-openai-key"
```

### 3) Enable Google Sign-in
```bash
copy .streamlit\secrets.toml.example .streamlit\secrets.toml   # Windows
```
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # macOS/Linux
```
Edit `.streamlit/secrets.toml`:
```toml
client_id = "your-client-id.apps.googleusercontent.com"
client_secret = "your-client-secret"
redirect_uri = "http://localhost:8501"
```
Create credentials in Google Cloud → OAuth 2.0 Client (Web) and add `http://localhost:8501` as an authorized redirect URI.

### 4) Run locally
```bash
streamlit run app.py
```
Open `http://localhost:8501`.

### 5) Public link via Cloudflare (in another Terminal)
```bash
cloudflared tunnel --url http://localhost:8501
```
Copy the generated `https://<random>.trycloudflare.com` URL.
If using Google sign-in publicly, update:
- `.streamlit/secrets.toml` → `redirect_uri = "https://<random>.trycloudflare.com"`
- Google Cloud Console → add the Cloudflare URL as an authorized redirect URI

## Troubleshooting

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

## Team Members
Sergio de los Reyes, Nadia Gherab, Marcos Morales, Ibtihal Nasri, Clara Nogales, Tomás Povedano, Harutyun Yeranyan
