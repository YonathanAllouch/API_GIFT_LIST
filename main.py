from fastapi import FastAPI, HTTPException
from typing import List
import json
from models import StoredItem, UserGiftListRequest, ItemDescription, AgentItem  # Ensure these models are defined in your models.py
from crud import select_best_item, store_item, check_item_exists, get_all_agent_options
from agents import execute_parallel_searches
from gpt_agent import get_list_from_gpt  
from database import get_db_connection

app = FastAPI()

@app.post("/generate-gift-list/", response_model=List[StoredItem])
async def generate_gift_list(request: UserGiftListRequest):
    final_list = []

    # Use GPT to generate the gift list based on user input
    gpt_list = get_list_from_gpt(request.list_type, request.number_of_items, request.gender_of_gifts, request.price_range)

    # Ensure the GPT response is in the expected format, consider using json.loads() for safety
    try:
        items = json.loads(gpt_list)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid format received from GPT")

    with get_db_connection() as conn:
        for item in items:
            item_description = ItemDescription(**item)  # Create an ItemDescription object from each item
            # Check if the item already exists in the database
            if not check_item_exists(conn, item_description.description):
                # If not, use SerpAPI to get details for each item
                agent_results = execute_parallel_searches(item_description.description, item_description.price_range)
                # Process and store each result
                for result in agent_results:
                    if result:  # Ensure the result is not None
                        store_item(conn, item_description.description, result)

            # Retrieve all agent options for the current item from the database
            agent_options = get_all_agent_options(conn, item_description.description)
            # Select the best item based on rating and within the GPT-provided price range
            best_option = select_best_item(agent_options, item_description.price_range)
            if best_option:
                final_list.append(StoredItem(description=item_description.description, agent_items=[best_option]))

    return final_list

def process_and_store_results(conn, description: str, agent_results: List[dict]) -> List[AgentItem]:
    processed_results = []
    for result in agent_results:
        if result:
            agent_item = AgentItem(link=result['link'], price=result['price'], rating=result['rating'])
            processed_results.append(agent_item)
            # Store each result in the database
            store_item(conn, description, agent_item)
    return processed_results