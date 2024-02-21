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
def store_item(conn, description: str, agent1_item: dict, agent2_item: dict, agent3_item: dict):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO gift_items (
            description, 
            agent1_link, agent1_price, agent1_rating, 
            agent2_link, agent2_price, agent2_rating, 
            agent3_link, agent3_price, agent3_rating
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        description, 
        agent1_item['link'], agent1_item['price'], agent1_item['rating'], 
        agent2_item['link'], agent2_item['price'], agent2_item['rating'], 
        agent3_item['link'], agent3_item['price'], agent3_item['rating']
    ))
    conn.commit()

def get_all_agent_options(conn, description: str) -> List[AgentItem]:
    cursor = conn.cursor()
    # Query updated to select agent data for all three agents
    cursor.execute("""
        SELECT 
            agent1_link, agent1_price, agent1_rating, 
            agent2_link, agent2_price, agent2_rating, 
            agent3_link, agent3_price, agent3_rating 
        FROM gift_items WHERE description=?
    """, (description,))
    rows = cursor.fetchall()

    # Flatten the results to a list of AgentItem, accounting for each agent in a row
    agent_items = []
    for row in rows:
        # Assuming row is a tuple and using indexing
        agent_items.append(AgentItem(link=row[0], price=row[1], rating=row[2]))  # Agent 1
        agent_items.append(AgentItem(link=row[3], price=row[4], rating=row[5]))  # Agent 2
        agent_items.append(AgentItem(link=row[6], price=row[7], rating=row[8]))  # Agent 3

    return agent_items

def select_best_item(agent_options: List[AgentItem], price_range: str) -> AgentItem:
    low_price, high_price = map(int, [s.strip() for s in price_range.replace('$', '').split('-')])
    valid_options = [option for option in agent_options if low_price <= float(option.price.strip('$')) <= high_price]
    return max(valid_options, key=lambda x: (x.rating, -float(x.price.strip('$'))), default=None)
