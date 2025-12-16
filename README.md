# The Notes App (Streamlit App with LLM & Google OAuth)

A full-stack notes application built with Streamlit, featuring user authentication, SQLite database, PDF uploads, and OpenAI-powered chatbot.

## Demo
Video
https://youtu.be/5EpzRjfQI-M

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

### 1) Setup Project Files

**Option A: From ZIP file**
1. Extract ZIP file to a location you can remember (e.g., Desktop or Documents)
2. Open VS Code
3. Click "File" in top menu → "Open Folder" → Navigate and select the `streamlit_app` folder
4. Open integrated terminal: Click "Terminal" in top menu → "New Terminal" (this opens a terminal at the bottom of VS Code)

**Option B: Clone from GitHub**
1. Open terminal/command prompt on your computer
2. Navigate to where you want the project (e.g., `cd Desktop`)
3. Run:
   ```bash
   git clone https://github.com/sdanieldlr/streamlit_app
   ```
4. Open VS Code
5. Click "File" → "Open Folder" → Select the `streamlit_app` folder
6. Open integrated terminal: "Terminal" → "New Terminal"

**Install Python Dependencies:**

These commands create an isolated environment and install required packages.

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

You should see `(.venv)` appear at the start of your terminal line when activated.

Note: If activation fails on Windows, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` then try again.

### 2) Configure OpenAI API Key (Required for Chatbot)

**Step 1:** Create your secrets file by copying the example:

**Windows:**
```bash
copy secrets.py.example secrets.py
```

**macOS/Linux:**
```bash
cp secrets.py.example secrets.py
```

**Step 2:** Get your OpenAI API key:
- Go to https://platform.openai.com/api-keys
- Sign in or create account
- Click "Create new secret key"
- Copy the key (starts with `sk-`)

**Step 3:** Open `secrets.py` in VS Code and replace the placeholder:
```python
OPENAI_API_KEY = "sk-your-actual-key-here"
```
Save the file (Ctrl+S or Cmd+S).

### 3) Enable Google Sign-in (Optional)

#### Step 3.1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Click the project dropdown at the top (says "Select a project")
4. Click "New Project" button in popup
5. Enter a project name (e.g., "Notes App" or "Streamlit Project")
6. Click "Create" button
7. Wait for notification, then click "Select Project" to switch to your new project

#### Step 3.2: Configure OAuth Consent Screen

1. In left sidebar, click "APIs & Services" → "OAuth consent screen"
2. Select "External" as user type → Click "Create"
3. Fill in required fields:
   - App name: Enter "Notes App" or any name
   - User support email: Select your email from dropdown
   - Developer contact: Enter your email
4. Click "Save and Continue" three times (skip optional sections)
5. On summary page, scroll down and click "Back to Dashboard"

#### Step 3.3: Create OAuth Credentials

1. In left sidebar, click "APIs & Services" → "Credentials"
2. Click "+ Create Credentials" at top → Select "OAuth client ID"
3. Application type: Select "Web application" from dropdown
4. Name: Enter "Streamlit App" (or any name)
5. Under "Authorized redirect URIs":
   - Click "+ Add URI"
   - Enter: `http://localhost:8501`
   - Click "Create" button
6. A popup appears with your credentials:
   - Copy the "Client ID" (long string ending in `.apps.googleusercontent.com`)
   - Copy the "Client Secret" (shorter string starting with `GOCSPX-`)
   - Save both somewhere safe (notepad/notes app)

#### Step 3.4: Add Credentials to Application

**Step 1:** Create secrets file in VS Code terminal:

**Windows:**
```bash
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
```

**macOS/Linux:**
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

**Step 2:** Open `.streamlit/secrets.toml` in VS Code (look in `.streamlit` folder in sidebar)

**Step 3:** Replace the placeholders with your actual credentials from Step 3.3:
```toml
client_id = "paste-your-client-id-here.apps.googleusercontent.com"
client_secret = "paste-your-client-secret-here"
redirect_uri = "http://localhost:8501"
```

**Step 4:** Save file (Ctrl+S or Cmd+S)

### 4) Run the Application

**Step 1:** In VS Code terminal (make sure you see `(.venv)` at start of line), run:
```bash
streamlit run app.py
```

**Step 2:** Wait for the output to show:
```
Local URL: http://localhost:8501
```

**Step 3:** Open your web browser and go to `http://localhost:8501`

The app should now be running. You can sign up, create notes, and use the chatbot.

### 5) Create Public URL with Cloudflare (Optional)

This allows anyone on the internet to access your app.

#### Step 5.1: Install Cloudflare Tunnel

**Windows:**
1. Go to https://github.com/cloudflare/cloudflared/releases
2. Scroll to "Assets" section
3. Download `cloudflared-windows-amd64.exe`
4. Once downloaded, rename file to `cloudflared.exe`
5. Move it to `C:\Windows\System32\` (requires admin permission)

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

#### Step 5.2: Start Cloudflare Tunnel

**Important:** Keep your Streamlit app running from Step 4.

**Step 1:** Open a NEW terminal in VS Code:
- Click "Terminal" → "New Terminal" (or click the + icon in terminal panel)
- This creates a second terminal while keeping Streamlit running

**Step 2:** In this NEW terminal, run:
```bash
cloudflared tunnel --url http://localhost:8501
```

**Step 3:** Wait for output showing:
```
Your quick tunnel has been created! Visit it at:
https://random-words-here.trycloudflare.com
```

**Step 4:** Copy your public URL (the `https://` link). It will be different each time.

#### Step 5.3: Update Google OAuth for Public URL

**Only needed if you set up Google Sign-in in Step 3.**

**Step 1:** Open `.streamlit/secrets.toml` in VS Code

**Step 2:** Change the `redirect_uri` to your Cloudflare URL:
```toml
redirect_uri = "https://your-cloudflare-url.trycloudflare.com"
```
Replace with YOUR actual URL from Step 5.2. Save file.

**Step 3:** Update Google Cloud Console:
1. Go to [Google Cloud Console Credentials](https://console.cloud.google.com/apis/credentials)
2. Click on your OAuth client name
3. Under "Authorized redirect URIs", click "+ ADD URI"
4. Paste your Cloudflare URL: `https://your-cloudflare-url.trycloudflare.com`
5. Click "Save" at bottom

**Step 4:** Restart Streamlit:
1. Go to first terminal (where Streamlit is running)
2. Press `Ctrl+C` to stop
3. Run `streamlit run app.py` again
4. Keep second terminal with Cloudflare running (don't close it)

**Done!** Access your app at the Cloudflare URL from any device.

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
