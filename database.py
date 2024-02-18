import sqlite3

# Path to your SQLite database
DATABASE_PATH = "my_project_db.sqlite"

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(DATABASE_PATH)

# Create a cursor object using the connection
cursor = conn.cursor()

create_table_query ='''CREATE TABLE IF NOT EXISTS gift_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    estimated_price TEXT NOT NULL,
    agent_low_link TEXT,
    agent_low_rating TEXT,
    agent_mid_link TEXT,
    agent_mid_rating TEXT,
    agent_high_link TEXT,
    agent_high_rating TEXT
);'''


# Execute the SQL commands
cursor.execute(create_table_query)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database initialized and table created.")
