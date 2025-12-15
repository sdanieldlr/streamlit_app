# The Notes App (Streamlit App with LLM & Google OAuth)

A full-stack notes application built with Streamlit, featuring user authentication, SQLite database, PDF uploads, and OpenAI-powered chatbot.

## Demo Video
https://drive.google.com/file/d/1evAcAnl-Buz3WALOWUJ7JKvPoE1MFsuh/view?usp=sharing

## Features Implemented

### Core Features:
- User authentication (Sign up / Login with email/password)
- SQLite database with CRUD operations
- Create, view, and delete personal notes
- View all users' notes with author information
- PDF upload and embedded viewer
- Account management page with logout, password change, and account deletion

### Bonus Features:
- **Google Sign-in** - OAuth 2.0 integration
- **Chatbot UI** - GPT-4o-mini powered assistant that can read note content and PDFs
- **Hashed Passwords** - Secure bcrypt password storage
- **Public Link** - Cloudflare tunnel deployment

## Instructions for Peers/Testers

### Setup Overview

**Required:**
1. Install dependencies
2. Configure OpenAI API key
3. Run application

**Optional:**
- Step 3: Google OAuth configuration
- Step 5: Cloudflare tunnel for public access

---

### 1) Install

**Option A: From ZIP file**
1. Extract ZIP file
2. Open folder in VS Code (File → Open Folder → Select `streamlit_app`)
3. Open terminal in VS Code (Terminal → New Terminal)

**Option B: Clone from repository**
1. Clone repository:
   ```bash
   git clone https://github.com/sdanieldlr/streamlit_app
   ```
2. Open folder in VS Code (File → Open Folder → Select `streamlit_app`)
3. Open terminal in VS Code (Terminal → New Terminal)

**Install dependencies:**

Windows:
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
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

### 3) Enable Google Sign-in (Optional)

#### Step 3.1: Create OAuth Project

1. Navigate to [Google Cloud Console](https://console.cloud.google.com/)
2. Authenticate with Google account
3. Select "New Project"
4. Enter project name
5. Create and select project

#### Step 3.2: Configure Consent Screen

1. Navigate to APIs & Services → OAuth consent screen
2. Select External user type
3. Enter required fields: app name, support email, developer contact
4. Save configuration

#### Step 3.3: Create Credentials

1. Navigate to APIs & Services → Credentials
2. Create Credentials → OAuth client ID
3. Application type: Web application
4. Add authorized redirect URI: `http://localhost:8501`
5. Create and save Client ID and Client Secret

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

### 4) Run locally
```bash
streamlit run app.py
```
Open `http://localhost:8501`.

### 5) Cloudflare Tunnel Configuration

#### Step 5.1: Install Cloudflared

**Windows:**
1. Download `cloudflared-windows-amd64.exe` from https://github.com/cloudflare/cloudflared/releases
2. Rename to `cloudflared.exe`
3. Move to `C:\Windows\System32\` or add to PATH

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

#### Step 5.2: Execute Tunnel

Open second terminal:

```bash
cloudflared tunnel --url http://localhost:8501
```

Output:
```
https://abc-xyz-123.trycloudflare.com
```

Copy generated URL.

#### Step 5.3: Update OAuth Configuration

Required if using Google Sign-in:

1. Update `.streamlit/secrets.toml`:
   ```toml
   redirect_uri = "https://abc-xyz-123.trycloudflare.com"
   ```

2. Navigate to Google Cloud Console → APIs & Services → Credentials
3. Select OAuth client
4. Add authorized redirect URI: `https://abc-xyz-123.trycloudflare.com`
5. Save configuration

6. Restart Streamlit application in first terminal:
   ```bash
   Ctrl+C
   streamlit run app.py
   ```
   Maintain Cloudflare tunnel in second terminal.

Application accessible at Cloudflare URL.

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
