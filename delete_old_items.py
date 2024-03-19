import sqlite3
DATABASE_URL = "./test.db" 

def delete_old_items():
    with sqlite3.connect(DATABASE_URL) as conn:
        conn.execute("DELETE FROM gift_items WHERE created_at < DATETIME('now', '-24 hours')")
        conn.commit()

if __name__ == "__main__":
    delete_old_items()
