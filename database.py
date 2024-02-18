import sqlite3

DATABASE_URL = "./test.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS gift_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                agent1_link TEXT, agent1_price TEXT, agent1_rating REAL,
                agent2_link TEXT, agent2_price TEXT, agent2_rating REAL,
                agent3_link TEXT, agent3_price TEXT, agent3_rating REAL
            );
        """)
        conn.commit()

init_db()
