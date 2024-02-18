import sqlite3
from typing import List
from models import AgentItem

DATABASE_URL = "sqlite:///./test.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL.replace("sqlite:///", ""))
    conn.row_factory = sqlite3.Row
    return conn

def check_item_exists(conn, description: str) -> bool:
    cursor = conn.cursor()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM gift_items WHERE description=?)", (description,))
    return cursor.fetchone()[0] == 1

def store_item(conn, description: str, agent_item: AgentItem):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO gift_items (description, agent_link, agent_price, agent_rating)
        VALUES (?, ?, ?, ?)
    """, (description, agent_item.link, agent_item.price, agent_item.rating))
    conn.commit()

def get_all_agent_options(conn, description: str) -> List[AgentItem]:
    cursor = conn.cursor()
    cursor.execute("SELECT agent_link, agent_price, agent_rating FROM gift_items WHERE description=?", (description,))
    rows = cursor.fetchall()
    return [AgentItem(link=row['agent_link'], price=row['agent_price'], rating=row['agent_rating']) for row in rows]

def select_best_item(agent_options: List[AgentItem], price_range: str) -> AgentItem:
    low_price, high_price = map(int, price_range.split('-'))
    valid_options = [option for option in agent_options if low_price <= int(option.price.strip('$')) <= high_price]
    return max(valid_options, key=lambda x: (x.rating, -int(x.price.strip('$'))), default=None)
