import sqlite3
from models import GiftList

DATABASE_URL = "sqlite:///./test.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

def create_gift_list(gift_list: GiftList):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Adjust SQL commands for SQLite syntax if needed
    cursor.execute("INSERT INTO gift_lists (event_type) VALUES (?)", (gift_list.event_type,))
    list_id = cursor.lastrowid

    for item in gift_list.items:
        cursor.execute("INSERT INTO gift_items (list_id, name, price_range, description) VALUES (?, ?, ?, ?)",
                       (list_id, item.name, item.price_range, item.description))

    conn.commit()
    cursor.close()
    conn.close()
    return list_id

def get_gift_list(list_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gift_items WHERE list_id = ?", (list_id,))
    items = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert row objects to dictionaries
    items_list = [dict(item) for item in items]
    return items_list
