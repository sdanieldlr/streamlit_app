
import sqlite3
import os

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


# ---------- USER FUNCTIONS ----------

def create_user(email: str, password: str):
    """Creates a MANUAL (email/password) user."""
    with _conn() as con:
        con.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, password),
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

def create_note(user_id: int, title: str, content: str):
    """Creates a note for a user."""
    with _conn() as con:
        con.execute(
            "INSERT INTO notes (user_id, title, content) VALUES (?, ?, ?)",
            (user_id, title, content),
        )


def get_user_notes(user_id: int):
    """Retrieves all notes for a user."""
    with _conn() as con:
        cur = con.execute(
            "SELECT id, title, content, created_at FROM notes WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        )
        return cur.fetchall()


def get_all_notes():
    """Retrieves all notes from all users."""
    with _conn() as con:
        cur = con.execute(
            "SELECT notes.id, users.email, notes.title, notes.content, notes.created_at FROM notes JOIN users ON notes.user_id = users.id ORDER BY notes.created_at DESC"
        )
        return cur.fetchall()