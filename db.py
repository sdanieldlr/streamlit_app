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
    init_db()
    with _conn() as con:
        con.execute(
            "INSERT INTO users(email, password, method) VALUES (?, ?, 'manual')",
            (email, password)
        )


def create_google_user(email: str, name: str):
    """
    Creates a GOOGLE user (email only, no password).
    If user already exists, does nothing.
    """
    init_db()
    with _conn() as con:
        con.execute("""
            INSERT OR IGNORE INTO users(email, name, method)
            VALUES (?, ?, 'google')
        """, (email, name))


def get_user(email: str):
    """Returns (id, email, password, name, method) or None."""
    init_db()
    with _conn() as con:
        return con.execute(
            "SELECT id, email, password, name, method FROM users WHERE email=?",
            (email,)
        ).fetchone()


def delete_user(email: str):
    init_db()
    with _conn() as con:
        con.execute("DELETE FROM users WHERE email=?", (email,))


def list_users():
    """Optional helper: list all users."""
    init_db()
    with _conn() as con:
        return con.execute(
            "SELECT id, email, name, method, created_at FROM users"
        ).fetchall()


# ---------- NOTE FUNCTIONS ----------

def create_note(user_id: int, title: str, content: str):
    init_db()
    with _conn() as con:
        con.execute(
            "INSERT INTO notes(user_id, title, content) VALUES (?, ?, ?)",
            (user_id, title, content),
        )


def get_user_notes(user_id: int):
    """All notes for a specific user."""
    init_db()
    with _conn() as con:
        return con.execute(
            "SELECT id, title, content, created_at "
            "FROM notes WHERE user_id=? ORDER BY created_at DESC",
            (user_id,)
        ).fetchall()


def get_all_notes():
    """All notes from all users, joined with user emails."""
    init_db()
    with _conn() as con:
        return con.execute(
            "SELECT notes.id, users.email, notes.title, notes.content, notes.created_at "
            "FROM notes JOIN users ON notes.user_id = users.id "
            "ORDER BY notes.created_at DESC"
        ).fetchall()
