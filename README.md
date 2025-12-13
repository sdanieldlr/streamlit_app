# Streamlit + SQLite + LLM App

## How to Run

1. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows; use `source .venv/bin/activate` on macOS/Linux
   pip install -r requirements.txt
   ```

2. Write down the API key in file `secrets.py`:
   ```
   OPENAI_API_KEY = "PASTE-YOUR-KEY-HERE"
   ```

3. Run:
   ```bash
   streamlit run app.py
   ```
