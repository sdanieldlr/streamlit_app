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

### Quick Summary

**Minimum setup** (just to run the app locally):
1. Install Python dependencies
2. Add OpenAI API key
3. Run `streamlit run app.py`

**Optional extras** (for bonus points):
- Step 3: Google Sign-in (+20 points) - requires Google Cloud setup
- Step 5: Public URL (+5 points) - requires Cloudflare installation

---

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

### 3) Enable Google Sign-in (Optional - for +20 bonus points)

**⚠️ Note:** You can skip this step and just use email/password login. Google Sign-in is optional.

#### Step 3.1: Create Google OAuth Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Click "Select a project" at the top → "New Project"
4. Name your project (e.g., "Streamlit Notes App") → Click "Create"
5. Wait for the project to be created, then select it

#### Step 3.2: Configure OAuth Consent Screen

1. In the left menu, go to "APIs & Services" → "OAuth consent screen"
2. Select **External** → Click "Create"
3. Fill in required fields:
   - App name: "Streamlit Notes App"
   - User support email: your email
   - Developer contact: your email
4. Click "Save and Continue" → "Save and Continue" → "Save and Continue"

#### Step 3.3: Create OAuth Credentials

1. In the left menu, go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Application type: **Web application**
4. Name: "Streamlit App"
5. Under "Authorized redirect URIs", click "Add URI"
6. Add: `http://localhost:8501`
7. Click "Create"
8. Copy your **Client ID** and **Client Secret** (save them somewhere safe)

#### Step 3.4: Add Credentials to Your App

```bash
copy .streamlit\secrets.toml.example .streamlit\secrets.toml   # Windows
```
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # macOS/Linux
```

Edit `.streamlit/secrets.toml` and paste your credentials:
```toml
client_id = "YOUR-CLIENT-ID.apps.googleusercontent.com"
client_secret = "YOUR-CLIENT-SECRET"
redirect_uri = "http://localhost:8501"
```

#### Step 3.5: Add Test Users (Important!)

1. Back in Google Cloud Console, go to "OAuth consent screen"
2. Scroll to "Test users" → Click "Add Users"
3. Add your Gmail address (the one you'll use to test login)
4. Click "Save"

**Why?** Your app is in "Testing" mode, so only specific users can log in.

### 4) Run locally
```bash
streamlit run app.py
```
Open `http://localhost:8501`.

### 5) Public link via Cloudflare (Optional - for +5 bonus points)

**⚠️ Note:** This step is optional and only needed if you want a public URL for the bonus points or demo video.

#### Step 5.1: Install Cloudflare Tunnel

**Windows:**
1. Download from: https://github.com/cloudflare/cloudflared/releases
2. Look for `cloudflared-windows-amd64.exe`
3. Download it to your Downloads folder
4. Rename it to `cloudflared.exe`
5. Move it to `C:\Windows\System32\` (or add to PATH)

**macOS:**
```bash
brew install cloudflared
```

**Linux:**
```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
sudo chmod +x /usr/local/bin/cloudflared
```

#### Step 5.2: Run Cloudflare Tunnel

Open a **second terminal** (keep your Streamlit app running in the first one):

```bash
cloudflared tunnel --url http://localhost:8501
```

You'll see output like:
```
Your quick tunnel has been created! Visit it at:
https://abc-xyz-123.trycloudflare.com
```

Copy this URL.

#### Step 5.3: Update Google OAuth (if using Google Sign-in)

If you set up Google OAuth in Step 3:

1. Open `.streamlit/secrets.toml`
2. Change `redirect_uri` to your Cloudflare URL:
   ```toml
   redirect_uri = "https://abc-xyz-123.trycloudflare.com"
   ```

3. Go to [Google Cloud Console](https://console.cloud.google.com/) → APIs & Services → Credentials
4. Click your OAuth client
5. Under "Authorized redirect URIs", click "Add URI"
6. Add: `https://abc-xyz-123.trycloudflare.com`
7. Click "Save"

8. **Restart your Streamlit app** (stop and run `streamlit run app.py` again)

Now your app is publicly accessible at the Cloudflare URL!

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
