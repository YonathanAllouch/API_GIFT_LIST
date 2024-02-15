import sqlite3

# Path to your SQLite database
DATABASE_PATH = "my_project_db.sqlite"

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(DATABASE_PATH)

# Create a cursor object using the connection
cursor = conn.cursor()

# SQL statement to create the 'gift_lists' table
#TO DO: Fix the SQL statement to create the 'gift_lists' table
'''create_gift_lists_table = """
CREATE TABLE IF NOT EXISTS gift_lists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL
);
"""
'''

# SQL statement to create the 'gift_items' table
#TO DO: Fix the SQL statement to create the 'gift_items' table
'''create_gift_items_table = """
CREATE TABLE IF NOT EXISTS gift_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    list_id INTEGER,
    name TEXT NOT NULL,
    price_range TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (list_id) REFERENCES gift_lists (id)
);
"""
'''
# Execute the SQL commands
#cursor.execute(create_gift_lists_table)
#cursor.execute(create_gift_items_table)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database initialized and tables created.")
