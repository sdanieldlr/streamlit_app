
import sqlite3
import os
import bcrypt

DB_PATH = "data/app.db"
os.makedirs("data", exist_ok=True)


def _conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    with _conn() as con:
        # 1) Ensure basic users table exists (old schema compatible)
        con.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # 2) Check existing columns and add missing ones (name, method)
        cur = con.execute("PRAGMA table_info(users)")
        cols = [row[1] for row in cur.fetchall()]

        if "name" not in cols:
            con.execute("ALTER TABLE users ADD COLUMN name TEXT")

        if "method" not in cols:
            con.execute("ALTER TABLE users ADD COLUMN method TEXT DEFAULT 'manual'")

        # 3) Notes table
        con.execute("""
        CREATE TABLE IF NOT EXISTS notes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)
        
        # Add pdf_path column if it doesn't exist
        cur = con.execute("PRAGMA table_info(notes)")
        cols = [row[1] for row in cur.fetchall()]
        if "pdf_path" not in cols:
            con.execute("ALTER TABLE notes ADD COLUMN pdf_path TEXT")


# ---------- USER FUNCTIONS ----------

def create_user(email: str, password: str):
    """Creates a MANUAL (email/password) user with hashed password."""
    with _conn() as con:
        # Hash the password using bcrypt
        hashed_pwd = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        con.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, hashed_pwd),
        )


def get_user(email: str):
    """Retrieves a user by email."""
    with _conn() as con:
        cur = con.execute("SELECT * FROM users WHERE email = ?", (email,))
        return cur.fetchone()


def create_google_user(email: str, name: str):
    """Creates a GOOGLE user."""
    with _conn() as con:
        con.execute(
            "INSERT INTO users (email, name, method) VALUES (?, ?, ?)",
            (email, name, "google"),
        )


# ---------- NOTE FUNCTIONS ----------

def create_note(user_id: int, title: str, content: str, pdf_path: str = None):
    """Creates a note for a user."""
    with _conn() as con:
        con.execute(
            "INSERT INTO notes (user_id, title, content, pdf_path) VALUES (?, ?, ?, ?)",
            (user_id, title, content, pdf_path),
        )


def get_user_notes(user_id: int):
    """Retrieves all notes for a user."""
    with _conn() as con:
        cur = con.execute(
            "SELECT id, title, content, created_at, pdf_path FROM notes WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        )
        return cur.fetchall()


def get_all_notes():
    """Retrieves all notes from all users."""
    with _conn() as con:
        cur = con.execute(
            "SELECT notes.id, users.email, notes.title, notes.content, notes.created_at, notes.pdf_path FROM notes JOIN users ON notes.user_id = users.id ORDER BY notes.created_at DESC"
        )
        return cur.fetchall()


def delete_note(note_id: int, user_id: int) -> bool:
    """Deletes a note if it belongs to the user. Returns True if successful."""
    try:
        with _conn() as con:
            con.execute(
                "DELETE FROM notes WHERE id = ? AND user_id = ?",
                (note_id, user_id),
            )
        return True
    except Exception:
        return False


# ---------- ADDITIONAL USER FUNCTIONS (for compatibility) ----------

def verify_user(email: str, password: str) -> int | None:
    """Verifies user credentials with bcrypt. Returns user ID if valid, None otherwise."""
    row = get_user(email)
    if row is None:
        return None
    
    user_id, _, stored_hash = row[0], row[1], row[2]
    
    # Handle both old plaintext passwords and new bcrypt hashes
    if isinstance(stored_hash, str):
        # Old plaintext password
        if password == stored_hash:
            return user_id
    else:
        # New bcrypt hash (bytes)
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
            return user_id
    
    return None


def add_user(email: str, password: str) -> bool:
    """Creates a new user. Returns True if successful, False if email already exists."""
    try:
        create_user(email, password)
        return True
    except Exception:
        return False


def update_password(user_id: int, new_password: str) -> bool:
    """
    Updates user password with bcrypt hashing.
    Returns True if successful, False otherwise.
    """
    try:
        with _conn() as con:
            hashed_pwd = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
            con.execute(
                "UPDATE users SET password = ? WHERE id = ?",
                (hashed_pwd, user_id),
            )
            return True
    except Exception:
        return False


def delete_user(user_id: int) -> bool:
    """Deletes a user and all their notes. Returns True if successful."""
    try:
        with _conn() as con:
            # Delete all notes for this user
            con.execute("DELETE FROM notes WHERE user_id = ?", (user_id,))
            # Delete the user
            con.execute("DELETE FROM users WHERE id = ?", (user_id,))
        return True
    except Exception:
        return False