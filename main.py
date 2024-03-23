from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json
from models import StoredItem, UserGiftListRequest, ItemDescription, AgentItem  # Ensure these models are defined in your models.py
from crud import select_best_item, store_item, check_item_exists, get_all_agent_options
from agents import execute_parallel_searches
from gpt_agent import get_list_from_gpt  
from database import get_db_connection
from delete_old_items import delete_old_items
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
logger = logging.getLogger("uvicorn")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type",
        "Content-Length",
        "Host",
        "User-Agent",
        "Accept",
        "Accept-Encoding",
        "Connection",
        ],
)

@app.post("/generate-gift-list/", response_model=List[StoredItem])
async def generate_gift_list(request: UserGiftListRequest):
    logger.info("Received request to generate gift list.")
    delete_old_items()
    final_list = []
    try:
        # Use GPT to generate the gift list based on user input
        gpt_list = get_list_from_gpt(request.list_type, request.number_of_items, request.gender_of_gifts, request.price_range)
        if not gpt_list or 'gifts' not in gpt_list:
            logger.error("GPT did not return any items or the 'gifts' key is missing..")
            raise HTTPException(status_code=404, detail="No items found")
        #key_to_access = list(gpt_list.keys())[0]
        gift_list = gpt_list['gifts']
        with get_db_connection() as conn:
            for item in gift_list:
                values_list = list(item.values())  # Convert the dictionary values to a list
                item_description = ItemDescription(description=values_list[0] , price_range=values_list[1])  # Create an ItemDescription object from each item
                # Check if the item already exists in the database
                if not check_item_exists(conn, item_description.description):
                    logger.info(f"Item not found in DB, executing searches for: {item_description.description}")
                    # If not, use SerpAPI to get details for each item
                    agent_results = execute_parallel_searches(item_description.description, item_description.price_range)
                    # Initialize default results for each agent in case they return None
                    default_agent_result = {'link': None, 'price': None, 'rating': None}
                    # Process agent results
                    processed_results = []
                    for result in agent_results:
                        # Replace None results with the default result
                        processed_result = result if result is not None else default_agent_result
                        processed_results.append(processed_result)

                    # Ensure we have exactly 3 items in processed_results
                    if len(processed_results) == 3:
                        agent1_result, agent2_result, agent3_result = processed_results
                        store_item(conn, item_description.description, agent1_result, agent2_result, agent3_result)
                    else:
                        # Handle unexpected case where processed_results does not contain 3 items
                        print("Error: Expected 3 agent results, received:", len(processed_results))
                else:
                    logger.info(f"Item found in DB, retrieving options for: {item_description.description}")

                # Retrieve all agent options for the current item from the database
                agent_options = get_all_agent_options(conn, item_description.description)
                # Select the best item based on rating and within the GPT-provided price range
                best_option = select_best_item(agent_options, item_description.price_range)
                if best_option:
                    best_agent_item = AgentItem(
                        link=best_option.link,  # Ensure this is a valid URL or string
                        price=best_option.price,  # Should be a string representing the price
                        rating=best_option.rating  # Should be a float
                    )
                    final_list_item = StoredItem(description=item_description.description, agent_items=[best_agent_item])
                    final_list.append(final_list_item)
        logger.info("Gift list generated successfully.")
    except HTTPException as http_ex:
        logger.error(f"HTTPException occurred: {http_ex.detail}")
        raise
    except Exception as ex:
        logger.exception("An error occurred while generating gift list.")
        raise HTTPException(status_code=500, detail="Internal Server Error")
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