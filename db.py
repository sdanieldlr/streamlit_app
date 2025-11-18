
# Stores and retrieves user data (email + password).
# It uses SQLite, which creates a small .db file locally.

import sqlite3 # Used to connect to a local SQLite database file
import os      # Lets you interact with files, folders, and environment variables
# sqlite3 connects to the database; os makes sure the data/ folder exists

DB_PATH = "data/app.db"